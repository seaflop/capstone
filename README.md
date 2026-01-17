# Embedded OCR-to-Speech System for Visually Impaired Users

## About
This repository contains the code for a wearable device that helps visually impaired users read text in natural scene conditions. There is also a version of the script that can be run on Windows/POSIX-compliant machines to test functionality. Both versions are capable of taking a picture, performing optical character recognition on it, and producing a text-to-speech output for the user.

This script uses [RapidOCR](https://github.com/RapidAI/RapidOCR) for text detection/recognition and [Piper](https://github.com/rhasspy/piper) for text-to-speech functionality (thank you Danny!).

This project is still in progress, so check back every once in a while for updates!

*Expected completion: April 2026.*

## Setup for POSIX/Windows

*Ensure that you have Python version 3.10.0 or later installed on your system.*

**NOTE:** *Since this project uses the pynput package for monitoring keyboard events, this script will not work on Linux DEs using the Wayland Protocol and requires sudo permissions to work on MacOS.*

**1. Download/Clone the repository in any directory you'd like.**

```
git clone https://github.com/seaflop/assistive-reader
```

**2. Navigate to the `capstone` directory.**

```
cd assistive-reader
```

**3. Activate a Python virtual environment.**

```
python -m venv .venv
.venv\Scripts\Activate
```

**4. Download the required packages.**

```
pip install --upgrade pip
pip install -r requirements.txt
```

**5. Run the Script**

Run the script from the `capstone` directory.

**Flags:**  
- `-w`: Use the webcam to take a picture.  
- `-i`: Specify the path to an existing image.  
_Use of at least one of these flags is required_

POSIX:

```
python ./src/main.py -i "pathtoyourimagehere.jpg"
python ./src/main.py -w
```

Windows:

```
python .\src\main.py -i "pathtoyourimagehere.jpg"
python .\src\main.py -w
```

The script will prompt you for input when it is ready to run. This may take some time, especially on the first run, as all the models will have to be downloaded first.

Press Space to start the script.  
If you specified `-w`, press Space to take a picture, or Esc to exit.  
You can exit the script at any time by pressing the Esc key.  
Audio playback can be paused/resumed by pressing Space.