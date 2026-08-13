from __future__ import annotations
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QDateEdit,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from pathlib import Path

from services.account_service import AccountService
from services.finance_service import FinanceService


class SidebarButton(QPushButton):
    def __init__(self, text, icon, parent=None):
        super().__init__(parent)
        self.setText(f"{icon}  {text}")
        self.setCheckable(True)
        self.setStyleSheet(
            """
            QPushButton {
                background: transparent; border: none; padding: 12px 14px; text-align: left; color: #CBD5E1;
                border-radius: 10px; font-size: 13px; font-weight: 600;
            }
            QPushButton:hover { background: rgba(148, 163, 184, 0.12); }
            QPushButton:checked { background: #1E88E5; color: white; }
            """
        )
        self.setFixedHeight(42)


class TitleBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(62)
        self.setStyleSheet("QFrame { background: #0F172A; border: none; }")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 10, 18, 10)
        layout.setSpacing(12)

        # Add logo image
        logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
        if logo_path.exists():
            logo_label = QLabel()
            logo_pixmap = QPixmap(str(logo_path))
            logo_pixmap = logo_pixmap.scaledToHeight(40, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
            layout.addWidget(logo_label)

        self.title_label = QLabel("VaultPay")
        self.title_label.setStyleSheet("color: #7DD3FC; font-size: 24px; font-weight: bold;")
        layout.addWidget(self.title_label)

        layout.addStretch(1)


class DashboardPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setStyleSheet("QWidget { background: #0A0F1C; } QLabel { color: #F8FAFC; }")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(24, 16, 24, 20)
        outer.setSpacing(18)

        self.welcome = QLabel("Welcome back")
        self.welcome.setStyleSheet("font-size: 28px; font-weight: bold;")
        outer.addWidget(self.welcome)

        cards = QHBoxLayout()
        cards.setSpacing(12)
        self.balance_card = self._card_widget("Current Balance", "0.00")
        self.people_owe_me_card = self._card_widget("People Owe Me", "0.00")
        self.i_owe_others_card = self._card_widget("I Owe Others", "0.00")
        self.transaction_count_card = self._card_widget("Total Transactions", "0")
        for widget in [self.balance_card, self.people_owe_me_card, self.i_owe_others_card, self.transaction_count_card]:
            cards.addWidget(widget)
        outer.addLayout(cards)

        middle = QHBoxLayout()
        middle.setSpacing(16)

        recent = QFrame()
        recent_layout = QVBoxLayout(recent)
        recent_layout.setContentsMargins(14, 14, 14, 14)
        recent_title = QLabel("Latest 5 transactions")
        recent_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        recent_layout.addWidget(recent_title)
        self.recent_list = QListWidget()
        self.recent_list.setStyleSheet("QListWidget { background: #111827; border: none; color: white; }")
        recent_layout.addWidget(self.recent_list)
        middle.addWidget(recent, 2)

        upcoming = QFrame()
        upcoming_layout = QVBoxLayout(upcoming)
        upcoming_layout.setContentsMargins(14, 14, 14, 14)
        upcoming_title = QLabel("Upcoming debts")
        upcoming_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        upcoming_layout.addWidget(upcoming_title)
        self.upcoming_list = QListWidget()
        self.upcoming_list.setStyleSheet("QListWidget { background: #111827; border: none; color: white; }")
        upcoming_layout.addWidget(self.upcoming_list)
        middle.addWidget(upcoming, 1)

        outer.addLayout(middle)

        actions = QFrame()
        actions_layout = QVBoxLayout(actions)
        actions_layout.setContentsMargins(14, 14, 14, 14)
        actions_title = QLabel("Quick actions")
        actions_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        actions_layout.addWidget(actions_title)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        actions_map = [
            ("Add Money", "wallet"),
            ("Withdraw Money", "wallet"),
            ("Transfer", "transfer"),
            ("Add Debt", "debts"),
            ("Repay Debt", "debts"),
        ]
        self.quick_buttons = []
        for text, target in actions_map:
            btn = QPushButton(text)
            btn.setStyleSheet("QPushButton { background: #1E293B; border: 1px solid #334155; padding: 10px; }")
            btn.clicked.connect(lambda _, t=target, txt=text: self.parent_window.open_page(t, txt))
            buttons.addWidget(btn)
            self.quick_buttons.append(btn)
        actions_layout.addLayout(buttons)
        outer.addWidget(actions)

    def _card_widget(self, title, value):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background: #111827; border: 1px solid #1F2937; border-radius: 12px; }")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 12, 14, 12)
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #94A3B8; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;")
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return frame

    def refresh(self):
        data = self.parent_window.finance_service.get_dashboard_data(self.parent_window.user_id)
        currency = self.parent_window.finance_service.get_currency(self.parent_window.user_id)
        self.balance_card.layout().itemAt(1).widget().setText(f"{currency} {data['balance']:,.2f}")
        self.people_owe_me_card.layout().itemAt(1).widget().setText(f"{currency} {data['people_owe_me']:,.2f}")
        self.i_owe_others_card.layout().itemAt(1).widget().setText(f"{currency} {data['i_owe_others']:,.2f}")
        self.transaction_count_card.layout().itemAt(1).widget().setText(str(data['total_transactions']))

        self.recent_list.clear()
        for tx in data['recent_transactions']:
            item = QListWidgetItem(f"{tx['type']} - {currency} {float(tx['amount']):,.2f} - {tx['person'] or 'Self'}")
            self.recent_list.addItem(item)

        self.upcoming_list.clear()
        for debt in data['upcoming_debts']:
            item = QListWidgetItem(f"{debt['person_name']} • {currency} {float(debt['remaining_amount']):,.2f} • {debt['due_date']}")
            self.upcoming_list.addItem(item)


class WalletPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setStyleSheet("QWidget { background: #0A0F1C; } QLabel { color: #F8FAFC; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        title = QLabel("Wallet")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        root.addWidget(title)

        card = QFrame()
        card.setStyleSheet("QFrame { background: #111827; border: 1px solid #1F2937; border-radius: 14px; }")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)

        form = QFormLayout()
        self.action_combo = QComboBox()
        self.action_combo.addItems(["Add Money", "Withdraw Money"])
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Optional note")
        form.addRow("Action", self.action_combo)
        form.addRow("Amount", self.amount_input)
        form.addRow("Note", self.note_input)
        card_layout.addLayout(form)

        self.submit_button = QPushButton("Process Transaction")
        self.submit_button.clicked.connect(self.handle_action)
        card_layout.addWidget(self.submit_button)
        root.addWidget(card)

    def handle_action(self):
        try:
            amount = float(self.amount_input.text())
            action = self.action_combo.currentText()
            if not self.parent_window.confirm_pin():
                return
            if action == "Add Money":
                self.parent_window.finance_service.add_money(self.parent_window.user_id, amount, self.note_input.text())
                QMessageBox.information(self, "Success", "Money added to your wallet.")
            else:
                self.parent_window.finance_service.withdraw_money(self.parent_window.user_id, amount, self.note_input.text())
                QMessageBox.information(self, "Success", "Money withdrawn from your wallet.")
            self.parent_window.refresh_all()
            self.amount_input.clear(); self.note_input.clear()
        except ValueError as exc:
            QMessageBox.warning(self, "Invalid Input", str(exc))


class TransferPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setStyleSheet("QWidget { background: #0A0F1C; } QLabel { color: #F8FAFC; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(18)

        title = QLabel("Transfer")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        root.addWidget(title)

        card = QFrame()
        card.setStyleSheet("QFrame { background: #111827; border: 1px solid #1F2937; border-radius: 14px; }")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)

        form = QFormLayout()
        self.recipient = QLineEdit()
        self.recipient.setPlaceholderText("Recipient name")
        self.amount = QLineEdit()
        self.amount.setPlaceholderText("0.00")
        self.note = QLineEdit()
        self.note.setPlaceholderText("Optional note")
        form.addRow("Recipient", self.recipient)
        form.addRow("Amount", self.amount)
        form.addRow("Note", self.note)
        card_layout.addLayout(form)

        btn = QPushButton("Send Transfer")
        btn.clicked.connect(self.handle_transfer)
        card_layout.addWidget(btn)
        root.addWidget(card)

    def handle_transfer(self):
        try:
            amount = float(self.amount.text())
            if not self.parent_window.confirm_pin():
                return
            self.parent_window.finance_service.transfer_money(
                self.parent_window.user_id,
                self.recipient.text(),
                amount,
                self.note.text(),
            )
            QMessageBox.information(self, "Transfer Sent", "The transfer has been recorded.")
            self.parent_window.refresh_all()
            self.recipient.clear(); self.amount.clear(); self.note.clear()
        except ValueError as exc:
            QMessageBox.warning(self, "Transfer Failed", str(exc))


class DebtsPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.selected_debt_id = None
        self.setStyleSheet("QWidget { background: #0A0F1C; } QLabel { color: #F8FAFC; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        title = QLabel("Debts")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        root.addWidget(title)

        form_card = QFrame()
        form_card.setStyleSheet("QFrame { background: #111827; border: 1px solid #1F2937; border-radius: 14px; }")
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(18, 18, 18, 18)
        form = QFormLayout()
        self.debt_direction = QComboBox()
        self.debt_direction.addItems(["People Owe Me", "I Owe Others"])
        self.debt_person = QLineEdit()
        self.debt_person.setPlaceholderText("Person name")
        self.debt_amount = QLineEdit()
        self.debt_amount.setPlaceholderText("0.00")
        self.debt_due_date = QDateEdit()
        self.debt_due_date.setCalendarPopup(True)
        self.debt_note = QLineEdit()
        self.debt_note.setPlaceholderText("Optional note")
        self.affects_balance = QComboBox()
        self.affects_balance.addItems(["Do not affect wallet", "Affect wallet"])
        form.addRow("Type", self.debt_direction)
        form.addRow("Person", self.debt_person)
        form.addRow("Amount", self.debt_amount)
        form.addRow("Due Date", self.debt_due_date)
        form.addRow("Note", self.debt_note)
        form.addRow("Wallet Impact", self.affects_balance)
        form_layout.addLayout(form)

        button_row = QHBoxLayout()
        add_btn = QPushButton("Add Debt")
        add_btn.clicked.connect(self.handle_add_debt)
        edit_btn = QPushButton("Edit Selected")
        edit_btn.clicked.connect(self.handle_edit_debt)
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.handle_delete_debt)
        payment_btn = QPushButton("Record Payment")
        payment_btn.clicked.connect(self.handle_payment)
        for btn in [add_btn, edit_btn, delete_btn, payment_btn]:
            button_row.addWidget(btn)
        form_layout.addLayout(button_row)
        root.addWidget(form_card)

        table = QFrame()
        table.setStyleSheet("QFrame { background: #111827; border: 1px solid #1F2937; border-radius: 14px; }")
        table_layout = QVBoxLayout(table)
        table_layout.setContentsMargins(14, 14, 14, 14)
        self.debt_table = QTableWidget(0, 5)
        self.debt_table.setHorizontalHeaderLabels(["Type", "Person", "Amount", "Remaining", "Status"])
        self.debt_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.debt_table.cellClicked.connect(self.on_debt_selected)
        table_layout.addWidget(self.debt_table)
        root.addWidget(table)

    def on_debt_selected(self, row, col):
        item = self.debt_table.item(row, 0)
        if item is not None:
            self.selected_debt_id = int(item.text())

    def handle_add_debt(self):
        try:
            direction = "owe_me" if self.debt_direction.currentText() == "People Owe Me" else "owe_others"
            amount = float(self.debt_amount.text())
            affect_balance = self.affects_balance.currentText() == "Affect wallet"
            if self.parent_window.confirm_pin():
                self.parent_window.finance_service.add_debt(
                    self.parent_window.user_id,
                    direction,
                    self.debt_person.text(),
                    amount,
                    self.debt_due_date.date().toString("yyyy-MM-dd"),
                    self.debt_note.text(),
                    affect_balance,
                )
                QMessageBox.information(self, "Debt Added", "Debt successfully recorded.")
                self.parent_window.refresh_all()
                self.clear_form()
        except ValueError as exc:
            QMessageBox.warning(self, "Debt Error", str(exc))

    def clear_form(self):
        self.debt_person.clear(); self.debt_amount.clear(); self.debt_note.clear(); self.affects_balance.setCurrentIndex(0)

    def handle_edit_debt(self):
        if self.selected_debt_id is None:
            QMessageBox.warning(self, "Selection Needed", "Choose a debt row first.")
            return
        try:
            person, ok1 = QInputDialog.getText(self, "Edit Person", "Person name:", text=self.debt_person.text())
            if not ok1:
                return
            amount_str, ok2 = QInputDialog.getText(self, "Edit Amount", "Amount:", text=self.debt_amount.text())
            if not ok2:
                return
            due_date, ok3 = QInputDialog.getText(self, "Edit Due Date", "Due date (YYYY-MM-DD):", text=self.debt_due_date.date().toString("yyyy-MM-dd"))
            if not ok3:
                return
            note, ok4 = QInputDialog.getText(self, "Edit Note", "Note:", text=self.debt_note.text())
            if not ok4:
                return
            self.parent_window.finance_service.update_debt(self.parent_window.user_id, self.selected_debt_id, person, float(amount_str), due_date, note)
            self.parent_window.refresh_all()
        except ValueError as exc:
            QMessageBox.warning(self, "Edit Failed", str(exc))

    def handle_delete_debt(self):
        if self.selected_debt_id is None:
            QMessageBox.warning(self, "Selection Needed", "Choose a debt row first.")
            return
        self.parent_window.finance_service.delete_debt(self.parent_window.user_id, self.selected_debt_id)
        self.parent_window.refresh_all()

    def handle_payment(self):
        if self.selected_debt_id is None:
            QMessageBox.warning(self, "Selection Needed", "Choose a debt row first.")
            return
        amount, ok = QInputDialog.getText(self, "Record Payment", "Payment amount:")
        if not ok or not amount:
            return
        note, ok_note = QInputDialog.getText(self, "Payment Note", "Optional note:", text="")
        if not ok_note:
            note = ""
        affect = QMessageBox.question(self, "Wallet Update", "Should this payment update the VaultPay balance?", QMessageBox.Yes | QMessageBox.No)
        try:
            if not self.parent_window.confirm_pin():
                return
            self.parent_window.finance_service.record_debt_payment(self.parent_window.user_id, self.selected_debt_id, float(amount), note, affect == QMessageBox.Yes)
            QMessageBox.information(self, "Payment Recorded", "Debt payment was saved.")
            self.parent_window.refresh_all()
        except ValueError as exc:
            QMessageBox.warning(self, "Payment Failed", str(exc))

    def refresh(self):
        debts = self.parent_window.finance_service.get_debts(self.parent_window.user_id)
        self.debt_table.setRowCount(len(debts))
        for row_index, debt in enumerate(debts):
            self.debt_table.setItem(row_index, 0, QTableWidgetItem(str(debt['id'])))
            self.debt_table.setItem(row_index, 1, QTableWidgetItem(debt['person_name']))
            self.debt_table.setItem(row_index, 2, QTableWidgetItem(f"{float(debt['amount']):,.2f}"))
            self.debt_table.setItem(row_index, 3, QTableWidgetItem(f"{float(debt['remaining_amount']):,.2f}"))
            self.debt_table.setItem(row_index, 4, QTableWidgetItem(debt['status']))


class TransactionsPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setStyleSheet("QWidget { background: #0A0F1C; } QLabel { color: #F8FAFC; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(16)

        title = QLabel("Transactions")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        root.addWidget(title)

        controls = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search by person, type or note")
        self.search_box.textChanged.connect(self.refresh)
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Add Money", "Withdraw Money", "Transfer", "Debt Payment Received", "Debt Payment Made"])
        self.type_filter.currentIndexChanged.connect(self.refresh)
        controls.addWidget(self.search_box, 2)
        controls.addWidget(self.type_filter, 1)
        root.addLayout(controls)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Type", "Person", "Amount", "Date"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        root.addWidget(self.table)

    def refresh(self):
        rows = self.parent_window.finance_service.get_transactions(
            self.parent_window.user_id,
            self.type_filter.currentText(),
            self.search_box.text(),
        )
        self.table.setRowCount(len(rows))
        for row_index, tx in enumerate(rows):
            self.table.setItem(row_index, 0, QTableWidgetItem(str(tx['id'])))
            self.table.setItem(row_index, 1, QTableWidgetItem(tx['type']))
            self.table.setItem(row_index, 2, QTableWidgetItem(tx['person'] or "Self"))
            self.table.setItem(row_index, 3, QTableWidgetItem(f"{float(tx['amount']):,.2f}"))
            self.table.setItem(row_index, 4, QTableWidgetItem(tx['created_at']))


class ProfilePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setStyleSheet("QWidget { background: #0A0F1C; } QLabel { color: #F8FAFC; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(18)

        title = QLabel("Profile")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        root.addWidget(title)

        card = QFrame()
        card.setStyleSheet("QFrame { background: #111827; border: 1px solid #1F2937; border-radius: 14px; }")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)

        self.avatar = QLabel("NA")
        self.avatar.setAlignment(Qt.AlignCenter)
        self.avatar.setStyleSheet("background: #1E88E5; border-radius: 30px; min-width: 80px; min-height: 80px; font-size: 28px; font-weight: bold;")
        card_layout.addWidget(self.avatar, 0, Qt.AlignCenter)

        self.profile_details = QLabel()
        self.profile_details.setWordWrap(True)
        self.profile_details.setStyleSheet("font-size: 16px; line-height: 1.6;")
        card_layout.addWidget(self.profile_details)

        button_row = QHBoxLayout()
        btn1 = QPushButton("Edit Name")
        btn1.clicked.connect(self.handle_edit_name)
        btn2 = QPushButton("Change Password")
        btn2.clicked.connect(self.handle_change_password)
        btn3 = QPushButton("Change PIN")
        btn3.clicked.connect(self.handle_change_pin)
        for btn in [btn1, btn2, btn3]:
            button_row.addWidget(btn)
        card_layout.addLayout(button_row)
        root.addWidget(card)

    def handle_edit_name(self):
        name, ok = QInputDialog.getText(self, "Edit Full Name", "Full name:")
        if ok and name:
            try:
                self.parent_window.account_service.change_name(self.parent_window.user_id, name)
                self.parent_window.refresh_all()
            except ValueError as exc:
                QMessageBox.warning(self, "Update Failed", str(exc))

    def handle_change_password(self):
        current, ok = QInputDialog.getText(self, "Current Password", "Current password:", QLineEdit.Password)
        if not ok or not current:
            return
        new_pw, ok2 = QInputDialog.getText(self, "New Password", "New password:", QLineEdit.Password)
        if not ok2 or not new_pw:
            return
        confirm_pw, ok3 = QInputDialog.getText(self, "Confirm Password", "Confirm new password:", QLineEdit.Password)
        if not ok3:
            return
        try:
            self.parent_window.account_service.change_password(self.parent_window.user_id, current, new_pw, confirm_pw)
            QMessageBox.information(self, "Password Changed", "Your password has been updated.")
        except ValueError as exc:
            QMessageBox.warning(self, "Password Change Failed", str(exc))

    def handle_change_pin(self):
        current, ok = QInputDialog.getText(self, "Current PIN", "Current PIN:", QLineEdit.Password)
        if not ok or not current:
            return
        new_pin, ok2 = QInputDialog.getText(self, "New PIN", "New PIN:", QLineEdit.Password)
        if not ok2 or not new_pin:
            return
        confirm_pin, ok3 = QInputDialog.getText(self, "Confirm PIN", "Confirm new PIN:", QLineEdit.Password)
        if not ok3:
            return
        try:
            self.parent_window.account_service.change_pin(self.parent_window.user_id, current, new_pin, confirm_pin)
            QMessageBox.information(self, "PIN Changed", "Your PIN has been updated.")
        except ValueError as exc:
            QMessageBox.warning(self, "PIN Change Failed", str(exc))

    def refresh(self):
        user = self.parent_window.account_service.get_user_by_id(self.parent_window.user_id)
        if not user:
            return
        initials = "".join(part[0].upper() for part in user["full_name"].split()[:2])
        self.avatar.setText(initials[:2] or "NA")
        self.profile_details.setText(
            f"<b>Full Name:</b> {user['full_name']}<br>"
            f"<b>Username:</b> {user['username']}<br>"
            f"<b>Email:</b> {user['email']}<br>"
            f"<b>Created:</b> {user['created_at']}"
        )


class SettingsPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        self.setStyleSheet("QWidget { background: #0A0F1C; } QLabel { color: #F8FAFC; }")

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(20)

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        root.addWidget(title)

        card = QFrame()
        card.setStyleSheet("QFrame { background: #111827; border: 1px solid #1F2937; border-radius: 14px; }")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)

        form = QFormLayout()
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["BDT", "USD", "EUR", "GBP"])
        form.addRow("Currency", self.currency_combo)
        card_layout.addLayout(form)

        save_btn = QPushButton("Save Currency")
        save_btn.clicked.connect(self.handle_currency_save)
        card_layout.addWidget(save_btn)

        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("QPushButton { background: #DC2626; border: none; }")
        logout_btn.clicked.connect(self.parent_window.logout)
        card_layout.addWidget(logout_btn)
        root.addWidget(card)

    def handle_currency_save(self):
        currency = self.currency_combo.currentText()
        self.parent_window.finance_service.set_currency(self.parent_window.user_id, currency)
        QMessageBox.information(self, "Updated", f"Default currency saved as {currency}.")

    def refresh(self):
        currency = self.parent_window.finance_service.get_currency(self.parent_window.user_id)
        self.currency_combo.setCurrentText(currency)


