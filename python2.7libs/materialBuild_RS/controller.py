#####################################
#           LICENSE                 #
#####################################
#
# Copyright (C) 2020  Elmar Glaubauf
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import hou

from PySide2 import QtWidgets, QtCore

import materialBuild_RS.core as core
import materialBuild_RS.view as view

# Where is this script?
# SCRIPT_LOC = os.path.split(__file__)[0]

reload(core)
reload(view)
'''
Open with

import materialBuild_RS.controller as matBuildRS
reload(matBuildRS)
matBuildRS.open()

'''

develop = False
tmpWindow = None

def open(develop=False):

    if develop:
        reload(core)
        reload(view)
    try:
        tmpWindow.close()
    except:
        pass

    tmpWindow = Controller()
    tmpWindow.show()


class Controller(QtWidgets.QDialog, view.Ui_RSMatBuilder):

    def __init__(self, parent=hou.qt.mainWindow()):
        super(Controller, self).__init__(parent)

        self.setupUi(self)
        self.configureUiStates()

        # Set Houdini Style to Window
        self.setProperty("houdiniStyle", True)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.core = core.Core()
        self.createConnections()

    # linking Buttons to Functions
    def createConnections(self):

        self.cbx_applyMat.toggled.connect(self.setApplyMat)
        self.cbx_context.toggled.connect(self.setContext)
        self.cbx_convert.toggled.connect(self.setConvert)
        self.cbx_setupOGL.toggled.connect(self.setOGL)
        self.cbx_useTex.toggled.connect(self.useTex)
        self.buttonBox.rejected.connect(self.destroy)
        self.buttonBox.accepted.connect(self.execute)
        self.fld_username.textChanged.connect(self.setName)

    def configureUiStates(self):
        self.cbx_convert.setDisabled(True)

    def setApplyMat(self):
        if self.cbx_applyMat.isChecked():
            self.core.setApplyMat(True)
        else:
            self.core.setApplyMat(False)

    def setContext(self):
        if self.cbx_context.isChecked():
            self.core.setContext(True)
        else:
            self.core.setContext(False)

    def setOGL(self):
        if self.cbx_setupOGL.isChecked():
            self.core.setOGL(True)
        else:
            self.core.setOGL(False)

    def setName(self):
        self.core.setName(self.fld_username.text())

    def useTex(self):
        if not self.cbx_useTex.isChecked():
            self.cbx_convert.setDisabled(True)
            self.cbx_convert.setChecked(False)
            self.setConvert()
        else:
            self.cbx_convert.setDisabled(False)

        self.core.setUseTex(self.cbx_useTex.isChecked())

    def setConvert(self, ):
        if self.cbx_convert.isChecked():
            self.core.setConvert(True)
        else:
            self.core.setConvert(False)

    # Execute Material Creation
    def execute(self):
        self.core.createMaterial()
        # if count == 0:
        #     hou.ui.displayMessage('An error occured during Material Creation - Please Check Materials/Textures', buttons=('Ok',))
        #     return
        # message = str(count) + ' Materials created succesfully'
        # hou.ui.displayMessage(message, buttons=('Ok',))
        self.destroy()
