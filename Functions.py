import cv2
import openpyxl
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (QFileDialog, QStyle)

    
class logic():
    def openvideo(self):
        # need to install codec for *.mp4 *.mkv *.ts *.mts videos.
        fileName, _ = QFileDialog.getOpenFileName(self, "", ".", "Video Files (*.avi)")
        print(fileName)
        if fileName:
            self.videoPath = fileName
            self.cap = cv2.VideoCapture(fileName)
            self.frameCount = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.frameRate = self.cap.get(cv2.CAP_PROP_FPS)
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.statusBar.showMessage(fileName)
            self.play()

    def stopvideo(self):
        """Stops the video playback and resets the frame counter."""
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.stop()
        self.timer.stop()
        self.frame_number = 0
        self.frameLabel.setText('Frame Number: 0')

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.timer.stop()
        else:
            self.mediaPlayer.play()
            self.timer.start(int(1000 / self.frameRate))

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
            self.timer.start(int(1000 / self.frameRate))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
            self.timer.stop()

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        if self.frameRate > 0:
            self.frame_number = int((position / 1000) * self.frameRate)
            self.frameLabel.setText(f'Frame Number: {self.frame_number}')

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())

    def trimVideo(self):
        if hasattr(self, 'videoPath'):
            cap = cv2.VideoCapture(self.videoPath)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter('output_trimmed.mp4', fourcc, self.frameRate, (int(cap.get(3)), int(cap.get(4))))
            count = 0
            while True:
                ret, frame = cap.read()
                if not ret or count > (30 * self.frameRate):
                    break
                out.write(frame)
                count += 1
            cap.release()
            out.release()
            print("Trimming completed.")

    def next_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame_number += 1
            self.frameLabel.setText(f'Frame Number: {self.frame_number}')
        else:
            self.timer.stop()
            self.cap.release()
            self.frame_number = 0
            self.frameLabel.setText('Frame Number: 0')

    def export_data(self):
        # Get selected values
        weather_type = self.WeatherComboBox.currentText()
        road_type = self.roadTypeComboBox.currentText()
        traffic_type = self.TrafficComboBox.currentText()

        # Create Excel workbook and sheet
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(["Weather", "Road Type", "Traffic"])
        sheet.append([weather_type, road_type, traffic_type])

        # Save the Excel file
        wb.save("data.xlsx")

        # Show success message
        print("Data exported to data.xlsx")
