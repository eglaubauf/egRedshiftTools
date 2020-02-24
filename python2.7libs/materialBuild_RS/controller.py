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
        self.configure_uistates()

        # Set Houdini Style to Window
        self.setProperty("houdiniStyle", True)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.core = core.Core()
        self.create_connections()

    # linking Buttons to Functions
    def create_connections(self):

        self.cbx_applyMat.toggled.connect(self.set_apply_mat)
        self.cbx_context.toggled.connect(self.set_context)
        self.cbx_convert.toggled.connect(self.set_convert)
        self.cbx_setupOGL.toggled.connect(self.set_ogl)
        self.cbx_useTex.toggled.connect(self.use_tex)
        self.buttonBox.rejected.connect(self.destroy)
        self.buttonBox.accepted.connect(self.execute)
        self.fld_username.textChanged.connect(self.set_name)

    def configure_uistates(self):
        self.cbx_convert.setDisabled(True)

    def set_apply_mat(self):
        if self.cbx_applyMat.isChecked():
            self.core.set_apply_mat(True)
        else:
            self.core.set_apply_mat(False)

    def set_context(self):
        if self.cbx_context.isChecked():
            self.core.set_context(True)
        else:
            self.core.set_context(False)

    def set_ogl(self):
        if self.cbx_setupOGL.isChecked():
            self.core.set_ogl(True)
        else:
            self.core.set_ogl(False)

    def set_name(self):
        self.core.set_name(self.fld_username.text())

    def use_tex(self):
        if not self.cbx_useTex.isChecked():
            self.cbx_convert.setDisabled(True)
            self.cbx_convert.setChecked(False)
            self.set_convert()
        else:
            self.cbx_convert.setDisabled(False)

        self.core.set_use_tex(self.cbx_useTex.isChecked())

    def set_convert(self):
        if self.cbx_convert.isChecked():
            self.core.set_convert(True)
        else:
            self.core.set_convert(False)

    # Execute Material Creation
    def execute(self):
        self.core.create_material()
        self.destroy()
