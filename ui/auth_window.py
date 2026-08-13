from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QInputDialog,
)

from services.account_service import AccountService
from services.finance_service import FinanceService
from ui.main_window import VaultPayMainWindow


class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.account_service = AccountService()
        self.setWindowTitle("VaultPay")
        self.resize(440, 680)
        self.setStyleSheet(
            """
            QMainWindow { background: #0A0F1C; }
            QWidget { background: #0A0F1C; color: #F8FAFC; }
            QLabel { color: #F8FAFC; }
            QLineEdit {
                background: #1E293B; border: 1px solid #334155; border-radius: 10px;
                color: white; padding: 10px 12px; font-size: 14px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1E88E5, stop:1 #00C2FF);
                border: none; border-radius: 10px; color: white; font-weight: bold; padding: 12px;
            }
            QPushButton:hover { opacity: 0.95; }
            QPushButton.secondary {
                background: transparent; border: 1px solid #1E88E5; color: #7DD3FC; padding: 8px 12px;
            }
            """
        )

        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        self.login_widget = self._build_login_form()
        self.register_widget = self._build_register_form()
        self.stack.addWidget(self.login_widget)
        self.stack.addWidget(self.register_widget)

    def _build_login_form(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(35, 30, 35, 20)
        layout.setSpacing(14)

        logo = QLabel("VaultPay")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size: 34px; font-weight: bold; color: #7DD3FC;")
        layout.addWidget(logo)

        subtitle = QLabel("Secure. Simple. Smart.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #CBD5E1; font-size: 14px; margin-bottom: 18px;")
        layout.addWidget(subtitle)

        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Username or Email")
        layout.addWidget(self.login_username)

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.login_password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        register_text = QLabel("Don't have an account?")
        register_text.setAlignment(Qt.AlignCenter)
        register_text.setStyleSheet("color: #CBD5E1; margin-top: 8px;")
        layout.addWidget(register_text)

        self.go_register = QPushButton("Create account")
        self.go_register.setProperty("class", "secondary")
        self.go_register.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(self.go_register)

        layout.addStretch()
        return page

    def _build_register_form(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(35, 30, 35, 20)
        layout.setSpacing(12)

        title = QLabel("Create your account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)
        self.register_full_name = QLineEdit()
        self.register_username = QLineEdit()
        self.register_email = QLineEdit()
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_confirm_password = QLineEdit()
        self.register_confirm_password.setEchoMode(QLineEdit.Password)
        self.register_pin = QLineEdit()
        self.register_pin.setEchoMode(QLineEdit.Password)
        self.register_confirm_pin = QLineEdit()
        self.register_confirm_pin.setEchoMode(QLineEdit.Password)

        form.addRow("Full Name", self.register_full_name)
        form.addRow("Username", self.register_username)
        form.addRow("Email", self.register_email)
        form.addRow("Password", self.register_password)
        form.addRow("Confirm Password", self.register_confirm_password)
        form.addRow("PIN", self.register_pin)
        form.addRow("Confirm PIN", self.register_confirm_pin)
        layout.addLayout(form)

        self.register_button = QPushButton("Create Account")
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)

        self.back_login = QPushButton("Back to Login")
        self.back_login.setProperty("class", "secondary")
        self.back_login.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(self.back_login)

        layout.addStretch()
        return page

    def handle_register(self):
        try:
            self.account_service.register_user(
                self.register_full_name.text(),
                self.register_username.text(),
                self.register_email.text(),
                self.register_password.text(),
                self.register_confirm_password.text(),
                self.register_pin.text(),
                self.register_confirm_pin.text(),
            )
            QMessageBox.information(self, "Account Created", "Your VaultPay account has been created successfully.")
            self.stack.setCurrentIndex(0)
            self.login_username.setText(self.register_username.text())
            self.register_full_name.clear()
            self.register_username.clear()
            self.register_email.clear()
            self.register_password.clear()
            self.register_confirm_password.clear()
            self.register_pin.clear()
            self.register_confirm_pin.clear()
        except ValueError as exc:
            QMessageBox.warning(self, "Registration Failed", str(exc))

    def handle_login(self):
        try:
            user = self.account_service.login_user(self.login_username.text(), self.login_password.text())
            pin, ok = QInputDialog.getText(
                self,
                "PIN Verification",
                "Enter your 4 or 6 digit PIN to continue:",
                QLineEdit.Password,
                "",
            )
            if not ok or not pin:
                return
            if not self.account_service.verify_pin_for_user(user["id"], pin):
                raise ValueError("Incorrect PIN.")

            self.login_password.clear()
            self.hide()
            main_window = VaultPayMainWindow(user["id"], self.account_service, FinanceService())
            main_window.show()
        except ValueError as exc:
            QMessageBox.warning(self, "Login Failed", str(exc))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec_())
