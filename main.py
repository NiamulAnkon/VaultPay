import sys

from PyQt5.QtWidgets import QApplication

from database.db_manager import initialize_database
from ui.auth_window import AuthWindow


if __name__ == "__main__":
    initialize_database()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = AuthWindow()
    window.show()
    sys.exit(app.exec_())