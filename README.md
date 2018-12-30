# CAD (Computer Aided Design)

This project aims for perfect and flawless object-oriented development. 
It's focused on using best practices, suitable design patterns, proper testing, 
and overall healthy code as it is a semestral project for an object-oriented 
programming course (BI-OOP) at FIT CTU.

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

Create a virtual environment via `venv` (2nd *venv* is name of the folder with 
virtual environment):
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
./run.py
```

### Generating UI and/or resources

#### Resources

Run (from root folder):
```
pyrcc5 .\app\ui\resources.qrc -o .\app\ui\resources.py
```

#### UI

Run (from root folder):
```
pyuic5 .\app\ui\main_window.ui -o .\app\ui\main_window.py
``` 
and change `import resources_rc` (at the bottom of the file) to `import app.ui.resources`.

## Tests

To run tests, just make sure you are inside the application's root directory and 
that you are working under your virtual environment. Then just run tests via:
```
pytest
```