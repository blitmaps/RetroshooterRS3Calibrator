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

## Configuration

There is a config.toml next to calibrate.py, this controls the behaviour of the calibration utility.

example:
```toml
[display]
x_resolution = 1920
y_resolution = 1080
dpi_scaling = 1

[gun]
player=1
calibration_target="Mouse"

[calibration]
target_size=100
```

If your gun registers as 'player 2' (my gray gun), then setting player=2 will calibrate that one.


### Limitations:
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

#### 4. Dependencies
We rely on `evtest`, `python3-devel`, `pkg-config` and `raylib`.
These will need to be installed from your distro's repos before setting up your python virtual environment. I'm happy
to take pull requests for installation commands.

#### 5. Setup a Python venv for calibrate.sh
The calibrate shell script will toggle to the python venv for you, but this is how you set it up. Change
directory to the location of `calibrate.sh` and run these commands:
```commandline
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```


### Installing the utility on Bazzite 
#### (PR if you have installation instruction on somthing else)
In the root of the repo directory, run the installer for the dependencies 
```commandline
./install_dependencies.sh
```



