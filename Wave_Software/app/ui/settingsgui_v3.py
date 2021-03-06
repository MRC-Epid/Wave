# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Cobin\Documents\GitHub\Wave\Wave_Software\tools\\..\app\ui\settings_v3.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_settingsWindow(object):
    def setupUi(self, settingsWindow):
        settingsWindow.setObjectName("settingsWindow")
        settingsWindow.resize(650, 705)
        settingsWindow.setMinimumSize(QtCore.QSize(650, 705))
        settingsWindow.setMaximumSize(QtCore.QSize(650, 730))
        self.centralwidget = QtWidgets.QWidget(settingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(9, 9, 631, 670))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(631, 670))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_5.setMaximumSize(QtCore.QSize(16777215, 60))
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox.setMinimumSize(QtCore.QSize(180, 0))
        self.comboBox.setEditable(False)
        self.comboBox.setMaxVisibleItems(20)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_9 = QtWidgets.QLabel(self.groupBox_5)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_2.addWidget(self.label_9)
        self.templateNameLineEdit = QtWidgets.QLineEdit(self.groupBox_5)
        self.templateNameLineEdit.setObjectName("templateNameLineEdit")
        self.horizontalLayout_2.addWidget(self.templateNameLineEdit)
        self.addTemplatePushButton = QtWidgets.QPushButton(self.groupBox_5)
        self.addTemplatePushButton.setObjectName("addTemplatePushButton")
        self.horizontalLayout_2.addWidget(self.addTemplatePushButton)
        self.removeTemplatePushButton = QtWidgets.QPushButton(self.groupBox_5)
        self.removeTemplatePushButton.setObjectName("removeTemplatePushButton")
        self.horizontalLayout_2.addWidget(self.removeTemplatePushButton)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.groupBox_5)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 60))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.processingepochLabel = QtWidgets.QLabel(self.groupBox_3)
        self.processingepochLabel.setObjectName("processingepochLabel")
        self.gridLayout_3.addWidget(self.processingepochLabel, 0, 0, 1, 1)
        self.lineEditProcessEpoch = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditProcessEpoch.setObjectName("lineEditProcessEpoch")
        self.gridLayout_3.addWidget(self.lineEditProcessEpoch, 0, 2, 1, 1)
        self.noisecutoffLabel = QtWidgets.QLabel(self.groupBox_3)
        self.noisecutoffLabel.setObjectName("noisecutoffLabel")
        self.gridLayout_3.addWidget(self.noisecutoffLabel, 0, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 3, 1, 1)
        self.lineEditNoiseCutoff = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditNoiseCutoff.setObjectName("lineEditNoiseCutoff")
        self.gridLayout_3.addWidget(self.lineEditNoiseCutoff, 0, 5, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 6, 1, 1)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setMaximumSize(QtCore.QSize(16777215, 150))
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame = QtWidgets.QFrame(self.groupBox_4)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 206))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plotting_enabled = QtWidgets.QRadioButton(self.frame)
        self.plotting_enabled.setChecked(True)
        self.plotting_enabled.setObjectName("plotting_enabled")
        self.buttonGroup = QtWidgets.QButtonGroup(settingsWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.plotting_enabled)
        self.verticalLayout.addWidget(self.plotting_enabled)
        self.plotting_disabled = QtWidgets.QRadioButton(self.frame)
        self.plotting_disabled.setObjectName("plotting_disabled")
        self.buttonGroup.addButton(self.plotting_disabled)
        self.verticalLayout.addWidget(self.plotting_disabled)
        self.gridLayout_4.addWidget(self.frame, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.groupBox_4)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.outputplotlistlabel = QtWidgets.QLabel(self.frame_2)
        self.outputplotlistlabel.setObjectName("outputplotlistlabel")
        self.verticalLayout_2.addWidget(self.outputplotlistlabel)
        self.listWidget = QtWidgets.QListWidget(self.frame_2)
        self.listWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.verticalLayout_2.addWidget(self.listWidget)
        self.gridLayout_4.addWidget(self.frame_2, 0, 1, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.groupBox_4)
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 320))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 320))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.spinBox_7 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_7.setMaximum(999999)
        self.spinBox_7.setProperty("value", 150)
        self.spinBox_7.setObjectName("spinBox_7")
        self.gridLayout_5.addWidget(self.spinBox_7, 3, 1, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_2.setMaximum(999999)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout_5.addWidget(self.spinBox_2, 1, 1, 1, 1)
        self.spinBox_11 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_11.setMaximum(999999)
        self.spinBox_11.setProperty("value", 1000)
        self.spinBox_11.setObjectName("spinBox_11")
        self.gridLayout_5.addWidget(self.spinBox_11, 4, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 0, 2, 1, 1)
        self.spinBox_8 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_8.setMaximum(999999)
        self.spinBox_8.setProperty("value", 300)
        self.spinBox_8.setObjectName("spinBox_8")
        self.gridLayout_5.addWidget(self.spinBox_8, 3, 2, 1, 1)
        self.spinBox_6 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_6.setMaximum(999999)
        self.spinBox_6.setProperty("value", 5)
        self.spinBox_6.setObjectName("spinBox_6")
        self.gridLayout_5.addWidget(self.spinBox_6, 2, 3, 1, 1)
        self.spinBox_15 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_15.setMinimum(0)
        self.spinBox_15.setMaximum(999999)
        self.spinBox_15.setProperty("value", 1000)
        self.spinBox_15.setObjectName("spinBox_15")
        self.gridLayout_5.addWidget(self.spinBox_15, 5, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        self.label.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 1, 1, 1)
        self.spinBox_4 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_4.setMaximum(999999)
        self.spinBox_4.setProperty("value", 5)
        self.spinBox_4.setObjectName("spinBox_4")
        self.gridLayout_5.addWidget(self.spinBox_4, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 0, 3, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox.setMaximum(999999)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout_5.addWidget(self.spinBox, 1, 3, 1, 1)
        self.spinBox_9 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_9.setMinimum(0)
        self.spinBox_9.setMaximum(999999)
        self.spinBox_9.setProperty("value", 10)
        self.spinBox_9.setObjectName("spinBox_9")
        self.gridLayout_5.addWidget(self.spinBox_9, 3, 3, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem3, 0, 0, 1, 1)
        self.spinBox_13 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_13.setMaximumSize(QtCore.QSize(16777215, 30))
        self.spinBox_13.setMaximum(999999)
        self.spinBox_13.setProperty("value", 1000)
        self.spinBox_13.setObjectName("spinBox_13")
        self.gridLayout_5.addWidget(self.spinBox_13, 5, 1, 1, 1)
        self.spinBox_10 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_10.setMaximum(999999)
        self.spinBox_10.setProperty("value", 300)
        self.spinBox_10.setObjectName("spinBox_10")
        self.gridLayout_5.addWidget(self.spinBox_10, 4, 1, 1, 1)
        self.spinBox_12 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_12.setMinimum(0)
        self.spinBox_12.setMaximum(999999)
        self.spinBox_12.setProperty("value", 100)
        self.spinBox_12.setObjectName("spinBox_12")
        self.gridLayout_5.addWidget(self.spinBox_12, 4, 3, 1, 1)
        self.spinBox_5 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_5.setMaximum(999999)
        self.spinBox_5.setProperty("value", 150)
        self.spinBox_5.setObjectName("spinBox_5")
        self.gridLayout_5.addWidget(self.spinBox_5, 2, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout_5.addWidget(self.label_7, 4, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 5, 0, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_3.setMaximum(999999)
        self.spinBox_3.setProperty("value", 5)
        self.spinBox_3.setObjectName("spinBox_3")
        self.gridLayout_5.addWidget(self.spinBox_3, 1, 2, 1, 1)
        self.spinBox_14 = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox_14.setMaximum(999999)
        self.spinBox_14.setProperty("value", 5000)
        self.spinBox_14.setObjectName("spinBox_14")
        self.gridLayout_5.addWidget(self.spinBox_14, 5, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_5.addWidget(self.label_6, 3, 0, 1, 1)
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.groupBox)
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_6.setMinimumSize(QtCore.QSize(0, 50))
        self.groupBox_6.setMaximumSize(QtCore.QSize(16777215, 50))
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(285, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.cancelsettingsPush = QtWidgets.QPushButton(self.groupBox_6)
        self.cancelsettingsPush.setObjectName("cancelsettingsPush")
        self.horizontalLayout.addWidget(self.cancelsettingsPush)
        self.defaultsettingsPush = QtWidgets.QPushButton(self.groupBox_6)
        self.defaultsettingsPush.setObjectName("defaultsettingsPush")
        self.horizontalLayout.addWidget(self.defaultsettingsPush)
        self.submitsettingsPush = QtWidgets.QPushButton(self.groupBox_6)
        self.submitsettingsPush.setObjectName("submitsettingsPush")
        self.horizontalLayout.addWidget(self.submitsettingsPush)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.groupBox_6)
        settingsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(settingsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 650, 21))
        self.menubar.setObjectName("menubar")
        settingsWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(settingsWindow)
        self.statusbar.setObjectName("statusbar")
        settingsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(settingsWindow)
        self.cancelsettingsPush.clicked.connect(settingsWindow.close)
        self.submitsettingsPush.clicked.connect(settingsWindow.submitsettings)
        self.plotting_disabled.clicked.connect(self.frame_2.hide)
        self.plotting_enabled.clicked.connect(self.frame_2.show)
        QtCore.QMetaObject.connectSlotsByName(settingsWindow)

    def retranslateUi(self, settingsWindow):
        _translate = QtCore.QCoreApplication.translate
        settingsWindow.setWindowTitle(_translate("settingsWindow", "Wave: Settings Menu"))
        self.groupBox_2.setTitle(_translate("settingsWindow", "Advanced Settings"))
        self.groupBox_5.setTitle(_translate("settingsWindow", "Templates"))
        self.comboBox.setItemText(0, _translate("settingsWindow", "Default"))
        self.label_9.setText(_translate("settingsWindow", "Template Options:"))
        self.addTemplatePushButton.setText(_translate("settingsWindow", "Add"))
        self.removeTemplatePushButton.setText(_translate("settingsWindow", "Remove"))
        self.processingepochLabel.setText(_translate("settingsWindow", "Processing Epoch (sec)"))
        self.lineEditProcessEpoch.setText(_translate("settingsWindow", "5"))
        self.noisecutoffLabel.setText(_translate("settingsWindow", "Noise Cutoff (mg)"))
        self.lineEditNoiseCutoff.setText(_translate("settingsWindow", "13"))
        self.groupBox_4.setTitle(_translate("settingsWindow", "Plotting"))
        self.plotting_enabled.setText(_translate("settingsWindow", "Enabled"))
        self.plotting_disabled.setText(_translate("settingsWindow", "Disabled"))
        self.outputplotlistlabel.setText(_translate("settingsWindow", "Plot Epoch (mins)"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("settingsWindow", "1"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("settingsWindow", "Thresholds"))
        self.label_2.setText(_translate("settingsWindow", "Last Section Point"))
        self.label.setText(_translate("settingsWindow", "First Section Point"))
        self.label_3.setText(_translate("settingsWindow", "Increment"))
        self.label_7.setText(_translate("settingsWindow", "Fourth Section"))
        self.label_5.setText(_translate("settingsWindow", "Second Section"))
        self.label_8.setText(_translate("settingsWindow", "Fifth Section"))
        self.label_4.setText(_translate("settingsWindow", "First Section"))
        self.label_6.setText(_translate("settingsWindow", "Third Section"))
        self.cancelsettingsPush.setText(_translate("settingsWindow", "Cancel"))
        self.defaultsettingsPush.setText(_translate("settingsWindow", "Save"))
        self.submitsettingsPush.setText(_translate("settingsWindow", "Submit"))
