#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtWidgets import QApplication,QWidget,QColorDialog
class PaintBoard(QWidget):
	def __init__(self,parent=None):

		super().__init__()

		self.__size = QSize(224,224)
		self.__fill = QColor(0,0,0,255)
		self.__board = QPixmap(self.__size)
		self.__board.fill(self.__fill)
		self.setFixedSize(self.__size)
		self.__painter = QPainter()
		self.__pen = QPen(QColor(255,255,255,255) ,15)
		self.__pen.setCapStyle(Qt.RoundCap)
		self.__pen.setCapStyle(Qt.RoundCap)
		self.__pen.setJoinStyle(Qt.MiterJoin)
		self.__begin_point = QPoint()
		self.__end_point = QPoint()

	def clear(self):
		self.__board.fill(self.__fill)
		self.update()

	def setPenColor(self):
		color = QColorDialog.getColor(Qt.blue)
		self.__pen.setColor(color)

	def paintEvent(self, paintEvent):
		self.__painter.begin(self)
		self.__painter.drawPixmap(0,0,self.__board)
		self.__painter.end()

	def mousePressEvent(self, mouseEvent):
		if mouseEvent.button() == Qt.LeftButton:
			self.__begin_point = mouseEvent.pos()
			self.__end_point = self.__begin_point
			self.update()

	def mouseMoveEvent(self, mouseEvent):
		if mouseEvent.buttons() == Qt.LeftButton:
			self.__end_point = mouseEvent.pos()
			self.__painter.begin(self.__board)
			self.__painter.setPen(self.__pen)
			self.__painter.drawLine(self.__begin_point, self.__end_point)
			self.__painter.end()
			self.__begin_point = self.__end_point
			self.update()

	def toImage(self):
		image = self.__board.toImage()
		return image

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = PaintBoard()
    demo.show()
    sys.exit(app.exec_())