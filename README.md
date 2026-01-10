# Embedded OCR-to-Speech System for Visually Impaired Users

## About
This repository contains the code for a wearable device that helps visually impaired users to read text in natural scene conditions.

The script uses PaddleOCR to perform optical character recognition, and Piper to perform text-to-speech.

There is a `main.py` script that can be run on Windows/Linux machines to test the functionality of the system (see the Setup for Linux/Windows instructions below).

A RaspberryPi-specific script is coming soon!

## Setup

### Setup for Linux/Windows

*Ensure that you have Python version 3.10 or later installed on your system.*

*PaddleOCR is known to have issues with MacOS running on M-series chips. You can attempt to follow the instructions below for the Linux installation, but it is not guaranteed to work*

**NOTE:** *Since this project uses the pynput package for monitoring keyboard events, this script will not work on Linux DEs using the Wayland Protocol.*

Download/Clone the repository.

```
$ git clone github.com/seaflop/capstone
```

Navigate to the `capstone` directory.

Activate a Python virtual environment.

Linux:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Windows:

```
$ python -m venv .venv
$ .venv\Scripts\Activate
```

Download the required packages.

```
$ pip install -r requirements.txt
```

Run the script from the `capstone` directory.

```
$ python ./src/main.py -i "path/to/your/image/here.jpg"
```

## To-do
