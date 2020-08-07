#!/usr/bin/env python3
from datetime import datetime
from enum import Enum
from functools import partial
import argparse
import os
from pathlib import Path
import random
import sys
import typing
import uuid

import viz

from fbs_runtime.application_context.PySide2 import ApplicationContext as AppCtx
from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import (Qt, QUrl, Signal, Slot, QTimer, QObject)
from PySide2.QtGui import *
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer, QSound, QSoundEffect
from PySide2.QtPrintSupport import *
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtWidgets import *

DEV = False
EXPIRY_DATE = '9999-12-31'
HELP_STRING = 'INSERT INSTRUCTIONS HERE'
BTNFUNCS = {
    'fn1': lambda _: print('fn1'),
    'fn2': lambda _: print('fn2'),
    'fn3': lambda _: print('fn3'),
    'fn4': lambda _: print('fn4'),
    'fn5': lambda _: print('fn5'),
    'fn6': lambda _: print('fn6'),
    'fn7': lambda _: print('fn7'),
    'fn8': lambda _: print('fn8'),
    }

VIZFUNCS = {
    'nucdist': viz.nucleotide_distribution,
    'pepdist': viz.peptide_distribution,
    'grecord': viz.plot_graphic_record,
    'fn4': lambda _: print(_),
    'fn5': lambda _: print(_),
    'fn6': lambda _: print(_),
    'fn7': lambda _: print(_),
    'fn8': lambda _: print(_),
    }


def get_result(fs_file, func):
    pass

def makePlotWindow(pic):
        image = QLabel()
        pic = QPixmap(appctxt.get_resource(pic))
        image.setPixmap(pic)
        return image

class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        sizepol = QtWidgets.QSizePolicy
        policy = QtWidgets.QSizePolicy(sizepol.Expanding, sizepol.Fixed)
        self.setSizePolicy(policy)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


class VizButtons(QWidget):
    def __init__(self, *args, **kwargs):
        super(VizButtons, self).__init__(*args, **kwargs)
        self.btnGroup = QButtonGroup()
        self.btnGroup.buttonClicked[int].connect(self.onClick)
        self.btn1 = QPushButton()
        self.btn2 = QPushButton()
        self.btn3 = QPushButton()
        self.btn4 = QPushButton()
        self.btn5 = QPushButton()
        self.btn6 = QPushButton()
        self.btn7 = QPushButton()
        self.btn8 = QPushButton()
        self.btnGroup.addButton(self.btn1)
        self.btnGroup.addButton(self.btn2)
        self.btnGroup.addButton(self.btn3)
        self.btnGroup.addButton(self.btn4)
        self.btnGroup.addButton(self.btn5)
        self.btnGroup.addButton(self.btn6)
        self.btnGroup.addButton(self.btn7)
        self.btnGroup.addButton(self.btn8)
        for btn in self.btnGroup.buttons():
            btn.setIcon(QIcon(QPixmap(appctxt.get_resource('icon/64.png'))))
            btn.setFixedSize(96, 96)
            # btn.clicked.connect(BTNFUNCS[btnFunc])

    def onClick(self, id):
        for btn in self.btnGroup.buttons():
            if btn is self.btnGroup.button(id):
                print(f'Button clicked: {id}')


