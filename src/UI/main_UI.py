# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_UiWindow(object):
    def setupUi(self, UiWindow):
        if not UiWindow.objectName():
            UiWindow.setObjectName(u"UiWindow")
        UiWindow.resize(310, 261)
        self.gridLayout = QGridLayout(UiWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.layoutmain = QGridLayout()
        self.layoutmain.setObjectName(u"layoutmain")
        self.calender_box = QGroupBox(UiWindow)
        self.calender_box.setObjectName(u"calender_box")
        self.verticalLayout_2 = QVBoxLayout(self.calender_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.start_date = QDateEdit(self.calender_box)
        self.start_date.setObjectName(u"start_date")
        self.start_date.setDateTime(QDateTime(QDate(2016, 1, 1), QTime(1, 1, 15)))
        self.start_date.setMaximumDate(QDate(2025, 5, 27))
        self.start_date.setMinimumDate(QDate(2016, 1, 1))

        self.verticalLayout_2.addWidget(self.start_date)

        self.end_date = QDateEdit(self.calender_box)
        self.end_date.setObjectName(u"end_date")
        self.end_date.setDateTime(QDateTime(QDate(2016, 1, 8), QTime(0, 0, 0)))
        self.end_date.setMaximumDate(QDate(2025, 5, 31))
        self.end_date.setMinimumDate(QDate(2016, 1, 7))

        self.verticalLayout_2.addWidget(self.end_date)


        self.layoutmain.addWidget(self.calender_box, 1, 0, 4, 1)

        self.weekly_monthly = QComboBox(UiWindow)
        self.weekly_monthly.addItem("")
        self.weekly_monthly.addItem("")
        self.weekly_monthly.setObjectName(u"weekly_monthly")

        self.layoutmain.addWidget(self.weekly_monthly, 3, 1, 1, 1)

        self.datalabel = QLabel(UiWindow)
        self.datalabel.setObjectName(u"datalabel")

        self.layoutmain.addWidget(self.datalabel, 2, 1, 1, 1)


        self.gridLayout.addLayout(self.layoutmain, 0, 0, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lineEdit_browse = QLineEdit(UiWindow)
        self.lineEdit_browse.setObjectName(u"lineEdit_browse")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lineEdit_browse)

        self.pushButton_browse = QPushButton(UiWindow)
        self.pushButton_browse.setObjectName(u"pushButton_browse")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.pushButton_browse)


        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)

        self.map_box = QVBoxLayout()
        self.map_box.setObjectName(u"map_box")
        self.open_map = QPushButton(UiWindow)
        self.open_map.setObjectName(u"open_map")

        self.map_box.addWidget(self.open_map)

        self.load_terrain = QPushButton(UiWindow)
        self.load_terrain.setObjectName(u"load_terrain")

        self.map_box.addWidget(self.load_terrain)

        self.load_thermal = QPushButton(UiWindow)
        self.load_thermal.setObjectName(u"load_thermal")

        self.map_box.addWidget(self.load_thermal)


        self.gridLayout.addLayout(self.map_box, 2, 0, 1, 1)


        self.retranslateUi(UiWindow)

        QMetaObject.connectSlotsByName(UiWindow)
    # setupUi

    def retranslateUi(self, UiWindow):
        UiWindow.setWindowTitle(QCoreApplication.translate("UiWindow", u"UI", None))
        self.calender_box.setTitle(QCoreApplication.translate("UiWindow", u"Choose Start/End Date", None))
        self.weekly_monthly.setItemText(0, QCoreApplication.translate("UiWindow", u"weekly", None))
        self.weekly_monthly.setItemText(1, QCoreApplication.translate("UiWindow", u"monthly", None))

        self.weekly_monthly.setPlaceholderText(QCoreApplication.translate("UiWindow", u"weekly", None))
        self.datalabel.setText(QCoreApplication.translate("UiWindow", u"Data Frequency", None))
        self.pushButton_browse.setText(QCoreApplication.translate("UiWindow", u"Browse Data Folder...", None))
        self.open_map.setText(QCoreApplication.translate("UiWindow", u"Open Map", None))
        self.load_terrain.setText(QCoreApplication.translate("UiWindow", u"Load Terrain", None))
        self.load_thermal.setText(QCoreApplication.translate("UiWindow", u"Load Temperature Data", None))
    # retranslateUi

