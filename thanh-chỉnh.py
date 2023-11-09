import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

class ImageAdjustmentApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Adjustment App")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.image_label)

        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setRange(-100, 100)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(self.adjust_image)

        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(0, 300)
        self.contrast_slider.setValue(100)
        self.contrast_slider.valueChanged.connect(self.adjust_image)

        vbox = QVBoxLayout()
        vbox.addWidget(self.brightness_slider)
        vbox.addWidget(self.contrast_slider)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setMenuWidget(widget)

        self.image = None
        self.load_image('image.jpg')

    def load_image(self, image_path):
        self.image = cv2.imread(image_path)
        self.adjust_image()

    def adjust_image(self):
        if self.image is None:
            return

        brightness = self.brightness_slider.value()
        contrast = self.contrast_slider.value() / 100.0

        adjusted_image = cv2.convertScaleAbs(self.image, alpha=contrast, beta=brightness)

        h, w, c = adjusted_image.shape
        bytes_per_line = 3 * w
        q_image = QImage(adjusted_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

def main():
    app = QApplication(sys.argv)
    window = ImageAdjustmentApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
