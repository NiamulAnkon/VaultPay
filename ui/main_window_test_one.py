import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QStackedWidget, QFrame, QGraphicsDropShadowEffect, 
                             QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtGui import QColor, QFont, QIcon, QPainter, QPen

# ==========================================
# STYLESHEET
# ==========================================
STYLESHEET = """
    QMainWindow {
        background-color: #0A0F1C;
    }
    QLabel {
        color: white;
        font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
    }
    
    /* Sidebar */
    QFrame#Sidebar {
        background-color: #0F172A;
        border-right: 1px solid #1A2332;
    }
    QPushButton.SidebarButton {
        background-color: transparent;
        color: #B0BEC5;
        text-align: left;
        padding: 12px 20px;
        border: none;
        font-size: 14px;
        border-radius: 8px;
    }
    QPushButton.SidebarButton:hover {
        background-color: #1A2332;
        color: white;
    }
    QPushButton.SidebarButton:checked {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
    }

    /* Title Bar */
    QFrame#TitleBar {
        background-color: #0A0F1C;
    }
    QLineEdit#SearchBar {
        background-color: #1A2332;
        border: 1px solid #2A3441;
        border-radius: 8px;
        padding: 8px 15px;
        color: white;
        font-size: 14px;
    }
    QLineEdit#SearchBar:focus {
        border: 1px solid #1E88E5;
    }
    
    /* Cards */
    QFrame.Card {
        background-color: #1A2332;
        border-radius: 12px;
    }
    
    /* Buttons */
    QPushButton.ActionBtn {
        background-color: #2A3441;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 15px;
        font-size: 13px;
    }
    QPushButton.ActionBtn:hover {
        background-color: #1E88E5;
    }
    
    /* Window Controls */
    QPushButton.WindowCtrl {
        background-color: transparent;
        border: none;
        color: #B0BEC5;
        font-size: 16px;
    }
    QPushButton.WindowCtrl:hover {
        color: white;
        background-color: #ef4444; /* red for close */
        border-radius: 4px;
    }
    
    /* Profile Avatar */
    QPushButton#AvatarBtn {
        background-color: #1E88E5;
        color: white;
        border-radius: 16px;
        font-weight: bold;
    }
"""

