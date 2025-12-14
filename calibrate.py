# Retroshooter Guncon Calibration routine
# written by: Copyright (c) 2025 Bradley Pearce
# This code is released under the GNU General Public License, the same version as
# the code upon which it is based, from the Batocera Linux Distribution, see below:

#
# This file is part of the batocera distribution (https://batocera.org).
# Copyright (c) 2022 Nicolas Adenis-Lamarre.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# YOU MUST KEEP THIS HEADER AS IT IS
#
#
import binascii
import evdev
import hid
from evdev import ecodes
import select
from pyray import *
import time
import pytoml as toml


###### Calibration variables (DO NOT EDIT THESE, these are edited in the config.toml, and are added here as defaults)

# This identifies the guns, the 'Mouse' is always needed, and perhaps the '1' to a '2' if its the second gun
RETROSHOOTER_NAME = '3A-3H Retro Shooter 1'
CALIBRATION_TARGET = 'Mouse'
# Some displays have a different logical and physical resolution, adjust this number until the targets are aligned properly
desktop_scaling = 2
display_w = 1920 * desktop_scaling
display_h = 1080 * desktop_scaling
# Adjust these if the targets are too small for you
target_size = 100
half_size = int(target_size / 2)

def load_configuration():
    """
    Loads configuration
    :return: returns False if literally anything goes wrong
    """
    try:
        with open('config.toml', 'rb') as fin:
            cfg = toml.load(fin)
            global RETROSHOOTER_NAME
            global CALIBRATION_TARGET
            global display_h, display_w, target_size, half_size, desktop_scaling
            RETROSHOOTER_NAME = f'3A-3H Retro Shooter {cfg['gun']['player']}'
            CALIBRATION_TARGET = cfg['gun']['calibration_target']
            desktop_scaling = cfg['display']['dpi_scaling']
            display_w = cfg['display']['x_resolution'] * desktop_scaling
            display_h = cfg['display']['y_resolution'] * desktop_scaling
            target_size = cfg['calibration']['target_size']
            half_size = int(target_size / 2)
            print(cfg)
            return True
    except:
        return False

def get_retroshooter_devices():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if RETROSHOOTER_NAME in device.name and CALIBRATION_TARGET in device.name:
            return device.path
    return None


def get_retroshooter_hid():
    for x in hid.enumerate():
        print(x)
        if RETROSHOOTER_NAME in x['product_string']:
            return x['path']
    return None


def get_retroshooter_paths():
    devpath = get_retroshooter_devices()
    hidpath = get_retroshooter_hid()
    if devpath is None or hidpath is None:
        return None, None
    return devpath, hidpath

def draw_target(x, y, size=50, color=RED):
    draw_rectangle(x, y, size, size, color)
    draw_rectangle(x, int(y + (size / 2)) - 3, size, 5, BLACK)
    draw_rectangle(int(x + (size / 2)) - 3, y, 5, size, BLACK)


def moveTargetTo(fromPosition, toPosition):
    currentPosition = fromPosition
    while fromPosition[0] != toPosition[0] or fromPosition[1] != toPosition[1] :
        if currentPosition[0] < toPosition[0]:
            currentPosition[0] = currentPosition[0] +1
        if currentPosition[0] > toPosition[0]:
            currentPosition[0] = currentPosition[0] -1
        if currentPosition[1] < toPosition[1]:
            currentPosition[1] = currentPosition[1] +1
        if currentPosition[1] > toPosition[1]:
            currentPosition[1] = currentPosition[1] -1
        target.write(ecodes.EV_ABS, ecodes.ABS_X, currentPosition[0])
        target.write(ecodes.EV_ABS, ecodes.ABS_Y, currentPosition[1])
        target.syn()
        time.sleep(0.001) # x1000 = 1 second



