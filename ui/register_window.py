from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(442, 663)
        MainWindow.setStyleSheet("background-color: rgb(10, 15, 28);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(130, 20, 181, 101))
        self.logo.setStyleSheet("")
        self.logo.setText("")
        self.logo.setObjectName("logo")
        self.title_1 = QtWidgets.QLabel(self.centralwidget)
        self.title_1.setGeometry(QtCore.QRect(140, 130, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.title_1.setFont(font)
        self.title_1.setStyleSheet("color: rgb(255, 255, 255);\n"
"background: none;")
        self.title_1.setObjectName("title_1")
        self.title_2 = QtWidgets.QLabel(self.centralwidget)
        self.title_2.setGeometry(QtCore.QRect(230, 130, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.title_2.setFont(font)
        self.title_2.setStyleSheet("color: #1E88E5;\n"
"background: none;")
        self.title_2.setObjectName("title_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 180, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"background: none;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 220, 441, 21))
        self.label_2.setStyleSheet("color: rgb(234, 234, 234);\n"
"background: none;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.user_name = QtWidgets.QLineEdit(self.centralwidget)
        self.user_name.setGeometry(QtCore.QRect(12, 270, 411, 41))
        self.user_name.setStyleSheet("background-color: #1E293B;\n"
"border: 4px solid #1E293B;\n"
"border-radius: 12px;\n"
"color: rgb(255, 255, 255);")
        self.user_name.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.user_name.setObjectName("user_name")
        self.email = QtWidgets.QLineEdit(self.centralwidget)
        self.email.setGeometry(QtCore.QRect(10, 330, 411, 41))
        self.email.setStyleSheet("background-color: #1E293B;\n"
"border: 4px solid #1E293B;\n"
"border-radius: 12px;\n"
"color: rgb(255, 255, 255);")
        self.email.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.email.setObjectName("email")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(10, 390, 411, 41))
        self.password.setStyleSheet("background-color: #1E293B;\n"
"border: 4px solid #1E293B;\n"
"border-radius: 12px;\n"
"color: rgb(255, 255, 255);")
        self.password.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.password.setObjectName("password")
        self.sec_pin = QtWidgets.QLineEdit(self.centralwidget)
        self.sec_pin.setGeometry(QtCore.QRect(10, 450, 411, 41))
        self.sec_pin.setStyleSheet("background-color: #1E293B;\n"
"border: 4px solid #1E293B;\n"
"border-radius: 12px;\n"
"color: rgb(255, 255, 255);")
        self.sec_pin.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.sec_pin.setObjectName("sec_pin")
        self.create_acc_btn = QtWidgets.QPushButton(self.centralwidget)
        self.create_acc_btn.setGeometry(QtCore.QRect(20, 520, 391, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.create_acc_btn.setFont(font)
        self.create_acc_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.create_acc_btn.setStyleSheet("background: qlineargradient(\n"
"    x1:0, y1:0, x2:1, y2:0,\n"
"    stop:0 #1E88E5,\n"
"    stop:1 #00C2FF\n"
");\n"
"color: rgb(255, 255, 255);\n"
"border: 4px solid rgb(30, 136, 229);\n"
"border-radius: 10px;")
        self.create_acc_btn.setObjectName("create_acc_btn")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 620, 231, 21))
        self.label_3.setStyleSheet("color: rgb(234, 234, 234);\n"
"background: none;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.login_page_btn = QtWidgets.QPushButton(self.centralwidget)
        self.login_page_btn.setGeometry(QtCore.QRect(200, 620, 75, 23))
        self.login_page_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_page_btn.setStyleSheet("color: rgb(30, 136, 229);\n"
"background-color: rgb(10, 15, 28);\n"
"border: 1px solid  rgb(10, 15, 28);")
        self.login_page_btn.setObjectName("login_page_btn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title_1.setText(_translate("MainWindow", "Vault"))
        self.title_2.setText(_translate("MainWindow", "Pay"))
        self.label.setText(_translate("MainWindow", "Create Your Account"))
        self.label_2.setText(_translate("MainWindow", "Join VaultPay and take control of your finances"))
        self.user_name.setPlaceholderText(_translate("MainWindow", "Username"))
        self.email.setPlaceholderText(_translate("MainWindow", "Email"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.sec_pin.setPlaceholderText(_translate("MainWindow", "Security Pin (4 or 6 digits)"))
        self.create_acc_btn.setText(_translate("MainWindow", "Create Account"))
        self.label_3.setText(_translate("MainWindow", "Already have an Account?"))
        self.login_page_btn.setText(_translate("MainWindow", "Login"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())