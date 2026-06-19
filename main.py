import sys
from PyQt5.QtWidgets import QApplication
from Design import VideoPlayer


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.setWindowTitle("Video Player Application")
    player.resize(300, 500)
    player.show()
    sys.exit(app.exec_())

