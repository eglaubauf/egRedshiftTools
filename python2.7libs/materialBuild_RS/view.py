# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PySide2 import QtCore, QtGui, QtWidgets


class Ui_RSMatBuilder(object):
    def setupUi(self, RSMatBuilder):
        RSMatBuilder.setObjectName("RSMatBuilder")
        RSMatBuilder.resize(286, 229)
        self.verticalLayoutWidget = QtWidgets.QWidget(RSMatBuilder)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 251, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cbx_applyMat = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.cbx_applyMat.setObjectName("cbx_applyMat")
        self.verticalLayout.addWidget(self.cbx_applyMat)
        self.cbx_context = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.cbx_context.setObjectName("cbx_context")
        self.verticalLayout.addWidget(self.cbx_context)
        self.cbx_setupOGL = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.cbx_setupOGL.setObjectName("cbx_setupOGL")
        self.verticalLayout.addWidget(self.cbx_setupOGL)
        self.cbx_useTex = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.cbx_useTex.setObjectName("cbx_useTex")
        self.verticalLayout.addWidget(self.cbx_useTex)
        self.cbx_convert = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.cbx_convert.setObjectName("cbx_convert")
        self.verticalLayout.addWidget(self.cbx_convert)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.fld_username = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.fld_username.setObjectName("fld_username")
        self.verticalLayout.addWidget(self.fld_username)
        self.buttonBox = QtWidgets.QDialogButtonBox(RSMatBuilder)
        self.buttonBox.setGeometry(QtCore.QRect(-180, 180, 379, 28))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(RSMatBuilder)
        QtCore.QMetaObject.connectSlotsByName(RSMatBuilder)

    def retranslateUi(self, RSMatBuilder):
        _translate = QtCore.QCoreApplication.translate
        RSMatBuilder.setWindowTitle(_translate("RSMatBuilder", "RS Material Builder"))
        self.cbx_applyMat.setText(_translate("RSMatBuilder", "Apply Material to Selected"))
        self.cbx_context.setText(_translate("RSMatBuilder", "Use current Context"))
        self.cbx_setupOGL.setText(_translate("RSMatBuilder", "Setup OGL"))
        self.cbx_useTex.setText(_translate("RSMatBuilder", "Use Textures"))
        self.cbx_convert.setText(_translate("RSMatBuilder", "Convert Textures to OCIO"))
        self.label.setText(_translate("RSMatBuilder", "Name (Keep Empty to Use OBJ-Name)"))
