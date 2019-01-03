# CAD (Computer Aided Design)

This project aims for perfect and flawless object-oriented development. 
It's focused on using best practices, suitable design patterns, proper testing, 
and overall healthy code as it is a semestral project for an object-oriented 
programming course (BI-OOP) at FIT CTU.

The subject of this project is a simple version of Computer Aided Design (CAD). 
It provides GUI with following features:
* Command line interface
* History of all commands
* Drawing basic shapes (dots, lines, polylines, rectangles and circles)
* Shape preview while drawing
* Color choosing
* Moving and deleting shapes
* Undo and redo
* Saving and loading
* Output list of objects on some point (or on the whole canvas)


A user can interact with the application in two different ways - via command line 
interface (takes commands described below) or graphical user interface.

Above CLI is a history of all commands that have been executed (no matter whether
they were created via CLI or GUI) and messages that these commands can produce.
There's also a status bar in the left bottom corner indicating which action is
currently selected and if the file is saved/loaded, a message will appear there
as well.

The user can select an action via their icons. After choosing one, the action 
button will be highlighted, as well as there will be a name of the action in the 
status bar (bottom left corner). The default action is the move action (it means 
that if there's no action button pressed, the move action is active).
Also, the color of the shape to be drawn can be changed after clicking on the color 
button (the last one in the left toolbar).

The mouse cursor is changing according to the action you're about to do:
* Crosshair if you are drawing a shape
* Pointing hand if you are deleting a shape or choosing a brush
* Open hand if you are choosing a shape to move
* Closed hand if you have already chosen a shape and you are choosing where to
place it

Common key-shortcuts are also available (ctrl+s, ctrl+l, ctrl+n, ctrl+w, ctrl+z, 
ctrl+shift+z).

## Architecture
Model-View-Presenter architecture


## Design patterns

We've used following design patters:
* Polymorphism - shapes, shape factories, printers, commands, brushes
* Double-dispatch - we call `shape.print_to(printer)` on given shape (first 
dispatch) and then call respective method for printing concrete shape on given 
printer (second dispatch)
* Visitor pattern - printers (visitor) and shapes (object)
* Factory pattern - shape factories (rectangle and circle)
* Observer pattern - controller observes shapes store
* Parser combinators???
* Strategy pattern - canvas brushes
* Singleton - canvas brushes


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
pyrcc5 ./app/ui/resources.qrc -o ./app/ui/resources.py
```

#### UI

Run (from root folder):
```
pyuic5 ./app/ui/main_window.ui -o ./app/ui/main_window.py
``` 
and change `import resources_rc` (at the bottom of the file) to `import app.ui.resources`.

## Tests

To run tests, just make sure you are inside the application's root directory and 
that you are working under your virtual environment. Then just run tests via:
```
pytest
```