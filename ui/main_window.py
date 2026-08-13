import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QStackedWidget, QFrame,
    QGraphicsDropShadowEffect, QScrollArea, QSizePolicy, QMessageBox,
    QInputDialog, QTableWidget, QTableWidgetItem, QComboBox,
    QGroupBox, QFormLayout, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, QPoint, QSize, QEasingCurve, QPropertyAnimation
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QBrush, QCursor


BG = "#0A0F1C"
SECONDARY_BG = "#111827"
SIDEBAR_BG = "#0F172A"
CARD_BG = "#1A2332"
PRIMARY_BLUE = "#1E88E5"
ACCENT = "#00C2FF"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER = "#EF4444"
TEXT = "#FFFFFF"
TEXT_MUTED = "#B0BEC5"
BORDER = "#243042"


STYLESHEET = f"""
QMainWindow {{ background: transparent; }}
QWidget {{ color: {TEXT}; font-family: 'Segoe UI', 'Inter', 'Helvetica Neue', sans-serif; }}
QLabel {{ color: {TEXT}; }}
QFrame#WindowContainer {{
    background-color: {BG};
    border: 1px solid {BORDER};
    border-radius: 16px;
}}
QFrame#MainContent {{ background-color: {BG}; }}
QFrame#Sidebar {{
    background-color: {SIDEBAR_BG};
    border: 1px solid {BORDER};
    border-radius: 16px;
}}
QFrame.Card {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 14px;
}}
QFrame.SectionCard {{
    background-color: rgba(26, 35, 50, 0.9);
    border: 1px solid {BORDER};
    border-radius: 14px;
}}
QPushButton {{
    background-color: transparent;
    color: {TEXT};
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 10px 14px;
    outline: none;
}}
QPushButton:hover {{
    background-color: rgba(30, 136, 229, 0.15);
    border: 1px solid rgba(0, 194, 255, 0.35);
}}
QPushButton:pressed {{ background-color: rgba(30, 136, 229, 0.25); }}
QPushButton.ActionBtn {{
    background-color: rgba(30, 136, 229, 0.18);
    border: 1px solid rgba(0, 194, 255, 0.2);
    color: {TEXT};
    padding: 10px 16px;
}}
QPushButton.ActionBtn:hover {{
    background-color: {PRIMARY_BLUE};
    border: 1px solid {ACCENT};
}}
QPushButton.WindowCtrl {{
    background-color: transparent;
    border: none;
    color: {TEXT_MUTED};
    padding: 6px;
    min-width: 30px;
    min-height: 30px;
}}
QPushButton.WindowCtrl:hover {{ color: {TEXT}; background-color: rgba(255,255,255,0.06); }}
QPushButton#CloseBtn:hover {{ background-color: {DANGER}; color: white; }}
QLineEdit, QComboBox, QTextEdit {{
    background-color: rgba(255,255,255,0.05);
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 10px 12px;
    color: {TEXT};
}}
QLineEdit:focus, QComboBox:focus, QTextEdit:focus {{ border: 1px solid {ACCENT}; }}
QComboBox::drop-down {{ border: none; }}
QComboBox QAbstractItemView {{ background-color: {SECONDARY_BG}; selection-background-color: {PRIMARY_BLUE}; }}
QScrollBar:vertical {{ background: transparent; width: 10px; }}
QScrollBar::handle:vertical {{ background: rgba(255,255,255,0.16); border-radius: 5px; }}
QScrollBar::handle:vertical:hover {{ background: rgba(255,255,255,0.24); }}
QTableWidget {{
    background-color: transparent;
    gridline-color: rgba(255,255,255,0.06);
    border: none;
    color: {TEXT};
}}
QHeaderView::section {{
    background-color: rgba(255,255,255,0.04);
    color: {TEXT_MUTED};
    padding: 10px;
    border: none;
}}
QListWidget {{ background: transparent; border: none; }}
QListWidget::item {{ padding: 8px; border-radius: 8px; }}
QListWidget::item:hover {{ background-color: rgba(255,255,255,0.05); }}
"""


class CardWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Card")
        self.setProperty("class", "Card")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 70))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)


class SidebarButton(QPushButton):
    def __init__(self, icon, text, parent=None):
        super().__init__(parent)
        self.icon_text = icon
        self.label_text = text
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(46)
        self.setProperty("class", "SidebarButton")
        self.setToolTip(text)
        self.icon_label = QLabel(icon)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setFixedSize(24, 24)
        self.text_label = QLabel(text)
        self.text_label.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 13px;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addStretch(1)

    def set_collapsed(self, collapsed: bool):
        self.text_label.setVisible(not collapsed)
        self.setFixedWidth(70 if collapsed else 240)
        if collapsed:
            self.setToolTip(self.label_text)
        else:
            self.setToolTip("")


class CircularProgressWidget(QWidget):
    def __init__(self, percentage=72, parent=None):
        super().__init__(parent)
        self.percentage = percentage
        self.setFixedSize(140, 140)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(8, 8, -8, -8)
        painter.setPen(QPen(QColor(255, 255, 255, 18), 10))
        painter.drawArc(rect, 0, 360 * 16)
        painter.setPen(QPen(QColor(0, 194, 255), 10, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(rect, 90 * 16, int(-(self.percentage / 100) * 360) * 16)
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(rect.center(), 2, 2)
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.percentage}%")


class TitleBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("TitleBar")
        self.setFixedHeight(70)
        self.setStyleSheet(f"background-color: {BG};")
        self.start_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(14)

        logo_box = QHBoxLayout()
        logo_box.setSpacing(10)
        logo_icon = QLabel("V")
        logo_icon.setAlignment(Qt.AlignCenter)
        logo_icon.setFixedSize(34, 34)
        logo_icon.setStyleSheet(f"background-color: {PRIMARY_BLUE}; border-radius: 17px; color: white; font-weight: bold;")
        logo_text = QLabel("VaultPay")
        logo_text.setFont(QFont("Segoe UI", 15, QFont.Bold))
        logo_text.setStyleSheet(f"color: {TEXT};")
        logo_box.addWidget(logo_icon)
        logo_box.addWidget(logo_text)

        self.search = QLineEdit()
        self.search.setObjectName("SearchBar")
        self.search.setPlaceholderText("Search...")
        self.search.setFixedWidth(420)
        self.search.setStyleSheet("padding-left: 14px;")

        self.btn_notify = QPushButton("🔔")
        self.btn_notify.setProperty("class", "WindowCtrl")
        self.btn_notify.setFixedSize(38, 38)

        self.avatar_btn = QPushButton("AK")
        self.avatar_btn.setFixedSize(38, 38)
        self.avatar_btn.setStyleSheet(f"background-color: {ACCENT}; color: white; border-radius: 19px; font-weight: bold;")

        self.btn_min = QPushButton("—")
        self.btn_min.setProperty("class", "WindowCtrl")
        self.btn_min.setObjectName("MinBtn")
        self.btn_min.setFixedSize(34, 34)
        self.btn_max = QPushButton("▢")
        self.btn_max.setProperty("class", "WindowCtrl")
        self.btn_max.setFixedSize(34, 34)
        self.btn_close = QPushButton("✕")
        self.btn_close.setProperty("class", "WindowCtrl")
        self.btn_close.setObjectName("CloseBtn")
        self.btn_close.setFixedSize(34, 34)

        self.btn_min.clicked.connect(self.parent.showMinimized)
        self.btn_max.clicked.connect(self.toggle_max)
        self.btn_close.clicked.connect(self.parent.close)

        layout.addLayout(logo_box)
        layout.addStretch(1)
        layout.addWidget(self.search)
        layout.addStretch(1)
        layout.addWidget(self.btn_notify)
        layout.addWidget(self.avatar_btn)
        layout.addSpacing(12)
        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_max)
        layout.addWidget(self.btn_close)

    def toggle_max(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.start_pos is not None:
            delta = event.globalPos() - self.start_pos
            self.parent.move(self.parent.pos() + delta)
            self.start_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.start_pos = None


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        header = QVBoxLayout()
        header.setSpacing(4)
        title = QLabel("Welcome back, Ankon 👋")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        subtitle = QLabel("Here\'s an overview of your finances.")
        subtitle.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 13px;")
        header.addWidget(title)
        header.addWidget(subtitle)
        layout.addLayout(header)

        summary_row = QHBoxLayout()
        summary_row.setSpacing(16)
        summary_row.addWidget(self.create_metric_card("Current Balance", "$128,635.00", "+8.9%", PRIMARY_BLUE))
        summary_row.addWidget(self.create_metric_card("People Owe Me", "$4,200.00", "+12.1%", SUCCESS))
        summary_row.addWidget(self.create_metric_card("I Owe Others", "$1,640.00", "-3.2%", WARNING))
        summary_row.addWidget(self.create_metric_card("Recent Transactions", "3", "Today", ACCENT))
        layout.addLayout(summary_row)

        main_row = QHBoxLayout()
        main_row.setSpacing(16)

        left_col = QVBoxLayout()
        left_col.setSpacing(16)
        left_col.addWidget(self.create_recent_transactions_card())
        left_col.addWidget(self.create_debt_reminders_card())
        main_row.addLayout(left_col, 2)

        right_col = QVBoxLayout()
        right_col.setSpacing(16)
        right_col.addWidget(self.create_quick_actions_card())
        right_col.addWidget(self.create_monthly_overview_card())
        main_row.addLayout(right_col, 1)

        layout.addLayout(main_row)
        layout.addStretch(1)

    def create_metric_card(self, title, amount, meta, accent):
        card = CardWidget()
        card.setFixedHeight(115)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 13px;")
        amount_label = QLabel(amount)
        amount_label.setFont(QFont("Segoe UI", 19, QFont.Bold))
        meta_label = QLabel(meta)
        meta_label.setStyleSheet(f"color: {accent}; font-size: 12px; font-weight: bold;")
        layout.addWidget(title_label)
        layout.addWidget(amount_label)
        layout.addWidget(meta_label)
        return card

    def create_recent_transactions_card(self):
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        title = QLabel("Recent Transactions")
        title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        layout.addWidget(title)
        for name, amount, category in [("Ava Brooks", "-$240.00", "Groceries"), ("Liam Carter", "$1,500.00", "Salary"), ("Noah Reed", "-$80.00", "Utilities")]:
            row = QHBoxLayout()
            icon = QLabel("•")
            icon.setFixedSize(24, 24)
            icon.setAlignment(Qt.AlignCenter)
            icon.setStyleSheet(f"background-color: rgba(30,136,229,0.15); border-radius: 12px; color: {ACCENT};")
            info = QLabel(name)
            info.setStyleSheet(f"color: {TEXT_MUTED};")
            amount_label = QLabel(amount)
            amount_label.setStyleSheet(f"color: {TEXT}; font-weight: 600;")
            row.addWidget(icon)
            row.addWidget(info)
            row.addStretch(1)
            row.addWidget(amount_label)
            layout.addLayout(row)
        return card

    def create_debt_reminders_card(self):
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        title = QLabel("Upcoming Debt Reminders")
        title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        layout.addWidget(title)
        for name, due, amount in [("Mina Clark", "Today", "$320"), ("Rory Stone", "Tomorrow", "$120")]:
            row = QFrame()
            row.setStyleSheet(f"background-color: rgba(255,255,255,0.03); border-radius: 10px; padding: 8px;")
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(10, 8, 10, 8)
            label = QLabel(f"{name} · {due}")
            label.setStyleSheet(f"color: {TEXT_MUTED};")
            amount_label = QLabel(amount)
            amount_label.setStyleSheet(f"color: {WARNING}; font-weight: bold;")
            row_layout.addWidget(label)
            row_layout.addStretch(1)
            row_layout.addWidget(amount_label)
            layout.addWidget(row)
        return card

    def create_quick_actions_card(self):
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        title = QLabel("Quick Actions")
        title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        layout.addWidget(title)
        grid = QHBoxLayout()
        grid.setSpacing(10)
        for text in ["Add Money", "Withdraw", "Transfer", "Add Debt"]:
            btn = QPushButton(text)
            btn.setProperty("class", "ActionBtn")
            grid.addWidget(btn)
        layout.addLayout(grid)
        return card

    def create_monthly_overview_card(self):
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        title = QLabel("Monthly Overview")
        title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        layout.addWidget(title)
        row = QHBoxLayout()
        row.addWidget(CircularProgressWidget(78))
        legend = QVBoxLayout()
        for label, value, color in [("Income", "$6.8k", SUCCESS), ("Expense", "$4.2k", WARNING), ("Savings", "$2.6k", ACCENT)]:
            item = QHBoxLayout()
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 16px;")
            text = QLabel(f"{label}  {value}")
            text.setStyleSheet(f"color: {TEXT_MUTED};")
            item.addWidget(dot)
            item.addWidget(text)
            legend.addLayout(item)
        row.addLayout(legend)
        layout.addLayout(row)
        return card


class WalletPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)
        title = QLabel("Wallet")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        subtitle = QLabel("Manage balances, deposits, and withdrawals.")
        subtitle.setStyleSheet(f"color: {TEXT_MUTED};")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        summary = CardWidget()
        summary_layout = QHBoxLayout(summary)
        summary_layout.setContentsMargins(20, 20, 20, 20)
        balance_text = QLabel("Current Balance")
        balance_text.setStyleSheet(f"color: {TEXT_MUTED};")
        balance_value = QLabel("$128,635.00")
        balance_value.setFont(QFont("Segoe UI", 24, QFont.Bold))
        summary_layout.addWidget(balance_text)
        summary_layout.addStretch(1)
        summary_layout.addWidget(balance_value)
        layout.addWidget(summary)

        actions = QHBoxLayout()
        actions.setSpacing(12)
        add_money = QPushButton("Add Money")
        add_money.setProperty("class", "ActionBtn")
        add_money.clicked.connect(self.add_money)
        withdraw = QPushButton("Withdraw Money")
        withdraw.setProperty("class", "ActionBtn")
        withdraw.clicked.connect(self.withdraw_money)
        actions.addWidget(add_money)
        actions.addWidget(withdraw)
        layout.addLayout(actions)

        history_row = QHBoxLayout()
        history_row.setSpacing(16)
        history_row.addWidget(self.create_history_card("Deposit History", ["Payroll", "Transfer", "Refund"]), 1)
        history_row.addWidget(self.create_history_card("Withdrawal History", ["ATM", "Rent", "Vendor"]), 1)
        layout.addLayout(history_row)

    def create_history_card(self, title, items):
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 15, QFont.Bold))
        layout.addWidget(title_label)
        for item in items:
            row = QLabel(f"• {item}")
            row.setStyleSheet(f"color: {TEXT_MUTED};")
            layout.addWidget(row)
        layout.addStretch(1)
        return card

    def add_money(self):
        amount, ok = QInputDialog.getDouble(self, "Add Money", "Enter amount", 100.0, 0, 1000000, 2)
        if ok:
            QMessageBox.information(self, "Success", f"Added ${amount:.2f} to your wallet.")

    def withdraw_money(self):
        amount, ok = QInputDialog.getDouble(self, "Withdraw Money", "Enter amount", 50.0, 0, 1000000, 2)
        if ok:
            QMessageBox.information(self, "Success", f"Withdrawn ${amount:.2f} from your wallet.")


class TransferPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        title = QLabel("Transfer")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        subtitle = QLabel("Send money securely with a premium transfer flow.")
        subtitle.setStyleSheet(f"color: {TEXT_MUTED};")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        form_card = CardWidget()
        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form = QFormLayout()
        recipient = QLineEdit()
        recipient.setPlaceholderText("Recipient email or username")
        amount = QLineEdit()
        amount.setPlaceholderText("Amount")
        note = QLineEdit()
        note.setPlaceholderText("Add a note")
        form.addRow(QLabel("Recipient"), recipient)
        form.addRow(QLabel("Amount"), amount)
        form.addRow(QLabel("Note"), note)
        form_layout.addLayout(form)
        transfer_btn = QPushButton("Transfer")
        transfer_btn.setProperty("class", "ActionBtn")
        transfer_btn.clicked.connect(lambda: QMessageBox.information(self, "Transfer", "Transfer request queued successfully."))
        form_layout.addWidget(transfer_btn, 0, Qt.AlignRight)
        layout.addWidget(form_card)

        recent_card = CardWidget()
        recent_layout = QVBoxLayout(recent_card)
        recent_layout.setContentsMargins(18, 18, 18, 18)
        recent_title = QLabel("Recent Transfers")
        recent_title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        recent_layout.addWidget(recent_title)
        for target, amount_text in [("Mina", "$240.00"), ("Rory", "$80.00")]:
            row = QHBoxLayout()
            label = QLabel(f"{target} · {amount_text}")
            label.setStyleSheet(f"color: {TEXT_MUTED};")
            row.addWidget(label)
            row.addStretch(1)
            recent_layout.addLayout(row)
        layout.addWidget(recent_card)


class DebtsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)
        title = QLabel("Debts")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        subtitle = QLabel("Track what people owe you and what you owe others.")
        subtitle.setStyleSheet(f"color: {TEXT_MUTED};")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        summary_row = QHBoxLayout()
        summary_row.setSpacing(16)
        summary_row.addWidget(self.create_metric_card("Total Outstanding", "$4,200.00", SUCCESS))
        summary_row.addWidget(self.create_metric_card("Total Borrowed", "$1,640.00", WARNING))
        layout.addLayout(summary_row)

        actions = QHBoxLayout()
        actions.setSpacing(10)
        actions.addWidget(QPushButton("Add Debt"))
        actions.addStretch(1)
        layout.addLayout(actions)

        section1 = CardWidget()
        s1_layout = QVBoxLayout(section1)
        s1_layout.setContentsMargins(18, 18, 18, 18)
        s1_title = QLabel("People Owe Me")
        s1_title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        s1_layout.addWidget(s1_title)
        s1_layout.addWidget(self.create_debt_entry("Mina Clark", "$320.00", "$120.00", "May 18", "Open"))
        s1_layout.addWidget(self.create_debt_entry("Noah Reed", "$180.00", "$180.00", "Jun 03", "Overdue"))
        layout.addWidget(section1)

        section2 = CardWidget()
        s2_layout = QVBoxLayout(section2)
        s2_layout.setContentsMargins(18, 18, 18, 18)
        s2_title = QLabel("I Owe Others")
        s2_title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        s2_layout.addWidget(s2_title)
        s2_layout.addWidget(self.create_debt_entry("Ava Brooks", "$95.00", "$45.00", "May 30", "Scheduled"))
        layout.addWidget(section2)

    def create_metric_card(self, title, amount, color):
        card = CardWidget()
        card.setFixedHeight(100)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {TEXT_MUTED};")
        amount_label = QLabel(amount)
        amount_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        amount_label.setStyleSheet(f"color: {color};")
        layout.addWidget(title_label)
        layout.addWidget(amount_label)
        return card

    def create_debt_entry(self, name, amount, balance, due, status):
        entry = QFrame()
        entry.setStyleSheet(f"background-color: rgba(255,255,255,0.03); border-radius: 10px; padding: 8px;")
        layout = QHBoxLayout(entry)
        layout.setContentsMargins(10, 10, 10, 10)
        left = QVBoxLayout()
        left.addWidget(QLabel(name))
        left.addWidget(QLabel(f"Amount: {amount}"))
        left.addWidget(QLabel(f"Remaining: {balance}"))
        right = QVBoxLayout()
        right.addWidget(QLabel(f"Due: {due}"))
        badge = QLabel(status)
        badge.setStyleSheet(f"background-color: rgba(30,136,229,0.15); color: {ACCENT}; padding: 5px 8px; border-radius: 8px;")
        right.addWidget(badge)
        actions = QHBoxLayout()
        actions.addWidget(QPushButton("Mark Paid"))
        actions.addWidget(QPushButton("Edit"))
        actions.addWidget(QPushButton("Delete"))
        right.addLayout(actions)
        layout.addLayout(left)
        layout.addStretch(1)
        layout.addLayout(right)
        return entry


class TransactionsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        title = QLabel("Transactions")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        subtitle = QLabel("Analyze deposits, transfers, and debt activity.")
        subtitle.setStyleSheet(f"color: {TEXT_MUTED};")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        filters = QHBoxLayout()
        filters.setSpacing(10)
        filters.addWidget(QLineEdit("Search"))
        filters.addWidget(QComboBox())
        filters.addWidget(QComboBox())
        layout.addLayout(filters)

        table = QTableWidget(6, 6)
        table.setHorizontalHeaderLabels(["Date", "Description", "Category", "Amount", "Status", "Type"])
        rows = [
            ("2026-07-10", "Payroll", "Income", "$1,500", "Completed", "Deposit"),
            ("2026-07-08", "Transfer to Mina", "Transfer", "$240", "Pending", "Transfer"),
            ("2026-07-07", "Loan repayment", "Debt", "$80", "Completed", "Debt"),
        ]
        table.setRowCount(len(rows))
        for row_index, row_data in enumerate(rows):
            for col_index, value in enumerate(row_data):
                table.setItem(row_index, col_index, QTableWidgetItem(value))
        table.resizeColumnsToContents()
        layout.addWidget(table)


class AnalyticsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        title = QLabel("Analytics")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        subtitle = QLabel("Clear insight into spending, income, and debt trends.")
        subtitle.setStyleSheet(f"color: {TEXT_MUTED};")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        row1 = QHBoxLayout()
        row1.setSpacing(16)
        row1.addWidget(self.create_chart_card("Monthly Spending", [40, 70, 55, 90, 80]), 1)
        row1.addWidget(self.create_chart_card("Income vs Expense", [64, 32]), 1)
        layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(16)
        row2.addWidget(self.create_chart_card("Debt Overview", [30, 70]), 1)
        row2.addWidget(self.create_category_card(), 1)
        layout.addLayout(row2)

    def create_chart_card(self, title, bars):
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 15, QFont.Bold))
        layout.addWidget(title_label)
        for value in bars:
            bar = QFrame()
            bar.setFixedHeight(16)
            bar.setStyleSheet(f"background-color: rgba(255,255,255,0.06); border-radius: 8px;")
            inner = QFrame(bar)
            inner.setStyleSheet(f"background-color: {PRIMARY_BLUE}; border-radius: 8px;")
            inner.setGeometry(0, 0, int(value * 2), 16)
            layout.addWidget(bar)
        return card

    def create_category_card(self):
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        title = QLabel("Top Categories")
        title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        layout.addWidget(title)
        for category, amount in [("Food", "$840"), ("Travel", "$620"), ("Utilities", "$310")]:
            row = QHBoxLayout()
            row.addWidget(QLabel(category))
            row.addStretch(1)
            row.addWidget(QLabel(amount))
            layout.addLayout(row)
        return card


class NotificationsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        title = QLabel("Notifications")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        subtitle = QLabel("Stay on top of transfers, reminders, and account updates.")
        subtitle.setStyleSheet(f"color: {TEXT_MUTED};")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        for msg, time, unread in [("Transfer received from Mina", "2m ago", True), ("Debt reminder for Rory", "1h ago", True), ("Backup completed", "3h ago", False)]:
            card = CardWidget()
            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(16, 16, 16, 16)
            unread_dot = QLabel("●") if unread else QLabel("")
            unread_dot.setStyleSheet(f"color: {ACCENT}; font-size: 16px;")
            body = QLabel(msg)
            body.setStyleSheet(f"color: {TEXT_MUTED};")
            ts = QLabel(time)
            ts.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px;")
            actions = QHBoxLayout()
            actions.addWidget(QPushButton("Mark Read"))
            actions.addWidget(QPushButton("Delete"))
            card_layout.addWidget(unread_dot)
            card_layout.addWidget(body)
            card_layout.addStretch(1)
            card_layout.addWidget(ts)
            card_layout.addLayout(actions)
            layout.addWidget(card)


class ProfilePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)
        title = QLabel("Profile")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        subtitle = QLabel("Manage your identity and account security.")
        subtitle.setStyleSheet(f"color: {TEXT_MUTED};")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        profile_card = CardWidget()
        profile_layout = QHBoxLayout(profile_card)
        profile_layout.setContentsMargins(20, 20, 20, 20)
        avatar = QLabel("AK")
        avatar.setFixedSize(72, 72)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setStyleSheet(f"background-color: {PRIMARY_BLUE}; border-radius: 36px; font-size: 22px; font-weight: bold;")
        info = QVBoxLayout()
        info.addWidget(QLabel("Ankon Karmakar"))
        info.addWidget(QLabel("@ankon"))
        info.addWidget(QLabel("ankon@vaultpay.app"))
        profile_layout.addWidget(avatar)
        profile_layout.addLayout(info)
        layout.addWidget(profile_card)

        actions = QHBoxLayout()
        actions.setSpacing(10)
        actions.addWidget(QPushButton("Change Password"))
        actions.addWidget(QPushButton("Change PIN"))
        actions.addWidget(QPushButton("Upload Profile Picture"))
        layout.addLayout(actions)


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)
        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        subtitle = QLabel("Customize VaultPay and control local data operations.")
        subtitle.setStyleSheet(f"color: {TEXT_MUTED};")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        sections = [
            ("Application Settings", ["Dark mode", "Auto backup", "Compact layout"]),
            ("Database Backup", ["Create Backup", "Restore Backup"]),
            ("Security", ["2FA Enabled", "PIN Protection", "Biometric Support"]),
            ("About VaultPay", ["Version 1.0.0", "Offline-first desktop wallet", "Built for PyQt5"]),
        ]
        for heading, items in sections:
            card = CardWidget()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(18, 18, 18, 18)
            card_layout.addWidget(QLabel(heading))
            for item in items:
                row = QLabel(f"• {item}")
                row.setStyleSheet(f"color: {TEXT_MUTED};")
                card_layout.addWidget(row)
            layout.addWidget(card)


class VaultPayApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VaultPay")
        self.resize(1320, 860)
        self.setMinimumSize(1100, 720)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.container = QFrame(self)
        self.container.setObjectName("WindowContainer")
        self.container.setGraphicsEffect(QGraphicsDropShadowEffect(self.container))
        self.setCentralWidget(self.container)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.title_bar = TitleBar(self)
        self.title_bar.setStyleSheet(f"background-color: {BG}; border-bottom: 1px solid {BORDER};")

        content_row = QHBoxLayout()
        content_row.setContentsMargins(0, 0, 0, 0)
        content_row.setSpacing(0)

        self.sidebar = QFrame(self)
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setMinimumWidth(70)
        self.sidebar.setMaximumWidth(240)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(14, 18, 14, 18)
        self.sidebar_layout.setSpacing(8)

        self.collapse_btn = QPushButton("☰")
        self.collapse_btn.setFixedSize(40, 40)
        self.collapse_btn.setProperty("class", "ActionBtn")
        self.collapse_btn.clicked.connect(self.toggle_sidebar)
        self.sidebar_layout.addWidget(self.collapse_btn, 0, Qt.AlignLeft)

        self.menu_buttons = []
        menu_items = [
            ("🏠", "Dashboard"), ("💳", "Wallet"), ("🔁", "Transfer"),
            ("🏦", "Debts"), ("💱", "Transactions"), ("📊", "Analytics"),
            ("🔔", "Notifications"), ("👤", "Profile"), ("⚙️", "Settings")
        ]
        for icon, label in menu_items:
            button = SidebarButton(icon, label)
            button.setCheckable(True)
            if label == "Dashboard":
                button.setChecked(True)
            button.clicked.connect(lambda checked, lbl=label: self.switch_page(lbl))
            self.sidebar_layout.addWidget(button)
            self.menu_buttons.append(button)

        self.sidebar_layout.addStretch(1)
        bottom = QVBoxLayout()
        bottom.setSpacing(8)
        bottom.addWidget(QLabel("🌙 Dark"))
        bottom.addWidget(QLabel("v1.0.0"))
        balance_card = CardWidget()
        balance_card.setFixedHeight(100)
        b_layout = QVBoxLayout(balance_card)
        b_layout.setContentsMargins(12, 12, 12, 12)
        b_layout.addWidget(QLabel("Current Balance"))
        b_layout.addWidget(QLabel("$128,635.00"))
        bottom.addWidget(balance_card)
        self.sidebar_layout.addLayout(bottom)

        self.content_area = QFrame(self)
        self.content_area.setObjectName("MainContent")
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setStyleSheet("background-color: transparent;")
        self.dashboard_page = DashboardPage()
        self.wallet_page = WalletPage()
        self.transfer_page = TransferPage()
        self.debts_page = DebtsPage()
        self.transactions_page = TransactionsPage()
        self.analytics_page = AnalyticsPage()
        self.notifications_page = NotificationsPage()
        self.profile_page = ProfilePage()
        self.settings_page = SettingsPage()
        self.pages = {
            "Dashboard": self.dashboard_page,
            "Wallet": self.wallet_page,
            "Transfer": self.transfer_page,
            "Debts": self.debts_page,
            "Transactions": self.transactions_page,
            "Analytics": self.analytics_page,
            "Notifications": self.notifications_page,
            "Profile": self.profile_page,
            "Settings": self.settings_page,
        }
        for page in self.pages.values():
            self.stacked_widget.addWidget(page)

        self.content_layout.addWidget(self.title_bar)
        self.content_layout.addWidget(self.stacked_widget)

        content_row.addWidget(self.sidebar)
        content_row.addWidget(self.content_area)

        container_layout.addLayout(content_row)

        self.is_expanded = True
        self.sidebar_animation = QPropertyAnimation(self.sidebar, b"maximumWidth")
        self.sidebar_animation.setDuration(220)
        self.sidebar_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.sidebar_animation.setStartValue(240)
        self.sidebar_animation.setEndValue(70)

    def toggle_sidebar(self):
        self.is_expanded = not self.is_expanded
        target = 240 if self.is_expanded else 70
        self.sidebar_animation.stop()
        self.sidebar_animation.setStartValue(self.sidebar.width())
        self.sidebar_animation.setEndValue(target)
        self.sidebar_animation.start()
        for button in self.menu_buttons:
            button.set_collapsed(not self.is_expanded)

    def switch_page(self, label):
        for button in self.menu_buttons:
            button.setChecked(button.label_text == label)
        self.stacked_widget.setCurrentWidget(self.pages[label])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    window = VaultPayApp()
    window.show()
    sys.exit(app.exec_())
