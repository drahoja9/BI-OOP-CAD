import os
import sys

# Adding root folder of this application to PYTHON_PATH to be able to import the whole app in tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app
