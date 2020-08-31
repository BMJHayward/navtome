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

def getNumber(func, file):
    quid = QInputDialog()
    input, ok = quid.getInt(quid, 'How many?', 'Enter number > 0', 1, 1, 100, 1)
    if ok:
        return func(input, file)
    else:
        return 1

def getStringDist(func, file):
    quid = QInputDialog()
    input, ok = quid.getText(quid, 'Enter nuc/pep', 'type or paste your sequence here')
    if ok and input:
        return viz.calcDist(func, input, file)
    else:
        return 'NOT OK'

def funcHolder(func1, func2, *args):
    return func1(func2, *args)

def makePlotWindow(pic):
        image = QLabel()
        pic = QPixmap(appctxt.get_resource(pic))
        image.setPixmap(pic)
        return image

VIZFUNCS = {
    'nucdist': partial(viz.nucleotide_distribution, 3),
    'pepdist': partial(viz.peptide_distribution, 1),
    'nucNdist': partial(getNumber, viz.nucleotide_distribution),
    'pepNdist': partial(getNumber, viz.peptide_distribution),
    'linerec': partial(viz.plot_graphic_record, 'linear'),
    'circrec': partial(viz.plot_graphic_record, 'circular'),
    'nucHeatMap': partial(getNumber, viz.nucSimPlot),
    'pepHeatMap': partial(getNumber, viz.pepSimPlot),
    }


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

    def onClick(self, id):
        for btn in self.btnGroup.buttons():
            if btn is self.btnGroup.button(id):
                print(f'Button clicked: {id}')


class InputForm(QInputDialog):
    def __init__(self, inputType=int, parent=None):
        super(InputForm, self).__init__(parent)
        # Create widgets
        class NucSet(set):
            ab = 'acgit'
        class PepSet(set):
            ab = 'acdefghiklmnpqrstvwybxzjuo'

        typeMessages = {
                int: 'please enter a whole number greater than 0',
                str: 'please enter any combination of alphanumeric characters',
                NucSet: f'please enter any combination of {NucSet.ab}',
                PepSet: f'please enter any combination of {PepSet.ab}'
                }

        self.message = QTextLabel(typeMessages[inputType])
        self.edit = QLineEdit('Input here')
        self.okbutton = QPushButton('Ok')
        self.cancelbutton = QPushButton('Cancel')
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.message)
        layout.addWidget(self.edit)
        layout.addWidget(self.okbutton)
        layout.addWidget(self.cancelbutton)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)
    @Signal
    def sendInput(self):
        print(f'Sent: {self.edit.text()}')