class FileTabs(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(FileTabs, self).__init__(*args, **kwargs)
        tab = QTextEdit()
        demoFile = 'data/NC_005816.gb'
        demoText = open(appctxt.get_resource(demoFile), 'r').read()
        demoName = demoFile.split('/')[-1]
        tab.setDocumentTitle(demoName)
        tab.setText(demoText)
        tab.filePath = appctxt.get_resource(demoFile)
        self.addTab(tab, demoName)
        self.addTab(QWidget(), 'add tab')
        self.setMovable(True)
        self.setTabsClosable(True)


class PlotTabs(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(PlotTabs, self).__init__(*args, **kwargs)
        tab = QLabel()
        self.addTab(QWidget(), 'add tab')
        self.setMovable(True)
        self.setTabsClosable(True)

    def makePlotWindow(self, pic):
            image = QLabel()
            pic = QPixmap(appctxt.get_resource(pic))
            image.setPixmap(pic)
            return image


class Grid(QWidget):
    def __init__(self, *args, **kwargs):
        super(Grid, self).__init__(*args, **kwargs)
        self.PLOTDIR = appctxt.get_resource('plot')
        print(f'PLOTDIR: {self.PLOTDIR}')
        # make the widgets
        self.fileTabs = FileTabs()
        self.topPlotTabs = PlotTabs()
        self.botPlotTabs = PlotTabs()
        vizbuttons = VizButtons()
        buttonLayout = QVBoxLayout()
        # for btn in vizbuttons.btnGroup.buttons():
        for btn, fname, func in zip(vizbuttons.btnGroup.buttons(), VIZFUNCS.keys(), VIZFUNCS.values()):
            buttonLayout.addWidget(btn)
            btn.setText(fname)
            btn.clicked.connect(partial(self.runButtonFunc, btn.text()))
        buttonLayout.addStretch()
        # look into pyqtGraph for plotting at runtime
        self.demoPlot = self.topPlotTabs.makePlotWindow('plot/demoplot.png')
        self.nucplot = self.botPlotTabs.makePlotWindow('plot/nucplot.png')
        self.topPlotTabs.insertTab(0, self.demoPlot, 'demoPlot')
        self.botPlotTabs.insertTab(0, self.nucplot, 'nucPlot')
        self.topPlotTabs.setCurrentIndex(0)
        self.botPlotTabs.setCurrentIndex(0)
        layout = QGridLayout()

        layout.addLayout(buttonLayout, 0, 0, 9, 1)
        layout.addWidget(self.fileTabs, 0, 1, 9, 4)
        layout.addWidget(self.topPlotTabs, 0, 5, 4, 4)
        layout.addWidget(self.botPlotTabs, 4, 5, 4, 4)
        self.setLayout(layout)

    def runButtonFunc(self, btnFunc):
        currentFile = self.fileTabs.currentWidget().filePath
        currentFile = appctxt.get_resource(currentFile)
        filename, filetype = currentFile.split('.')
        print(f'called func: {btnFunc}')
        print(f'filename: {filename}')
        print(f'filetype: {filetype}')
        record = viz.get_seq(currentFile)
        try:
            result = VIZFUNCS[btnFunc](currentFile)
            fname = f"{btnFunc}{datetime.now().strftime('%Y%m%d_%H%M%S')}_plot.png"
            fpath = os.path.join(self.PLOTDIR, fname)
            result.savefig(fpath, transparent=True, bbox_inches='tight')
            result.clf()
            print(f'{fname} created')
            newPlot = appctxt.get_resource(fpath)
            self.botPlotTabs.insertTab(0, self.botPlotTabs.makePlotWindow(newPlot), fname.split('_')[0])
            self.botPlotTabs.setCurrentIndex(0)
        except AttributeError as e:
            print(f'record: {record}')
            print(f'func called: {VIZFUNCS[btnFunc]}')
            print(e)


class MainWindow(QMainWindow):
    def __init__(self, mainWidget):
        QMainWindow.__init__(self)
        self.setWindowTitle('BETA: app template version 0.0.1')
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('File')
        self.edit_menu = self.menu.addMenu('Edit')
        self.view_menu = self.menu.addMenu('View')
        self.help_menu = self.menu.addMenu('Help')

        def showHelp():
            helpBox = QMessageBox()
            helpBox.setText(HELP_STRING)
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
        appFont = QFont()
        appFont.setStyleStrategy(appFont.PreferAntialias)
        self.app.setFont(appFont)

    def run(self):
        self.grid = Grid()
        if DEV:
            print('show DEV things here...')
        self.mainWindow = MainWindow(self.grid)
        self.mainWindow.resize(1280, 720)
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
