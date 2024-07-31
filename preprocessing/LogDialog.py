# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LogDialog.ui'
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
    QHeaderView, QLabel, QSizePolicy, QTableView,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title_text = QLabel(Dialog)
        self.title_text.setObjectName(u"title_text")
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.title_text.setFont(font)

        self.verticalLayout.addWidget(self.title_text)

        self.info_text = QLabel(Dialog)
        self.info_text.setObjectName(u"info_text")

        self.verticalLayout.addWidget(self.info_text)

        self.log_table = QTableView(Dialog)
        self.log_table.setObjectName(u"log_table")

        self.verticalLayout.addWidget(self.log_table)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.title_text.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.info_text.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
    # retranslateUi

