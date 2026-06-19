from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QComboBox, QPushButton, QSlider, QVBoxLayout, QWidget, QStatusBar)
from Functions import logic


class VideoPlayer(QWidget, logic):

    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()
        self.frame_number = 0
        self.positionSlider = QSlider(Qt.Horizontal)
        self.frameLabel = QLabel('Frame Number: 0')
        self.openButton = QPushButton("Open Video")
        self.stopButton = QPushButton("Stop")
        self.trimButton = QPushButton("Trim Video")
        self.playButton = QPushButton("Pause/Play")
        self.exportButton = QPushButton("Export to Excel")

        self.WeatherLabel = QLabel("Weather:")
        self.WeatherComboBox = QComboBox()
        self.roadTypeLabel = QLabel("Road Type:")
        self.roadTypeComboBox = QComboBox()
        self.TrafficLabel = QLabel("Traffic:")
        self.TrafficComboBox = QComboBox()

        self.statusBar = QStatusBar()
        self.setupUi()

    def setupUi(self):
        self.playButton.setEnabled(False)
        btnSize = QSize(16, 16)

        # Setup Open Video Button
        self.openButton.setFixedHeight(30)
        self.openButton.setIconSize(btnSize)
        self.openButton.setFont(QFont("Noto Sans", 8))
        self.openButton.setIcon(QIcon.fromTheme("", QIcon("")))
        self.openButton.clicked.connect(self.openvideo)

        # Setup Stop Video Button
        self.stopButton.setFixedHeight(35)
        self.stopButton.setIconSize(btnSize)
        self.stopButton.setFont(QFont("Noto Sans", 8))
        self.stopButton.setIcon(QIcon.fromTheme("", QIcon("")))
        self.stopButton.clicked.connect(self.stopvideo)

        # Setup Trim Video Button
        self.trimButton.setFixedHeight(35)
        self.trimButton.setIconSize(btnSize)
        self.trimButton.setFont(QFont("Noto Sans", 8))
        self.trimButton.setIcon(QIcon.fromTheme("", QIcon("")))
        self.trimButton.clicked.connect(self.trimVideo)

        # Setup Play Button
        self.playButton.setFixedHeight(35)
        self.playButton.setIconSize(btnSize)
        self.playButton.setFont(QFont("Noto Sans", 8))
        self.playButton.setIcon(QIcon.fromTheme("document-open", QIcon("")))
        self.playButton.clicked.connect(self.play)

        # Setup Position Slider
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        # Setup dropdown
        self.WeatherComboBox.setMinimumSize(QSize(150, 30))
        self.WeatherComboBox.addItem("Sunny")
        self.WeatherComboBox.addItem("Rainy")
        self.WeatherComboBox.addItem("Cloudy")
        self.roadTypeComboBox.setMinimumSize(QSize(150, 30))
        self.roadTypeComboBox.addItem("Highway")
        self.roadTypeComboBox.addItem("City Road")
        self.roadTypeComboBox.addItem("Village Road")
        self.TrafficComboBox.setMinimumSize(QSize(150, 30))
        self.TrafficComboBox.addItem("Low")
        self.TrafficComboBox.addItem("Medium")
        self.TrafficComboBox.addItem("High")

        # Open, Play,Stop Layout
        openPlayLayout = QHBoxLayout()
        openPlayLayout.addWidget(self.openButton)
        openPlayLayout.addWidget(self.playButton)
        openPlayLayout.addWidget(self.stopButton)

        # Trim and Export Layout
        trimExportLayout = QHBoxLayout()
        trimExportLayout.addWidget(self.trimButton)
        trimExportLayout.addWidget(self.exportButton)
        self.exportButton.clicked.connect(self.export_data)

        # Frame Slider Layout
        frameSliderLayout = QHBoxLayout()
        frameSliderLayout.addWidget(self.frameLabel)
        frameSliderLayout.addWidget(self.positionSlider)

        # Combined Layout for Weather, Road Type, and Traffic
        combinedLayout = QHBoxLayout()
        combinedLayout.addWidget(self.WeatherLabel)
        combinedLayout.addWidget(self.WeatherComboBox)
        combinedLayout.addSpacing(-5)
        combinedLayout.addWidget(self.roadTypeLabel)
        combinedLayout.addWidget(self.roadTypeComboBox)
        combinedLayout.addSpacing(-5)
        combinedLayout.addWidget(self.TrafficLabel)
        combinedLayout.addWidget(self.TrafficComboBox)

        # Main Layout Assembly
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.videoWidget)
        mainLayout.addLayout(frameSliderLayout)
        mainLayout.addLayout(openPlayLayout)
        mainLayout.addLayout(trimExportLayout)
        mainLayout.addLayout(combinedLayout)
        mainLayout.addWidget(self.statusBar)
        self.setLayout(mainLayout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.statusBar.showMessage("")

        # Timer for video playback
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)


