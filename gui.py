#!/usr/bin/env python3
'''
1. intro screen
2. QA + notes screen
3. give results on final screen
    - main Qs asked: x/y
    - follow up topics discovered a/b
    - follow up questions asked n/m
    - remark 1
    - remark 2
'''
from datetime import datetime
from enum import Enum
from functools import partial
import argparse
import os
import random
import sys
import typing
import uuid

import viz

from fbs_runtime.application_context.PySide2 import ApplicationContext as AppCtx
from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import (Qt, QUrl, Signal, Slot, QTimer, QObject)
from PySide2.QtGui import (
        QColor,
        QComboBox,
        QFont,
        QGridLayout,
        QPainter,
        QPen,
        QPixmap,
        QTransform)
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer, QSound, QSoundEffect
from PySide2.QtPrintSupport import *
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWidgets import *

EXPIRY_DATE = '9999-12-31'


class QHLine(QFrame):
    def __init__(self, stretch):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        sizepol = QtWidgets.QSizePolicy
        policy = QtWidgets.QSizePolicy(sizepol.Expanding, sizepol.Fixed)
        policy.setHorizontalStretch(stretch)
        self.setSizePolicy(policy)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


class Grid(QWidget):
    def __init__(self, *args, **kwargs):
        super(Grid, self).__init__(*args, **kwargs)
        # make the widgets
        layout = QGridLayout()

        layout.addWidget(QLabel('template11'), 0, 0, 1, 1)
        layout.addWidget(QComboBox(), 0, 1, 1, 1)
        layout.addWidget(QHLine(), 1, 0, 1, 2)
        layout.addWidget(QLabel('template2'), 2, 0, 1, 1)
        layout.addWidget(QComboBox(), 2, 1, 1, 1)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, mainWidget):
        QMainWindow.__init__(self)
        self.setWindowTitle('BETA: app template version 0.0.1')
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('File')
        self.file_menu = self.menu.addMenu('Edit')
        self.help_menu = self.menu.addMenu('View')
        self.help_menu = self.menu.addMenu('Help')

        def showHelp():
            helpBox = QMessageBox()
            helpBox.setText(HELP_DICT)
            helpButton = QPushButton('OK')
            helpBox.setDefaultButton(helpButton)
            helpBox.exec_()

        help_action = QAction('How to use this program', self)
        help_action.setStatusTip('How to use this program')
        help_action.triggered.connect(showHelp)
        self.help_menu.addAction(help_action)
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)
        self.setCentralWidget(mainWidget)

    def closeEvent(self, event):
        if DEV: event.accept()

        if True:  # PLACEHOLDER: add confirmation/cleanup dialogue here
            event.accept()
        else:
            event.ignore()

    @Slot()
    def exit_app(self, checked):
        QApplication.quit()


class AppContext(AppCtx):
    def __init__(self, *args, **kwargs):
        super(AppContext, self).__init__(*args, **kwargs)
        self.session_id = str(uuid.uuid4()) # good for debugging

    def run(self):
        self.grid = Grid()
        if DEV:
            print('show DEV things here...')
        self.mainWindow = MainWindow(self.grid)
        self.mainWindow.resize(1600, 900)
        self.mainWindow.show()
        if not DEV and datetime.today().isoformat() > EXPIRY_DATE:
            exitBox = QMessageBox()
            exitBox.setText('This program is no longer available')
            exitButton = QPushButton('OK')
            exitBox.setDefaultButton(exitButton)
            sys.exit(exitBox.exec_())
        return self.app.exec_()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev', '-d', help='''\
        reveals some more widgets and does not send session\
        data on program closing''')
    parser.add_argument('--live', '-l',
        help='enables live reloading when source code is changed',
        action='store_true')
    args = parser.parse_args()
    if (args.dev is not None and (
        args.dev.lower() in ('true', 't', 'tru', 'yes', 'y'))):
            DEV = True
    appctxt = AppContext()        # 1. Instantiate AppCtx
    appctxt.app.setStyle('Fusion')
    exit_code = appctxt.run()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
