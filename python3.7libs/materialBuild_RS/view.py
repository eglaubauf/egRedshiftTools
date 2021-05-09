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
        RSMatBuilder.resize(327, 389)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RSMatBuilder.sizePolicy().hasHeightForWidth())
        RSMatBuilder.setSizePolicy(sizePolicy)
        RSMatBuilder.setMouseTracking(True)
        self.gridLayout = QtWidgets.QGridLayout(RSMatBuilder)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cbx_applyMat = QtWidgets.QCheckBox(RSMatBuilder)
        self.cbx_applyMat.setObjectName("cbx_applyMat")
        self.verticalLayout.addWidget(self.cbx_applyMat)
        self.cbx_context = QtWidgets.QCheckBox(RSMatBuilder)
        self.cbx_context.setObjectName("cbx_context")
        self.verticalLayout.addWidget(self.cbx_context)
        self.cbx_setupOGL = QtWidgets.QCheckBox(RSMatBuilder)
        self.cbx_setupOGL.setObjectName("cbx_setupOGL")
        self.verticalLayout.addWidget(self.cbx_setupOGL)
        self.cbx_useTex = QtWidgets.QCheckBox(RSMatBuilder)
        self.cbx_useTex.setObjectName("cbx_useTex")
        self.verticalLayout.addWidget(self.cbx_useTex)
        self.cbx_convert = QtWidgets.QCheckBox(RSMatBuilder)
        self.cbx_convert.setObjectName("cbx_convert")
        self.verticalLayout.addWidget(self.cbx_convert)
        self.cbx_ccDiffuse = QtWidgets.QCheckBox(RSMatBuilder)
        self.cbx_ccDiffuse.setObjectName("cbx_ccDiffuse")
        self.verticalLayout.addWidget(self.cbx_ccDiffuse)
        self.cbx_diffLinear = QtWidgets.QCheckBox(RSMatBuilder)
        self.cbx_diffLinear.setObjectName("cbx_diffLinear")
        self.verticalLayout.addWidget(self.cbx_diffLinear)
        self.cbx_heightDisp = QtWidgets.QCheckBox(RSMatBuilder)
        self.cbx_heightDisp.setObjectName("cbx_heightDisp")
        self.verticalLayout.addWidget(self.cbx_heightDisp)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(RSMatBuilder)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.fld_username = QtWidgets.QLineEdit(RSMatBuilder)
        self.fld_username.setObjectName("fld_username")
        self.verticalLayout.addWidget(self.fld_username)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(RSMatBuilder)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

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
        self.cbx_ccDiffuse.setText(_translate("RSMatBuilder", "ColorCorrection on Diffuse"))
        self.cbx_diffLinear.setText(_translate("RSMatBuilder", "Diffuse is Linear"))
        self.cbx_heightDisp.setText(_translate("RSMatBuilder", "Height is Displacement"))
        self.label.setText(_translate("RSMatBuilder", "Name (Keep Empty to Use OBJ-Name)"))
