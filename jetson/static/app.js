( function ( io, $, CanvasJS ) {
    var socket = io.connect('http://' + document.domain + ':' + location.port, {
        reconnectionDelayMax: 1000,
        transports: ['websocket', 'polling']
    });

    // VIDEO STREAM
    var streamEl = document.getElementById('stream')
    var canvas = streamEl.getElementsByTagName('canvas')[0];
    canvas.width = CAMERA_WIDTH;
    canvas.height = CAMERA_HEIGHT;
    var stream = {
        startTime: new Date().getTime(),
        frameCt: 0,
        fps: streamEl.getElementsByClassName('fps')[0],
        context: canvas.getContext('2d')
    };

    // ROBOT STATS
    var robotStats = {
        connected_to_jetson: false,
        connected_to_robot: false
    };

    var robotEditables = {};

    socket.on('close disconnect', function() {
        robotStats.connected_to_jetson = false;
        updateRobotStats();
    });
    socket.on('reconnect', function() {
        socket.emit('request_driver_vision');
        socket.emit('request_network_tables');
    });

    // VIDEO STREAM
    var latestData = null;
    socket.on('driver_vision', function ( data ) {
        // Each time we receive some data, request some more!
        // socket.emit('request_driver_vision');
        latestData = data;
        stream.frameCt++;
    } );
    function updateImage() {
        if (!latestData) {
            return;
        }

        var img = new Image();
        img.src = latestData.raw;

        if (img) {
            stream.context.drawImage(img, 0, 0);
        }
    }
    setInterval(updateImage, 33);

    /// FRAMES PER SECOND
    function updateFps () {
        // Update fps (loop)
        var d = new Date().getTime(),
            currentTime = (d - stream.startTime) / 1000,
            result = Math.floor(stream.frameCt / currentTime);

        if (currentTime > 1) {
            stream.startTime = new Date().getTime();
            stream.frameCt = 0;
        }

        stream.fps.innerText = result;
    }
    setInterval(updateFps, 500);

    // NETWORK TABLES

    socket.on('network_tables_update', function (data) {
        data.connected_to_jetson = true;

        Object.assign(robotStats, _.pickBy(data, function(value, key) {
            return !_.startsWith(key, 'editable--');
        }));

        Object.assign(robotEditables, _.pickBy(data, function(value, key) {
            return _.startsWith(key, 'editable--');
        }));

        updateRobotStats();

        clearTimeout(updateTimeout);
        updateTimeout = setTimeout(updateRobotEditables, 100);
    });

    function updateRobotStats() {
        var $stats = $('#robotStatsInner');
        Object.keys(robotStats).sort().forEach(function (key) {
            var $existing = $stats.find('#stats_' + key);
            if ($existing.length) {
                $existing.find('span').text(robotStats[key]);
            } else {
                $stats.append(
                    $('<div>', { id: 'stats_' + key })
                    .append($('<b>').text(key))
                    .append(': ')
                    .append($('<span>').text(robotStats[key]))
                );
            }
        });

        if (!robotStats.connected_to_jetson || !robotStats.connected_to_robot) {
            $(document.body).addClass('disconnected');
        } else {
            $(document.body).removeClass('disconnected');
        }
    }

    // stop editables update from propagating while the driver
    // is interacting with the dropdown menu. 
    var isInteractingWithEditable = false;
    $('#robotEditablesInner')
        .on('mouseenter', function () {
            isInteractingWithEditable = true;
        })
        .on('mouseleave', function () {
            isInteractingWithEditable = false;
        });

    var updateTimeout;
    function updateRobotEditables() {
        if (isInteractingWithEditable) {
            clearTimeout(updateTimeout);
            updateTimeout = setTimeout(updateRobotEditables, 100);
            return;
        }

        var $editables = $('#robotEditablesInner').empty(),
            alreadyHandled = {};

        Object.keys(robotEditables).sort().forEach(function (key) {
            var value = robotEditables[key],
                keyParams = key.split('--'),
                type = keyParams[1], name = keyParams[2].split('/')[0];

            if (alreadyHandled[name]) {
                return;
            } else {
                alreadyHandled[name] = true;
            }

            if (type === 'chooser') {
                var keyPrefix = keyParams.slice(0, 2).join('--') + '--' + name,
                    options = robotEditables[keyPrefix + '/options'],
                    defaultValue = robotEditables[keyPrefix + '/default'],
                    selectedValue = robotEditables[keyPrefix + '/selected'] || defaultValue;

                var $options = options.map(function (o) {
                    return $('<option>')
                        .prop('selected', o === selectedValue)
                        .text(o)
                        .prop('value', o)
                });

                $('<div>', { id: 'editables_' + name })
                    .append($('<b>').text(name))
                    .append(': ')
                    .append(
                        $('<select>')
                            .append($options)
                            .change(function () {
                                $(this).prop('disabled', true);
                                socket.emit('edit_network_tables', {
                                    key: keyPrefix + '/selected',
                                    value: $(this).val(),
                                    type: 'string'
                                });
                            })
                    )
                    .appendTo($editables);

            } else if (type === 'boolean') {
                $('<div>', { id: 'editables_' + name })
                    .append($('<b>').text(name))
                    .append(': ')
                    .append(
                        $('<input type="checkbox">')
                            .prop('checked', value)
                            .change(function () {
                                $(this).prop('disabled', true);
                                socket.emit('edit_network_tables', {
                                    key: key,
                                    value: $(this).prop('checked'),
                                    type: 'boolean'
                                });
                            })
                    )
                    .appendTo($editables);

            } else if (type === 'number') {
                $('<div>', { id: 'editables_' + name })
                    .append($('<b>').text(name))
                    .append(': ')
                    .append(
                        $('<input type="text" class="editable-textfield">')
                            .val(value),
                        $('<input type="button" class="editable-update">')
                            .val('Update')
                            .click(function () {
                                var $field = $(this).prev(),
                                    newValue = $field.val();

                                if (+newValue === value) {
                                    return;
                                }

                                socket.emit('edit_network_tables', {
                                    key: key,
                                    value: newValue,
                                    type: 'number'
                                });
                                $field.prop('disabled', true);
                            })
                    )
                    .appendTo($editables);
            }
        });
    }

    var graphData = {};
    function initializeRobotGraphs() {
        $('#robotGraphsInner > .graph').each(function () {
            var $container = $(this),
                title = $container.data('graph-title'),
                varString = $container.data('graph-vars'),
                vars = varString.split(','),
                $inner = $('<canvas width="400" height="250">').appendTo($container);

            $('<div class="graph-title">').text(title)
                .append($('<span>').text('Reset').click(function () {
                    graphData[varString].datasets.forEach(function (dataset) {
                        dataset.data = [];
                    });
                }))
                .prependTo($container);

            var datasets = vars.map(function (varName) {
                return {
                    label: varName,
                    data: []
                };
            });

            var chart = new CanvasJS.Chart($inner.get(0), {
                type: 'line',
                options: {
                    scales: {
                        xAxes: [{
                            type: 'linear',
                            position: 'bottom'
                        }]
                    },
                    responsive: true,
                    animation: {
                        duration: 0
                    },
                    tooltips: {
                        enabled: false
                    },
                    elements: {
                        line: {
                            borderWidth: 0.1
                        },
                        point: {
                            radius: 0.5
                        }
                    }
                },
                data: {
                    datasets: datasets
                }
            });

            graphData[varString] = {
                vars: vars,
                datasets: datasets,
                chart: chart
            };
        });
    }
    initializeRobotGraphs();

    var startTs = Date.now();
    function updateRobotGraphs() {
        var deltaTs = Date.now() - startTs;
        Object.keys(graphData).forEach(function (key) {
            var keyData = graphData[key];
            keyData.datasets.forEach(function (dataset) {
                dataset.data.push({
                    x: deltaTs,
                    y: robotStats[dataset.label] || 0
                });
            });
            keyData.chart.update();
        });
    }

    var updateRobotGraphsInterval;
    $('#robotGraphsToggle').click(function () {
        if (updateRobotGraphsInterval) {
            clearInterval(updateRobotGraphsInterval);
            updateRobotGraphsInterval = undefined;
        } else {
            updateRobotGraphsInterval = setInterval(updateRobotGraphs, 100);
        }
    });

    // Request initial updates
    socket.emit('request_driver_vision');
    socket.emit('request_network_tables');

    // LOL
    $('#yeeButton').click(function () {
        var yee = $('#yee').fadeIn().get(0);
        yee.currentTime = 0;
        yee.play();

        setTimeout(function () {
            $('#yee').fadeOut();
            $(document).off('keydown click', prematureyeeEndYee);
        }, 7500);

        function prematureyeeEndYee () {
            $('#yee').hide();
            yee.pause();
        }
        $(document).one('keydown click', prematureyeeEndYee)

        return false;
    });

}( io, jQuery, Chart ) );
