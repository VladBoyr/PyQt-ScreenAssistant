from PIL import Image, ImageGrab
from PyQt6 import QtCore, QtGui, QtWidgets


class SnippingWidget(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(SnippingWidget, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint | QtCore.Qt.WindowType.FramelessWindowHint)

        self.outsideSquareColor = "red"
        self.squareThickness = 2

        self.start_point = QtCore.QPointF()
        self.end_point = QtCore.QPointF()

        self.image = Image.new(mode='RGB', size=(1, 1), color=(255, 255, 255))

    def mousePressEvent(self, event):
        self.start_point = QtCore.QPointF(event.pos())
        self.end_point = QtCore.QPointF(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        self.end_point = QtCore.QPointF(event.pos())
        self.update()

    def mouseReleaseEvent(self, event):
        r = QtCore.QRectF(self.start_point, self.end_point).normalized()
        self.hide()
        self.image = ImageGrab.grab(bbox=r.getCoords())
        QtWidgets.QApplication.restoreOverrideCursor()
        self.closed.emit()
        self.start_point = QtCore.QPointF()
        self.end_point = QtCore.QPointF()

    def paintEvent(self, event):
        trans = QtGui.QColor(22, 100, 233)
        r = QtCore.QRectF(self.start_point, self.end_point).normalized()
        qp = QtGui.QPainter(self)
        trans.setAlphaF(0.2)
        qp.setBrush(trans)
        outer = QtGui.QPainterPath()
        outer.addRect(QtCore.QRectF(self.rect()))
        inner = QtGui.QPainterPath()
        inner.addRect(r)
        r_path = outer - inner
        qp.drawPath(r_path)
        qp.setPen(QtGui.QPen(QtGui.QColor(self.outsideSquareColor), self.squareThickness))
        trans.setAlphaF(0)
        qp.setBrush(trans)
        qp.drawRect(r)
