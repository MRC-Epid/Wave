import argparse
import sys
import traceback

from PyQt5.QtWidgets import QApplication, QLabel, QSplashScreen, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

from .gui import MainWindow


def new_excepthook(type, value, tb):
    # by default, Qt does not seem to output any errors, this prevents that
    traceback.print_exception(type, value, tb)


sys.excepthook = new_excepthook


def main():
    import sys, time

    app = QApplication(sys.argv)

    # Create and display the splash screen
    splash_pix = QPixmap('Logo.png').scaled(300,300)

    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.setEnabled(False)
    # splash = QSplashScreen(splash_pix)
    # adding progress bar
    progressBar = QProgressBar(splash)
    progressBar.setMaximum(5)
    progressBar.setGeometry(0, splash_pix.height()-20, splash_pix.width(), 20)

    # splash.setMask(splash_pix.mask())

    splash.show()
#    splash.showMessage("<h1><font color='white'>Wave</font></h1>", Qt.AlignTop | Qt.AlignCenter, Qt.black)

    for i in range(1, 30):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()


    parser = argparse.ArgumentParser()
    # parser.add_argument(...)
    known_args = parser.parse_known_args()[0]

    qapp = QApplication(sys.argv)
    gui = MainWindow(**vars(known_args))
    gui.show()
    splash.finish(gui)
    sys.exit(qapp.exec_())


if __name__ == '__main__':
    main()