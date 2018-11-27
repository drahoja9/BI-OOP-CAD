# CAD (Computer Aided Design)

This project aims for perfect and flawless object-oriented development. 
It's focused on using best practices, suitable design patterns, proper testing, and overall healthy code 
as it is a semestral project for an object-oriented programming course (BI-OOP) at FIT CTU.

The subject of this project is a simple version of Computer Aided Design (CAD). 
It provides GUI with following features:
* Command line interface
* History of command line commands
* Drawing basic shapes (e.g., lines, polylines, rectangles, circles)
* Saving and loading
* Changing colors of new objects or all current lines on some position
* Output list of objects on some points


## How to run

First, make sure you have Python 3 installed.
```
python3 --version
```

Create a virtual environment via `venv` (2nd *venv* is name of the folder with virtual environment):
```
python3 -m venv venv
```

Activate your virtual environment:
```
source venv/bin/activate
```

Upgrade pip to latest version and install all dependencies:
```
pip install --upgrade pip && pip install -r requirements.txt
```

Run the app:
```
bin/run.py
```