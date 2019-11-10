# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_templates/settings.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(211, 87)
        self.widget = QtWidgets.QWidget(Settings)
        self.widget.setGeometry(QtCore.QRect(0, 0, 207, 84))
        self.widget.setObjectName("widget")
        self.main_layout = QtWidgets.QVBoxLayout(self.widget)
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setObjectName("main_layout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.auto_2 = QtWidgets.QCheckBox(self.widget)
        self.auto_2.setObjectName("auto_2")
        self.horizontalLayout_3.addWidget(self.auto_2)
        self.font_button = QtWidgets.QPushButton(self.widget)
        self.font_button.setObjectName("font_button")
        self.horizontalLayout_3.addWidget(self.font_button)
        self.main_layout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.tab_width = QtWidgets.QSpinBox(self.widget)
        self.tab_width.setMinimum(1)
        self.tab_width.setMaximum(12)
        self.tab_width.setObjectName("tab_width")
        self.horizontalLayout.addWidget(self.tab_width)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabs = QtWidgets.QRadioButton(self.widget)
        self.tabs.setObjectName("tabs")
        self.horizontalLayout_2.addWidget(self.tabs)
        self.spaces = QtWidgets.QRadioButton(self.widget)
        self.spaces.setObjectName("spaces")
        self.horizontalLayout_2.addWidget(self.spaces)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.langs = QtWidgets.QComboBox(self.widget)
        self.langs.setObjectName("langs")
        self.verticalLayout.addWidget(self.langs)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.main_layout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Form"))
        self.auto_2.setText(_translate("Settings", "Auto Indent"))
        self.font_button.setText(_translate("Settings", "Font\'s settings"))
        self.label_2.setText(_translate("Settings", "Tab Width"))
        self.tabs.setText(_translate("Settings", "Tabs"))
        self.spaces.setText(_translate("Settings", "Spaces"))
        self.label.setText(_translate("Settings", "Default language"))