if __name__ == "__main__":

    did_configure_successfully = load_configuration()

    if not did_configure_successfully:
        print("Configuration loading failed, there must be a valid config.toml next to calibrate.py")
        exit()

    # These variables are used in the calibration process
    has_calibration_begun = False
    has_calibration_completed = False
    shot_count = 0
    frompos = [0, 0]
    target_pos = [-1, -1]

    devpath, hidpath = get_retroshooter_paths()

    try:
        input_dev = evdev.InputDevice(devpath)
        hidin = open(hidpath, "wb")
    except:
        print("Gun is not detected, please connect it and try again, or view the config.toml")
        exit()

    absVals = [[0, 100], [0, 100]] # input rectangle
    for (code, inf) in input_dev.capabilities()[ecodes.EV_ABS]:
        if code == ecodes.ABS_X:
            absVals[0] = [inf.min, inf.max]
        if code == ecodes.ABS_Y:
            absVals[1] = [inf.min, inf.max]
    poll = select.poll()
    poll.register(input_dev.fd, select.POLLIN)
    evkeys = [ecodes.KEY_CONFIG]
    for (code) in input_dev.capabilities()[ecodes.EV_KEY]:
        evkeys.append(code)

    target = evdev.UInput(name="Retro Shooter Lightgun", events={
        ecodes.EV_ABS: [
            (ecodes.ABS_X, evdev.AbsInfo(value=0, min=absVals[0][0], max=absVals[0][1], fuzz=0, flat=0, resolution=0)),
            (ecodes.ABS_Y, evdev.AbsInfo(value=0, min=absVals[1][0], max=absVals[1][1], fuzz=0, flat=0, resolution=0))
        ],
        ecodes.EV_KEY: evkeys})


    init_window(display_w, display_h, "Gun Calibration")
    toggle_fullscreen()
    hide_cursor()


    while not window_should_close():

        if is_key_down(KeyboardKey.KEY_ONE):
            close_window()

        begin_drawing()
        clear_background(BLACK)
        #draw_target(10, 10, size=50, color=RED)
        xx = get_mouse_x()
        yy = get_mouse_y()


        if not has_calibration_begun:
            draw_text("Shoot anywhere to begin calibration... Then shoot each target once", int(display_w/4), int(display_h/2), 42, VIOLET)
            draw_target(xx - half_size, yy - half_size, size=target_size, color=BLUE)

        if has_calibration_completed:
            draw_text("Writing Calibration, this might freeze a sec...", int(display_w/4), int(display_h/2), 42, VIOLET)
            draw_text("Press the first button to quit", int(display_w/4), int(display_h/2)+50, 42, VIOLET)

            draw_target(xx - half_size, yy - half_size, size=target_size, color=BLUE)
            end_drawing()
            continue

        if not target_pos[0] == -1:
            draw_target(target_pos[0] - half_size, target_pos[1] - half_size, size=target_size, color=RED)

        if poll.poll(15):
            for event in input_dev.read():
                if event.type == ecodes.EV_KEY and event.code == ecodes.BTN_LEFT and event.value == 1:

                        w = get_screen_width()
                        h = get_screen_height()

                        shot_count += 1

                        if shot_count == 1:
                            target.write(ecodes.EV_KEY, ecodes.KEY_CONFIG, 1)
                            target.syn()

                            frompos = [absVals[0][0] + round((absVals[0][1] - absVals[0][0]) * 0.5),
                                       absVals[1][0] + round((absVals[1][1] - absVals[1][0]) * 0.0)]
                            topos = [absVals[0][0] + round((absVals[0][1] - absVals[0][0]) * 0.5),
                                     absVals[1][0] + round((absVals[1][1] - absVals[1][0]) * 0.5)]
                            target_pos = [int(w/2), int(h/2)]

                            print(target_pos)
                            moveTargetTo(frompos, topos)
                            hidin.write(binascii.unhexlify('AA66'))
                            hidin.flush()

                        if shot_count == 2:
                            hidin.write(binascii.unhexlify('AAB1'))  # '\xaa\xb1'
                            hidin.flush()
                            frompos = [absVals[0][0] + round((absVals[0][1] - absVals[0][0]) * 0.5),
                                       absVals[1][0] + round((absVals[1][1] - absVals[1][0]) * 0.5)]
                            topos = [absVals[0][0] + round((absVals[0][1] - absVals[0][0]) * 0.1),
                                     absVals[1][0] + round((absVals[1][1] - absVals[1][0]) * 0.1)]
                            target_pos = [int(w * 0.1), int(h * 0.1)]

                            print(target_pos)
                            moveTargetTo(frompos, topos)

                        if shot_count == 3:
                            hidin.write(binascii.unhexlify('AAB2'))
                            hidin.flush()
                            frompos = [absVals[0][0] + round((absVals[0][1] - absVals[0][0]) * 0.1),
                                       absVals[1][0] + round((absVals[1][1] - absVals[1][0]) * 0.1)]
                            topos = [absVals[0][0] + round((absVals[0][1] - absVals[0][0]) * 0.9),
                                     absVals[1][0] + round((absVals[1][1] - absVals[1][0]) * 0.9)]
                            target_pos = [int(w * 0.9), int(h * 0.9)]

                            print(target_pos)
                            moveTargetTo(frompos, topos)

                        if shot_count == 4:
                            hidin.write(binascii.unhexlify('AAB3'))
                            hidin.flush()
                            frompos = [absVals[0][0] + round((absVals[0][1] - absVals[0][0]) * 0.9),
                                       absVals[1][0] + round((absVals[1][1] - absVals[1][0]) * 0.9)]
                            topos = [absVals[0][0] + round((absVals[0][1] - absVals[0][0]) * 0.9),
                                     absVals[1][0] + round((absVals[1][1] - absVals[1][0]) * 0.1)]
                            target_pos = [int(w * 0.9), int(h * 0.1)]

                            print(target_pos)
                            moveTargetTo(frompos, topos)

                        if shot_count == 5:
                            hidin.write(binascii.unhexlify('AAB4'))
                            hidin.flush()
                            hidin.write(binascii.unhexlify('AAB5'))
                            hidin.flush()
                            target.write(ecodes.EV_KEY, ecodes.KEY_CONFIG, 0)
                            target.syn()
                            has_calibration_completed = True

                        has_calibration_begun = True

        end_drawing()
    show_cursor()
