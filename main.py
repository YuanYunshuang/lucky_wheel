import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDesktopWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QFont, QTransform, QPen
from PyQt5.QtCore import Qt, QTimer, QPointF, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import random

games = {
    "Chinese Words": "\nWrite the chinese version \n of Merry Christmas: \n 圣诞快乐 \n ",
    "Persian Words": "\nWrite the persian version \n of Merry Christmas: \n کریسمس مبارک \n ",
    "Hindi Words": "\nWrite the hindi version \n of Merry Christmas: \n क्रिसमस की बधाई \n ",
    "I'm Strong!": "Choose one person\n in this room \n and walk around everyone \n with him/her on your back \n ",
    "Sing a Song": "Sing a christmas song \n ",
    "Push-ups": "Do 10 push-ups \n ",
    "Frog Jumps": "Do 10 frog jumps \n ",
    "Make up": "If you are a girl, \n draw mustaches \n over your mouth. \n If you are a boy, \n color your lips \nwith a red lipstick \n ",
    "Rotation": "Rotate yourself \n in place 10 times in circle, \n and walk in a straight line \n ",
    "Dance": "Mimic the video, \n dance with Gangnam style \n ",
    "Thousand-year Egg": "Eat Thousand-year Egg \n ",
    "Hot Noodles": "Eat the super spicy \n hot-chicken noodles \n ",
    "Self-portrait": "Blindfold yourself \n and attempt to draw\n a self-portrait \n within one minute \n ",
    "Imitation ": "Imitate an animal \n ",
}
game_keys = list(games.keys())


class CardDrawApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.time_start = time.time()

    def initUI(self):
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, min(screen.width(), 1024), min(screen.height(), 800))
        self.setWindowTitle('Card Draw App')

        self.background_label = QLabel(self)
        self.background_label.setAlignment(Qt.AlignCenter)

        self.game_label = QLabel(self)
        self.game_label.setAlignment(Qt.AlignCenter)

        self.draw_button = QPushButton('Merry Christmas, Boo!', self)
        self.draw_button.setFixedHeight(80)
        self.draw_button.setFont(QFont("Comic Sans MS", 50))
        self.draw_button.setStyleSheet('background-color: #006400; color: white;')
        self.draw_button.clicked.connect(self.startDrawing)

        self.layout = QVBoxLayout(self)
        layout = QHBoxLayout()
        layout.addWidget(self.background_label)
        layout.addWidget(self.game_label)
        self.layout.addLayout(layout)
        self.layout.addWidget(self.draw_button)

        self.ring_image_path = 'christmas-wreath-with-lights-clipart-lg.png'
        self.card_image_path = 'image.jpg'
        self.card_text = 'Merry Christmas !'  # 卡片上的文字内容
        self.ring_text = 'Merry Christmas'  # 卡片上的文字内容
        self.ring_pixmap = QPixmap(self.ring_image_path)
        self.card_pixmap = QPixmap(self.card_image_path)
        self.card_pixmap = self.card_pixmap.scaled(1200, 1200, Qt.KeepAspectRatio)

        self.media_player = QMediaPlayer()
        self.media_player.setVolume(100)
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile('/code/luky_wheel/elf-singing-89296.mp3')))

        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotateWheel)

        self.updateCardImage()  # 初始时更新卡片图片
        self.show()

    def updateCardImage(self):
        ring_pixmap = self.ring_pixmap.copy()
        card_pixmap = self.card_pixmap.copy()
        ring_painter = QPainter(ring_pixmap)
        card_painter = QPainter(card_pixmap)
        font = QFont('Comic Sans MS', QFont.Bold)
        font.setPointSize(80)
        ring_painter.setFont(font)
        font.setPointSize(50)
        card_painter.setFont(font)
        pen = QPen(Qt.darkGreen)
        ring_painter.setPen(pen)
        card_painter.setPen(pen)

        ring_painter.drawText(self.ring_pixmap.rect(), Qt.AlignCenter, self.ring_text)
        self.background_label.setPixmap(ring_pixmap)
        card_painter.drawText(self.card_pixmap.rect(), Qt.AlignCenter, self.card_text)
        self.game_label.setPixmap(card_pixmap)

        ring_painter.end()
        card_painter.end()

    def startDrawing(self):
        self.angle = 0
        self.timer.start(30)
        self.media_player.play()

    def rotateWheel(self):
        if self.angle < 5000:
            self.angle += random.randint(10, 30)
            self.background_label.setPixmap(self.rotatePixmap(self.angle))
        else:
            self.timer.stop()
            self.showDrawnCard()

    def rotatePixmap(self, angle):
        pixmap = QPixmap(self.ring_image_path)
        rotated_pixmap = QPixmap(pixmap.size())
        rotated_pixmap.fill(Qt.transparent)

        # Paint the rotated image onto the new pixmap
        painter = QPainter(rotated_pixmap)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)

        transform = QTransform().translate(pixmap.width() / 2, pixmap.height() / 2)
        transform.rotate(angle)
        transform.translate(-pixmap.width() / 2, -pixmap.height() / 2)

        painter.setTransform(transform)
        painter.drawPixmap(0, 0, pixmap)

        painter.end()

        return rotated_pixmap

    def showDrawnCard(self):
        time_used = (time.time() - self.time_start) / 60
        prob = min(0.7, time_used / 90)
        print(prob)
        if random.random() < prob:
            self.ring_text = "Merry Christmas!"
            self.card_text = "Secret Santa has \n left a gift for you! \n Please find it!"
        else:
            idx = random.randint(0, len(game_keys) - 1)
            game = games[game_keys[idx]]
            self.ring_text = game_keys[idx]
            self.card_text = game
        self.updateCardImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CardDrawApp()
    sys.exit(app.exec_())
