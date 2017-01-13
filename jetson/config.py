HOST = '0.0.0.0'
PORT = 5801

# DRIVER VISION
DRIVER_CAMERA_PORT = 0
DRIVER_CAMERA_WIDTH = 424
DRIVER_CAMERA_HEIGHT = 240
DRIVER_CAMERA_FPS = 30
DRIVER_CAMERA_BRIGHTNESS = -10  # Tuned for the Lifecam 3000
DRIVER_CAMERA_EXPOSURE = 20
DRIVER_STREAM_INTERVAL = 0.02
DRIVER_STREAM_RETRY_INTERVAL = 0.5

# TARGETING
TARGETING_INTERVAL = 0.02
TARGETING_RETRY_INTERVAL = 0.5
TARGETING_CAMERA_PORT = 1
TARGETING_CAMERA_WIDTH = 424
TARGETING_CAMERA_HEIGHT = 240
TARGETING_CAMERA_FPS = 30
TARGETING_CAMERA_WHITE_BALANCE = 3000
TARGETING_CAMERA_BRIGHTNESS = -10
TARGETING_CAMERA_EXPOSURE = 20
TARGETING_LOWER_HSV_BOUND = (30, 108, 101)  # Tune this at each regional
TARGETING_UPPER_HSV_BOUND = (99, 255, 255)

# NETWORK TABLES
ROBOT_IP_ADDRESS = 'roborio-5045-frc.local'
# ROBOT_IP_ADDRESS = '127.0.0.1'  # For development
NT_DRIVER_DIRECTION_SELECTOR = 'editable--chooser--driver_direction'
NT_AUTONOMOUS_COMMAND_SELECTOR = 'editable--chooser--autonomous_command'
NT_AUTONOMOUS_POSITION_SELECTOR = ('editable--chooser--autonomous'
                                   '_start_position')
NT_MACRO_SELECTOR = 'editable--chooser--macro'