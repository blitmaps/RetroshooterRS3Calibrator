# Retroshooter R3 Reaper Calibration Utility

## What is this?
This is a small python program which calibrates the R3 Reaper Lightgun on Linux; 
instead of using the (Windows Only) utility from the manufacturer.

I made this utility for myself, for use on Bazzite Linux (like SteamOS).
I am open-sourcing it as it utilises some GPL code from the
Batecera Linux Distribution, and it may be helpful to others.


## How do I use it?
You should install it first, and then you can launch `calibrate.sh` from your favourite launcher, to calibrate the lightgun. 
It works the same as the other utilities, you point the gun at targets on the screen, and fire. The gun's internal firmware
is then programmed and the calibration is 'commited'.

### Limitations:

* Currently, the utility will calibrate only the Player 1 gun. This could be extended, but it is not a priority for me.
* The utility is designed for a DPI scaled 4kTV. If targets do not appear near the edges of the monitor or the first is not
dead center, then you may need to adjust the scaling properties.
* I've not added configurations etc. Variables are hard coded, as they are what I need.
* The code is low quality, as I ported from Batecera's codebase and did not want to mess with the application logic too much.

## Installation

### Non Bazzite Distributions
You will need your user to be able to write to the raw HID device files on the machine, and control the display (if this is arcane to you, just follow the steps).
On Bazzite, this is not required, but it is on, for example Arch.

### User Permissions to Access the Guncon
#### 1. Add plugdev as a user group if it does not exist
```commandline
sudo groupadd plugdev
```
#### 2. Create a UDev rule to allow you to write to the HIDRaw devices
```commandline
sudo nvim /etc/udev/rules.d/99-hidraw-permissions.rules
```
Adding this text:
```commandline
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0660", GROUP="plugdev"
```
and saving.

#### 3. Adding your user to the group
```commandline
sudo usermod -a -G plugdev YOUR_USERNAME_DONT_COPY_ME_YOU_SILLY_GOOSE
```
then reboot with `sudo reboot`.

### Installing the utility on Bazzite 
#### (PR if you have installation instruction on somthing else)
In the root of the repo directory, run the installer for the dependencies 
```commandline
./install_dependencies.sh
```



