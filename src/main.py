import sys

from .application import EigenApplication

def main(version):
    app = EigenApplication()
    return app.run(sys.argv)