# ==========================================
# CUSTOM WIDGETS
# ==========================================
class CardWidget(QFrame):
    """Base class for all dashboard cards with shadows"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "Card")
        
        # Add subtle shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

class TitleBar(QFrame):
    """Custom Frameless Title Bar"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("TitleBar")
        self.setFixedHeight(60)
        self.start_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Logo placeholder
        self.logo = QLabel("VaultPay")
        self.logo.setFont(QFont("Arial", 16, QFont.Bold))
        self.logo.setStyleSheet("color: #00C2FF;")
        
        # Search Bar
        self.search = QLineEdit()
        self.search.setObjectName("SearchBar")
        self.search.setPlaceholderText("Search...")
        self.search.setFixedWidth(400)
        
        # Profile & Notifications
        self.btn_notify = QPushButton("🔔")
        self.btn_notify.setProperty("class", "WindowCtrl")
        
        self.btn_avatar = QPushButton("AA")
        self.btn_avatar.setObjectName("AvatarBtn")
        self.btn_avatar.setFixedSize(32, 32)
        
        # Window Controls
        self.btn_min = QPushButton("−")
        self.btn_max = QPushButton("□")
        self.btn_close = QPushButton("✕")
        for btn in [self.btn_min, self.btn_max, self.btn_close]:
            btn.setProperty("class", "WindowCtrl")
            btn.setFixedSize(30, 30)
            
        self.btn_min.clicked.connect(self.parent.showMinimized)
        self.btn_max.clicked.connect(self.toggle_max)
        self.btn_close.clicked.connect(self.parent.close)

        # Assembly
        layout.addWidget(self.logo)
        layout.addStretch(1)
        layout.addWidget(self.search)
        layout.addStretch(1)
        layout.addWidget(self.btn_notify)
        layout.addWidget(self.btn_avatar)
        layout.addSpacing(20)
        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_max)
        layout.addWidget(self.btn_close)

    def toggle_max(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    # Dragging logic
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
    """The main dashboard layout"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(20)
        
        # Greeting
        greeting = QLabel("Welcome back, Ankon 👋")
        greeting.setFont(QFont("Arial", 22, QFont.Bold))
        sub = QLabel("Here's an overview of your finances.")
        sub.setStyleSheet("color: #B0BEC5; font-size: 14px;")
        
        layout.addWidget(greeting)
        layout.addWidget(sub)
        layout.addSpacing(10)
        
        # --- Top Summary Cards ---
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)
        
        self.add_summary_card(top_layout, "Current Balance", "$128,635.00", "+90%")
        self.add_summary_card(top_layout, "People Owe Me", "$117.00")
        self.add_summary_card(top_layout, "I Owe Others", "$1.60")
        self.add_summary_card(top_layout, "Recent Transactions Count", "3")
        
        layout.addLayout(top_layout)
        
        # --- Middle Section (3 columns) ---
        mid_layout = QHBoxLayout()
        mid_layout.setSpacing(15)
        
        # 1. Recent Transactions (Left)
        tx_card = CardWidget()
        tx_layout = QVBoxLayout(tx_card)
        tx_title = QLabel("Recent Transactions")
        tx_title.setFont(QFont("Arial", 14, QFont.Bold))
        tx_layout.addWidget(tx_title)
        
        # Dummy transactions
        for item in [("Manthon", "-$200 USD"), ("Amandon", "-$110 USD"), ("Withdraw", "-$500 USD")]:
            row = QHBoxLayout()
            icon = QLabel("A")
            icon.setFixedSize(30,30)
            icon.setStyleSheet("background: #2A3441; border-radius: 15px; text-align: center; color: #B0BEC5;")
            name = QLabel(item[0])
            amt = QLabel(item[1])
            row.addWidget(icon)
            row.addWidget(name)
            row.addStretch()
            row.addWidget(amt)
            tx_layout.addLayout(row)
        tx_layout.addStretch()
        mid_layout.addWidget(tx_card, stretch=4)
        
        # 2. Upcoming Debt Reminders (Middle)
        debt_card = CardWidget()
        debt_layout = QVBoxLayout(debt_card)
        debt_title = QLabel("Upcoming Debt Reminders")
        debt_title.setFont(QFont("Arial", 14, QFont.Bold))
        debt_layout.addWidget(debt_title)
        debt_layout.addStretch()
        mid_layout.addWidget(debt_card, stretch=4)
        
        # 3. Actions & Chart (Right)
        right_panel = QVBoxLayout()
        right_panel.setSpacing(15)
        
        # Actions
        actions_card = CardWidget()
        actions_layout = QVBoxLayout(actions_card)
        actions_title = QLabel("Quick Actions")
        actions_title.setFont(QFont("Arial", 14, QFont.Bold))
        actions_layout.addWidget(actions_title)
        
        btn_grid = QHBoxLayout()
        btn_grid.addWidget(self.create_action_btn("Add Money"))
        btn_grid.addWidget(self.create_action_btn("Withdraw"))
        actions_layout.addLayout(btn_grid)
        
        btn_grid2 = QHBoxLayout()
        btn_grid2.addWidget(self.create_action_btn("Transfer"))
        btn_grid2.addWidget(self.create_action_btn("Add Debt"))
        actions_layout.addLayout(btn_grid2)
        
        # Chart placeholder
        chart_card = CardWidget()
        chart_layout = QVBoxLayout(chart_card)
        chart_title = QLabel("Monthly Overview")
        chart_title.setFont(QFont("Arial", 14, QFont.Bold))
        chart_layout.addWidget(chart_title)
        
        chart_placeholder = QLabel("Chart Component Here")
        chart_placeholder.setAlignment(Qt.AlignCenter)
        chart_placeholder.setStyleSheet("color: #2A3441; font-weight: bold; font-size: 16px;")
        chart_layout.addWidget(chart_placeholder)
        
        right_panel.addWidget(actions_card)
        right_panel.addWidget(chart_card)
        
        mid_layout.addLayout(right_panel, stretch=4)
        
        layout.addLayout(mid_layout)

    def add_summary_card(self, layout, title, amount, tag=None):
        card = CardWidget()
        c_layout = QVBoxLayout(card)
        
        t_label = QLabel(title)
        t_label.setStyleSheet("color: #B0BEC5; font-size: 13px;")
        a_label = QLabel(amount)
        a_label.setFont(QFont("Arial", 20, QFont.Bold))
        
        c_layout.addWidget(t_label)
        c_layout.addSpacing(5)
        
        bottom = QHBoxLayout()
        bottom.addWidget(a_label)
        bottom.addStretch()
        if tag:
            tag_label = QLabel(tag)
            tag_label.setStyleSheet("color: #22C55E; font-size: 12px; font-weight: bold;")
            bottom.addWidget(tag_label)
            
        c_layout.addLayout(bottom)
        layout.addWidget(card)
        
    def create_action_btn(self, text):
        btn = QPushButton(text)
        btn.setProperty("class", "ActionBtn")
        return btn

# ==========================================
# MAIN APPLICATION WINDOW
# ==========================================
class VaultPayApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VaultPay")
        self.resize(1200, 800)
        self.setMinimumSize(900, 600)
        
        # Frameless Window
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QHBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 30, 15, 20)
        
        menu_items = ["Dashboard", "Wallet", "Transfer", "Debts", 
                      "Transactions", "Analytics", "Notifications", 
                      "Profile", "Settings"]
        
        for item in menu_items:
            btn = QPushButton(item)
            btn.setProperty("class", "SidebarButton")
            btn.setCheckable(True)
            if item == "Dashboard":
                btn.setChecked(True) # Set active
            sidebar_layout.addWidget(btn)
            
        sidebar_layout.addStretch()
        
        # Sidebar Bottom Info
        theme_lbl = QLabel("🌙 Dark")
        theme_lbl.setStyleSheet("color: #B0BEC5;")
        sidebar_layout.addWidget(theme_lbl)
        
        # Main Content Area
        content_area = QFrame()
        content_area.setStyleSheet("background-color: #0A0F1C;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Add Title Bar & Pages
        self.title_bar = TitleBar(self)
        self.stacked_widget = QStackedWidget()
        
        # Add Pages to Stack
        self.dashboard_page = DashboardPage()
        self.stacked_widget.addWidget(self.dashboard_page)
        
        content_layout.addWidget(self.title_bar)
        content_layout.addWidget(self.stacked_widget)
        
        # Assemble Main Window
        central_layout.addWidget(self.sidebar)
        central_layout.addWidget(content_area)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    
    window = VaultPayApp()
    window.show()
    
    sys.exit(app.exec_())