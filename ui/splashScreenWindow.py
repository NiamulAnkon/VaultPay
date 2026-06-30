import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar, QLabel, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('VaultPay')
        self.setFixedSize(1100, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 100 # total instance

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        layout.addWidget(self.frame)

        # Add Logo with Glow Effect
        self.logoLabel = QLabel(self.frame)
        logo_pixmap = QPixmap('./assets/logo.png')
        logo_pixmap = logo_pixmap.scaledToWidth(100, Qt.SmoothTransformation)
        self.logoLabel.setPixmap(logo_pixmap)
        self.logoLabel.resize(100, 100)
        self.logoLabel.move(self.width() // 2 - 50, 10)
        
        # Create glow effect
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(25)
        glow_effect.setOffset(0, 0)
        glow_effect.setColor(QColor(0, 194, 255, 200))  # Bright cyan glow color
        self.logoLabel.setGraphicsEffect(glow_effect)

        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setObjectName('LabelTitle')

        # center labels
        self.labelTitle.resize(self.width() - 10, 100)
        self.labelTitle.move(0, 115)  # x, y - positioned below logo with spacing
        self.labelTitle.setText('VaultPay')
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.labelTitle.setStyleSheet('color: #FFFFFF;')

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 40)
        self.labelDescription.move(0, self.labelTitle.y() + 90)
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong>Rendering Window</strong>')
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 60)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('loading...')

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            self.labelDescription.setText('<strong>Loading Assets</strong>')
        elif self.counter == int(self.n * 0.6):
            self.labelDescription.setText('<strong>Initializing Components</strong>')
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(1)

            self.myApp = MyApp()
            self.myApp.show()

        self.counter += 1

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        #LabelTitle {
            font-size: 60px;
            color: #FFFFFF;
        }

        #LabelDesc {
            font-size: 30px;
            color: #c2ced1;
        }

        #LabelLoading {
            font-size: 30px;
            color: #e8e8eb;
        }

        QFrame {
            background-color: #0A0F1C;
            color: rgb(220, 220, 220);
        }

        QProgressBar {
            background-color: #1E1E1E;
            color: rgb(200, 200, 200);
            border-style: none;
            border-radius: 10px;
            text-align: center;
            font-size: 30px;
        }

        QProgressBar::chunk {
            border-radius: 10px;
            background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #1565C0, stop:1 #1E88E5);
        }
    ''')
    
    splash = SplashScreen()
    splash.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
