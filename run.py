import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.controller import Controller


if __name__ == '__main__':
    controller = Controller()
