# Android Second Screen on Linux

This application is developped because they're many on Windows or Mac, but nothing on linux. This allows you to use your android smartphone as a second screen on your linux computer, with your parameters like resolution and the position of se second screen. That use VNC so the fluidity may be bad, depending the connection, resolution or framerate. Don't hesitate to contribute for more compatibility and accuracy.

## Precondition

To run this programme you'll need some features.

* python3 (of course)
* x11vnc

You can of course use any vnc viewer for your android device, I use bVNCpro. It may be usefull to add a function to choose which VNC you would use.
Don't worry GTX1050 users, I have a solution for you ! :
Just create a file  `/usr/share/X11/xorg.conf.d/20-intel.conf` and edit it as super user :
```
Section "Device"
Identifier "intelgpu0"
Driver "intel"
Option "VirtualHeads" "2"
EndSection
```
Then logout or restart.

## How to use

They're few parameters :

* `-s` or `--screen-position`
  * After this parameter you can enter where your new screen will be placed acording your main screen. You can enter `left`, `right`, `top` or `bottom`. This argument is the only one required to launch the soft.
* `-r` or `--resolution`
  * After this parameter you have to enter the resolution you want. Be cautious, a high resolution and framerate will increase the ping.
* `-f` or `--framerate`
  * After this parameter must be the framerate you want. Be cautious, a high resolution and framerate will increase the ping.
* `-p` or `--primary`
  * This allows you to make the new screen you're configuring as your main screen.

### Example

```
./SecondScreenAndroid.py -s right -r 1920x1080 -f 30 -p
```
This command create a second screen on the right of your current screen, with a full HD resolution at 30 fps.

## To fix

* The second screen doesn't place itself at the right place. Top argument place it at the right.
* x11vnc is a litle bit chatty, it may be better to setup a verbose mode.
* Add an option to turn off the screen when you want
* x11vnc doesn't always clip the right screen part