class VaultPayMainWindow(QMainWindow):
    def __init__(self, user_id, account_service=None, finance_service=None):
        super().__init__()
        self.user_id = user_id
        self.account_service = account_service or AccountService()
        self.finance_service = finance_service or FinanceService()
        self.setWindowTitle("VaultPay")
        self.resize(1280, 780)
        self.setStyleSheet("QMainWindow { background: #0A0F1C; } QWidget { background: #0A0F1C; color: white; }")

        # Set window icon
        icon_path = Path(__file__).parent.parent / "assets" / "logo.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QHBoxLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet("QFrame { background: #0F172A; border-right: 1px solid #1E293B; }")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(12, 12, 12, 18)
        self.sidebar_layout.setSpacing(8)

        self.user_label = QLabel()
        self.user_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e2e8f0; padding: 10px;")
        self.sidebar_layout.addWidget(self.user_label)

        self.sidebar_buttons = []
        pages = [
            ("Dashboard", "⌂", "dashboard"),
            ("Wallet", "💰", "wallet"),
            ("Transfer", "↗", "transfer"),
            ("Debts", "📌", "debts"),
            ("Transactions", "🧾", "transactions"),
            ("Profile", "👤", "profile"),
            ("Settings", "⚙", "settings"),
        ]
        for label, icon, page_name in pages:
            btn = SidebarButton(label, icon)
            btn.clicked.connect(lambda _, page_name=page_name: self.show_page(page_name))
            self.sidebar_buttons.append(btn)
            self.sidebar_layout.addWidget(btn)
        self.sidebar_layout.addStretch(1)

        self.main_content = QWidget()
        self.main_content_layout = QVBoxLayout(self.main_content)
        self.main_content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_content_layout.setSpacing(0)

        self.title_bar = TitleBar(self)
        self.main_content_layout.addWidget(self.title_bar)

        self.pages_widget = QStackedWidget()
        self.main_content_layout.addWidget(self.pages_widget)

        self.dashboard_page = DashboardPage(self)
        self.wallet_page = WalletPage(self)
        self.transfer_page = TransferPage(self)
        self.debts_page = DebtsPage(self)
        self.transactions_page = TransactionsPage(self)
        self.profile_page = ProfilePage(self)
        self.settings_page = SettingsPage(self)

        self.pages_widget.addWidget(self.dashboard_page)
        self.pages_widget.addWidget(self.wallet_page)
        self.pages_widget.addWidget(self.transfer_page)
        self.pages_widget.addWidget(self.debts_page)
        self.pages_widget.addWidget(self.transactions_page)
        self.pages_widget.addWidget(self.profile_page)
        self.pages_widget.addWidget(self.settings_page)

        self.central_layout.addWidget(self.sidebar)
        self.central_layout.addWidget(self.main_content)

        self.current_page = "dashboard"
        self.show_page("dashboard")
        self.refresh_all()

    def refresh_all(self):
        user = self.account_service.get_user_by_id(self.user_id)
        if user:
            self.user_label.setText(f"{user['full_name']}\n@{user['username']}")
        self.dashboard_page.refresh()
        self.debts_page.refresh()
        self.transactions_page.refresh()
        self.profile_page.refresh()
        self.settings_page.refresh()

    def show_page(self, page_name, action_text=None):
        mapping = {
            "dashboard": 0,
            "wallet": 1,
            "transfer": 2,
            "debts": 3,
            "transactions": 4,
            "profile": 5,
            "settings": 6,
        }
        self.pages_widget.setCurrentIndex(mapping[page_name])
        self.current_page = page_name
        for idx, btn in enumerate(self.sidebar_buttons):
            btn.setChecked(idx == list(mapping).index(page_name))

        if action_text == "Add Money":
            self.wallet_page.action_combo.setCurrentText("Add Money")
        elif action_text == "Withdraw Money":
            self.wallet_page.action_combo.setCurrentText("Withdraw Money")

    def open_page(self, page_name, action_text=None):
        self.show_page(page_name, action_text)

    def confirm_pin(self):
        pin, ok = QInputDialog.getText(self, "PIN Verification", "Enter your PIN:", QLineEdit.Password)
        if not ok or not pin:
            return False
        if not self.account_service.verify_pin_for_user(self.user_id, pin):
            QMessageBox.warning(self, "PIN Error", "Incorrect PIN.")
            return False
        return True

    def logout(self):
        self.close()
        from ui.auth_window import AuthWindow
        auth_window = AuthWindow()
        auth_window.show()


if __name__ == "__main__":
    app = QApplication([])
    window = VaultPayMainWindow(1)
    window.show()
    app.exec_()
