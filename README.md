# Embedded OCR-to-Speech System for Visually Impaired Users

## About
This repository contains the code for a wearable device that helps visually impaired users to read text in natural scene conditions. It is capable of taking a picture, performing optical character recognition on it, and producing a text-to-speech output for the user.

The script uses PaddleOCR to perform optical character recognition, and Piper to perform text-to-speech (thank you Danny).

There is a `main.py` script that can be run on Windows/Linux machines to test the functionality of the system (see the Setup for Linux/Windows instructions below).

A RaspberryPi-specific script is coming soon!

## Setup

### Setup for Linux/Windows

*Ensure that you have Python version 3.10 or later installed on your system.*

*PaddleOCR is known to have issues with MacOS running on M-series chips. You can attempt to follow the instructions below for the Linux installation, but it is not guaranteed to work.*

**NOTE:** *Since this project uses the pynput package for monitoring keyboard events, this script will not work on Linux DEs using the Wayland Protocol.*

Run the following commands in a terminal.

#### Download/Clone the repository in any directory you'd like.

```
git clone https://github.com/seaflop/capstone
```

#### Navigate to the `capstone` directory.

```
cd capstone
```

#### Activate a Python virtual environment.

Linux:

```
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```
python -m venv .venv
.venv\Scripts\Activate
```

#### Download the required packages.

```
pip install -r requirements.txt
```

#### Run the Script

Run the script from the `capstone` directory, and provide the path to the image you'd like to test on.

```
python ./src/main.py -i "pathtoyourimagehere.jpg"
```

The script will play a "ding" noise when it is ready to run. This may take some time, especially on the first run, as all the models will have to be downloaded first.

Press Space to start the script.

You can exit the script at any time by pressing the Esc key.

Audio playback can be paused/resumed by pressing the spacebar.

### Setup for Raspberry Pi

Required Hardware:

- Raspberry Pi 4
- Raspberry Pi Camera 3
- Button connected to GPIO 

#### Activate a Python virtual environment

Make sure to include system-wide packages.

```
python3 -m venv .venv --system-site-packages
source .venv/bin/activate

```
