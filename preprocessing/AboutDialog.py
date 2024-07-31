# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AboutDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QSizePolicy, QTabWidget,
    QTextBrowser, QToolButton, QVBoxLayout, QWidget)
from preprocessing import icons_and_img_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(563, 474)
        Dialog.setStyleSheet(u"QToolbutton {\n"
"	background = transparent\n"
"}")
        Dialog.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.header_layout = QHBoxLayout()
        self.header_layout.setObjectName(u"header_layout")
        self.logo_btn = QToolButton(Dialog)
        self.logo_btn.setObjectName(u"logo_btn")
        self.logo_btn.setStyleSheet(u"background: transparent;")
        icon = QIcon()
        icon.addFile(u":/logo/logo.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.logo_btn.setIcon(icon)
        self.logo_btn.setIconSize(QSize(80, 80))

        self.header_layout.addWidget(self.logo_btn)

        self.copyright_layout = QVBoxLayout()
        self.copyright_layout.setObjectName(u"copyright_layout")
        self.name_lbl = QLabel(Dialog)
        self.name_lbl.setObjectName(u"name_lbl")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.name_lbl.setFont(font)
        self.name_lbl.setAlignment(Qt.AlignCenter)

        self.copyright_layout.addWidget(self.name_lbl)

        self.version_lbl = QLabel(Dialog)
        self.version_lbl.setObjectName(u"version_lbl")
        self.version_lbl.setAlignment(Qt.AlignCenter)

        self.copyright_layout.addWidget(self.version_lbl)

        self.copyright_lbl = QLabel(Dialog)
        self.copyright_lbl.setObjectName(u"copyright_lbl")
        font1 = QFont()
        font1.setBold(True)
        self.copyright_lbl.setFont(font1)
        self.copyright_lbl.setAlignment(Qt.AlignCenter)

        self.copyright_layout.addWidget(self.copyright_lbl)


        self.header_layout.addLayout(self.copyright_layout)


        self.verticalLayout_2.addLayout(self.header_layout)

        self.info_laout = QTabWidget(Dialog)
        self.info_laout.setObjectName(u"info_laout")
        self.license_tab = QWidget()
        self.license_tab.setObjectName(u"license_tab")
        self.verticalLayout = QVBoxLayout(self.license_tab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.license_text = QTextBrowser(self.license_tab)
        self.license_text.setObjectName(u"license_text")

        self.verticalLayout.addWidget(self.license_text)

        self.info_laout.addTab(self.license_tab, "")
        self.os_tab = QWidget()
        self.os_tab.setObjectName(u"os_tab")
        self.verticalLayout_3 = QVBoxLayout(self.os_tab)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.os_text = QTextBrowser(self.os_tab)
        self.os_text.setObjectName(u"os_text")

        self.verticalLayout_3.addWidget(self.os_text)

        self.info_laout.addTab(self.os_tab, "")

        self.verticalLayout_2.addWidget(self.info_laout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close|QDialogButtonBox.Help)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.info_laout.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"About web-rMKL preprocessing", None))
        self.logo_btn.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.name_lbl.setText(QCoreApplication.translate("Dialog", u"web-rMKL preprocessing tool", None))
        self.version_lbl.setText(QCoreApplication.translate("Dialog", u"version 2.0", None))
        self.copyright_lbl.setText(QCoreApplication.translate("Dialog", u"Copyright \u00a9 2023 University of T\u00fcbingen, Nicolas Kersten", None))
        self.info_laout.setTabText(self.info_laout.indexOf(self.license_tab), QCoreApplication.translate("Dialog", u"License", None))
        self.info_laout.setTabText(self.info_laout.indexOf(self.os_tab), QCoreApplication.translate("Dialog", u"Included open-source software", None))
    # retranslateUi

