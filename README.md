# 2017-robot

This repository contains the source code for [Team 5045's](http://team5045.com/#/home)
2017 season robot.

## Table of contents

- `./py` &ndash; runs on the RoboRIO: core drive code
  * `/subsystems`: Code that allows each of the robot's systems to carry out individual processes.
  * `/utils`: Code related to inputs and handling them.
  * `/commands`: Code that uses the previous two categories for functions such as `drive_with_controller.py`
- `./jetson` &ndash; runs on the Jetson TK1: vision systems, custom driver station, etc.

## License

The MIT License (MIT)

Copyright (c) 2017 White Station High School Robotics Team 5045

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.