class FileTabs(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(FileTabs, self).__init__(*args, **kwargs)
        # tb = self.tabBar()
        tab = QTextEdit()
        demoFile = 'data/NC_005816.gb'
        demoText = open(appctxt.get_resource(demoFile), 'r').read()
        demoName = demoFile.split('/')[-1]
        tab.setDocumentTitle(demoName)
        tab.setText(demoText)
        tab.filePath = appctxt.get_resource(demoFile)
        self.addTab(tab, demoName)
        newTabBtn = QTextEdit()
        newTabBtn.setDocumentTitle('New tab')
        self.addTab(newTabBtn, 'New tab')
        self.setMovable(False)
        self.setTabsClosable(True)
        self.currentChanged.connect(self.insertNew)

    def insertNew(self):
        print(f'currentIndex: {self.currentIndex()}')
        print(f'count: {self.count()}')
        curIdx = self.currentIndex()
        if curIdx == self.count() - 1:
            newFile = QFileDialog.getOpenFileName(parent=self, caption='Open file', dir='.')[0]
            print(f'newFile: {newFile}')
            newName = newFile.split('/')[-1]
            newText = open(appctxt.get_resource(newFile), 'r').read()
            newTab = QTextEdit()
            newTab.setDocumentTitle('newName')
            newTab.setText(newText)
            newTab.filePath = appctxt.get_resource(newFile)
            self.insertTab(0, newTab, newName)
            self.setCurrentIndex(0)
        else: pass


class PlotView(QGraphicsView):
    def __init__(self, pic):
        super(PlotView, self).__init__()
        '''
        1 create a view
        2 create a scene
        3 add scene to view
        4 create QGrapicsPixmap with plot
        5 add it to view with .addItem()
        '''
        self._scene = QGraphicsScene(self)
        self.pic = QPixmap(appctxt.get_resource(pic))
        self.picItem = QGraphicsPixmapItem(self.pic)
        self._scene.addItem(self.picItem)
        self.setScene(self._scene)
        self.setDragMode(QGraphicsView.ScrollHandDrag)


# TODO: create parent class for PlotTabs and FileTabs
class PlotTabs(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(PlotTabs, self).__init__(*args, **kwargs)
        tab = QLabel()
        self.addTab(QWidget(), 'add tab')
        self.setMovable(True)
        self.setTabsClosable(True)
        self.currentChanged.connect(self.insertNew)

    def makePlotWindow(self, pic):
            image = QLabel()
            pic = QPixmap(appctxt.get_resource(pic))
            image.setPixmap(pic)
            return image

    def insertNew(self):
        print(f'currentIndex: {self.currentIndex()}')
        print(f'count: {self.count()}')
        curIdx = self.currentIndex()
        PLOTDIR = appctxt.get_resource('plot')
        if curIdx == self.count() - 1:
            newFile = QFileDialog.getOpenFileName(parent=self, caption='Open file', dir=PLOTDIR)[0]
            print(f'newFile: {newFile}')
            newName = newFile.split('/')[-1]
            PlotView(newFile)
            self.insertTab(0, PlotView(newFile), newName)
            self.setCurrentIndex(0)
        else: pass


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
        for btn, fname, func in zip(vizbuttons.btnGroup.buttons(), VIZFUNCS.keys(), VIZFUNCS.values()):
            buttonLayout.addWidget(btn)
            btn.setText(fname)
            btn.clicked.connect(partial(self.runButtonFunc, btn.text()))
        buttonLayout.addStretch()
        # look into pyqtGraph for plotting at runtime
        self.demoplot = PlotView('plot/demoplot.png')
        self.nucplot = PlotView('plot/nucplot.png')
        self.topPlotTabs.insertTab(0, self.demoplot, 'demoplot')
        self.botPlotTabs.insertTab(0, self.nucplot, 'nucPlot')
        self.topPlotTabs.setCurrentIndex(0)
        self.botPlotTabs.setCurrentIndex(0)
        vertSplit = QSplitter(self)
        horiSplit = QSplitter(vertSplit)
        horiSplit.setOrientation(Qt.Vertical)
        horiSplit.addWidget(self.topPlotTabs)
        horiSplit.addWidget(self.botPlotTabs)
        vertSplit.addWidget(self.fileTabs)
        vertSplit.addWidget(horiSplit)
        layout = QGridLayout()
        layout.addLayout(buttonLayout, 0, 0, 9, 1)
        layout.addWidget(vertSplit, 0, 1, 9, 4)
        self.setLayout(layout)

    def runButtonFunc(self, btnFunc):
        currentFile = self.fileTabs.currentWidget().filePath
        currentFile = appctxt.get_resource(currentFile)
        filename, filetype = currentFile.split('.')
        print(f'called func: {btnFunc}')
        print(f'filename: {filename}')
        print(f'filetype: {filetype}')
        try:
            result = VIZFUNCS[btnFunc](currentFile)
            if type(result) == None: return
            fname = f"{btnFunc}{datetime.now().strftime('%Y%m%d_%H%M%S')}_plot.png"
            fpath = os.path.join(self.PLOTDIR, fname)
            result.savefig(fpath, transparent=True, bbox_inches='tight')
            result.clf()
            print(f'{fname} created')
            newPlot = appctxt.get_resource(fpath)
            self.botPlotTabs.insertTab(0, PlotView(newPlot), fname.split('_')[0])
            self.botPlotTabs.setCurrentIndex(0)
        except AttributeError as e:
            record = viz.get_seq(currentFile)
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

        def openFile():
            grid = self.centralWidget()
            tabCount = grid.fileTabs.count()
            grid.fileTabs.setCurrentIndex(tabCount - 1)
            grid.fileTabs.insertNew()

        def openPlot():
            grid = self.centralWidget()
            plotPath = appctxt.get_resource('plot')
            newFile = QFileDialog.getOpenFileName(parent=self, caption='Open file', dir=plotPath)[0]
            grid.botPlotTabs.insertTab(0, PlotView(newFile), newFile.split('_')[0])
            grid.botPlotTabs.setCurrentIndex(0)

        def openPlotDir():
            import os
            import platform
            import subprocess
            def open_file(path):
                if platform.system() == "Windows":
                    os.startfile(path)
                elif platform.system() == "Darwin":
                    subprocess.Popen(["open", path])
                else:
                    subprocess.Popen(["xdg-open", path])
            open_file(appctxt.get_resource('plot'))

        def showHelp():
            helpBox = QMessageBox()
            helpBox.setText(HELP_STRING)
            helpButton = QPushButton('OK')
            helpBox.setDefaultButton(helpButton)
            helpBox.exec_()

        # actions
        plot_action = QAction('Open plot', self)
        plot_action.setStatusTip('Open a previous plot')
        plot_action.triggered.connect(openPlot)
        plot_action.setShortcut('Ctrl+L')
        self.file_menu.addAction(plot_action)
        file_action = QAction('Open file', self)
        file_action.setStatusTip('Open a new sequence file')
        file_action.triggered.connect(openFile)
        file_action.setShortcut('Ctrl+O')
        self.file_menu.addAction(file_action)
        plotdir_action = QAction('Open plot folder', self)
        plotdir_action.setStatusTip('Open folder containing all your plots')
        plotdir_action.triggered.connect(openPlotDir)
        plotdir_action.setShortcut('Ctrl+Shift+P')
        self.file_menu.addAction(plotdir_action)
        help_action = QAction('How to use this program', self)
        help_action.setStatusTip('How to use this program')
        help_action.triggered.connect(showHelp)
        self.help_menu.addAction(help_action)
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(exit_action)
        self.setCentralWidget(mainWidget)
        # self.setWindowState(Qt.WindowMaximized)

    def closeEvent(self, event):
        if DEV: event.accept()

        # TODO: add confirmation/cleanup dialogue here
        if True:
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
