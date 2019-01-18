#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--screen-position",
                    type=str,
                    action="store",
                    dest="screen_position",
                    required=True,
                    help="Screen position regarding your main or current screen : left, right, top, bottom")
parser.add_argument("-r", "--resolution",
                    type=str,
                    action="store",
                    default="1920x1080",
                    dest="resolution",
                    help="New screen resolution : widthxheight \n default value = 1920x1080")
parser.add_argument("-f", "--framerate",
                    type=str,
                    action="store",
                    default="30",
                    dest="framerate",
                    help="New screen framerate \n default value = 30")
parser.add_argument("-p", "--primary",
                    action="store_true",
                    dest="primary",
                    help="Make the new screen your primary screen")
arg = parser.parse_args()


def debug(str):
    print('[DEBUG] ' + str)


def getModeline():
    '''
    Get the modeline depending your parameters (resolution and framerate)
    This modeline is used by xrandr to create a new mode for the virtual screen.
    you can get the modeline by using $gtf width height framerate
    '''
    resolution = arg.resolution.split("x")
    command = 'gtf ' + resolution[0] + " " + resolution[1] + " " + arg.framerate
    modeline = os.popen(command).read().split("Modeline ")
    modeline = modeline[1].split("\n")[0]
    model_name = modeline.split('"')[1]
    return modeline, model_name


def searchMainScreen():
    '''
    By writing $xrandr in a terminal, you can see all screen connected to your computer.
    The main screen is specified by "primary"
    '''
    xrandr = os.popen("xrandr").read().split('\n')
    for line in xrandr:
        if line.count("primary") == 1:
            mainScreen = line.split(" ")[0]
    return mainScreen


def newMode(modeline, model_name):
    '''
    Verifying if the model already exist, and creat it if not.
    '''
    xrandr = os.popen("xrandr").read()
    if xrandr.count(model_name) <= 0:
        error = os.popen("xrandr --newmode " + modeline).read()
        print(error)
    else:
        print("Mode already exist")


def addMode(model_name):
    '''
    Add the modeline to the VIRTUAL1 screen
    '''
    error = os.popen("xrandr --addmode VIRTUAL1 " + model_name).read()
    if len(error) > 0:
        print(error)
    else:
        print("Mode added to VIRTUAL1")


def activeScreen(modeline, mainScreen):
    '''
    Configure the screen using xrandr depending of your arguments : resolution, screen resolution and primary
    '''
    command = "xrandr --output VIRTUAL1 --mode " + model_name
    if arg.screen_position == "left":
        command += " --left-of"
    elif arg.screen_position == "right":
        command += " --right-of"
    elif arg.screen_position == "bottom":
        command += " --below"
    elif arg.screen_position == "top":
        command += " --above"
    command += " " + mainScreen

    if arg.primary:
        command += " --primary"

    debug(command)
    error = os.popen(command).read()
    if len(error) > 0:
        print(error)
    else:
        print("The screen is configured and activated")


def shutDownScreen():
    '''
    Shutdown the VIRTUAL1 screen using xrandr
    This doesn't erase your configuration or mode
    '''
    error = os.popen("xrandr --output VIRTUAL1 --off").read()
    if len(error) > 0:
        print(error)
    else:
        print("The screen is off")


def shareScreen():
    command = "x11vnc -clip "
    xrandr = os.popen("xrandr").read().split("\n")
    for line in xrandr:
        if line.count("VIRTUAL1") == 1:
            model = line.split(" ")[2]
    command += model
    error = os.popen(command).read()


def getIP():
    ip = ""
    ifconfig = os.popen("ifconfig").read().split("\n")
    for line in ifconfig:
        if line.count("inet ") >= 1 and line.count("broadcast "):
            ip = line
    ip = ip.split("  netmask")[0]
    ip = ip.split("inet ")[1]
    print("Try to connect to the VPN using this IP : ", ip)


if __name__ == "__main__":
    modeline, model_name = getModeline()
    mainScreen = searchMainScreen()
    debug(modeline)
    debug(model_name)
    debug(mainScreen)
    newMode(modeline, model_name)
    addMode(model_name)
    activeScreen(modeline, mainScreen)
    getIP()
    shareScreen()
    # shutDownScreen()
