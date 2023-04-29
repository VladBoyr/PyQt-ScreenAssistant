import keyboard
import pytesseract
import sys
from PyQt6 import QtCore, QtWidgets
from snippingwidget import SnippingWidget
from telegramclient import TelegramClient
from logger import Logger


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.button = QtWidgets.QPushButton()
        self.button.clicked.connect(self.activate_snipping)
        self.text = QtWidgets.QTextEdit(self)
        self.text.resize(800, 300)
        self.snipper = SnippingWidget()
        self.snipper.closed.connect(self.deactivate_snipping)
        self.telegram = TelegramClient()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def activate_snipping(self):
        self.snipper.showFullScreen()
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.CrossCursor)

    def deactivate_snipping(self):
        question = pytesseract.image_to_string(self.snipper.image)
        answer = self.telegram.send_question_and_receive_answer(question)
        Logger.log_question_and_answer(image=self.snipper.image, question=question, answer=answer)
        self.text.setText(answer.text)
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 300)
    keyboard.add_hotkey("print screen", lambda: window.button.click())
    keyboard.add_hotkey("escape", lambda: app.exit())
    sys.exit(app.exec())

# from PIL import Image, ImageGrab
# from PyQt6 import QtCore, QtGui, QtWidgets
#     def screenshot_file_name(self):
#         file_name = "screenshot"
#         file_ext = "png"
#         full_file_name = f"{file_name}.{file_ext}"
#         while 1 == 1:
#             if os.path.exists(full_file_name):
#                 self.screenshot_counter += 1
#                 full_file_name = f"{file_name} ({self.screenshot_counter}).{file_ext}"
#             else:
#                 return full_file_name
# self.screenshot_counter = 0
# import os.path
# img.save(self.screenshot_file_name())
