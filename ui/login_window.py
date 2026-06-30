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
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 180, 441, 21))
        self.label_2.setStyleSheet("color: rgb(234, 234, 234);\n"
"background: none;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.user_name_or_email = QtWidgets.QLineEdit(self.centralwidget)
        self.user_name_or_email.setGeometry(QtCore.QRect(10, 290, 411, 41))
        self.user_name_or_email.setStyleSheet("background-color: #1E293B;\n"
"border: 4px solid #1E293B;\n"
"border-radius: 12px;\n"
"color: rgb(255, 255, 255);")
        self.user_name_or_email.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.user_name_or_email.setObjectName("user_name_or_email")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(10, 340, 411, 41))
        self.password.setStyleSheet("background-color: #1E293B;\n"
"border: 4px solid #1E293B;\n"
"border-radius: 12px;\n"
"color: rgb(255, 255, 255);")
        self.password.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.password.setObjectName("password")
        self.login_btn = QtWidgets.QPushButton(self.centralwidget)
        self.login_btn.setGeometry(QtCore.QRect(20, 430, 391, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.login_btn.setFont(font)
        self.login_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.login_btn.setStyleSheet("background: qlineargradient(\n"
"    x1:0, y1:0, x2:1, y2:0,\n"
"    stop:0 #1E88E5,\n"
"    stop:1 #00C2FF\n"
");\n"
"color: rgb(255, 255, 255);\n"
"border: 4px solid rgb(30, 136, 229);\n"
"border-radius: 10px;")
        self.login_btn.setObjectName("login_btn")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(90, 620, 231, 21))
        self.label_3.setStyleSheet("color: rgb(234, 234, 234);\n"
"background: none;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.register_window_btn = QtWidgets.QPushButton(self.centralwidget)
        self.register_window_btn.setGeometry(QtCore.QRect(270, 620, 75, 23))
        self.register_window_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.register_window_btn.setStyleSheet("color: rgb(30, 136, 229);\n"
"background-color: rgb(10, 15, 28);\n"
"border: 1px solid  rgb(10, 15, 28);")
        self.register_window_btn.setObjectName("register_window_btn")
        self.remember_me_chck_box = QtWidgets.QRadioButton(self.centralwidget)
        self.remember_me_chck_box.setGeometry(QtCore.QRect(30, 400, 111, 17))
        self.remember_me_chck_box.setStyleSheet("color: rgb(255, 255, 255);")
        self.remember_me_chck_box.setObjectName("remember_me_chck_box")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 220, 401, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"background: none;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title_1.setText(_translate("MainWindow", "Vault"))
        self.title_2.setText(_translate("MainWindow", "Pay"))
        self.label_2.setText(_translate("MainWindow", "Secure. Simple. Smart."))
        self.user_name_or_email.setPlaceholderText(_translate("MainWindow", "Username or Email"))
        self.password.setPlaceholderText(_translate("MainWindow", "Password"))
        self.login_btn.setText(_translate("MainWindow", "Login"))
        self.label_3.setText(_translate("MainWindow", "Don\'t have an Account?"))
        self.register_window_btn.setText(_translate("MainWindow", "Register"))
        self.remember_me_chck_box.setText(_translate("MainWindow", "Remember Me"))
        self.label.setText(_translate("MainWindow", "Welcome Back"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())