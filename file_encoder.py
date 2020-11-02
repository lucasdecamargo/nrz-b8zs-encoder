################################################################################
# BEFORE YOU RUN, MAKE SURE YOU HAVE THE FOLLOWING LIBRARIES INSTALLED:
# NumPy: https://numpy.org/install/
# PyQt5: https://pypi.org/project/PyQt5/
# Plotly: https://plotly.com/python/getting-started/
# ------------------------------------------------------------------------------
# Author: Lucas de Camargo Souza
# E-Mail: lucas_camargo@hotmail.com.br
# ------------------------------------------------------------------------------
# Developed and tested on Python 3.8.5 under the OS Linux Kubuntu 20.04 64 bits
################################################################################

from ui_mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot

import csv
import data_lib as dl

class FileEncoderApplication(Ui_MainWindow, QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.data = dl.GenericData()
		self.plotter = dl.PlotlyDataPlotter()
		self.setupUi(self)
		self.show()
		self.fname = ""
		self.statusbar.showMessage("Ready")

	def setupUi(self, MainWindow):
		Ui_MainWindow.setupUi(self, MainWindow)
		self.center()
		# Custom Slots
		self.pb_load.clicked.connect(self.browseSlot)
		self.pb_exportPlot.clicked.connect(self.exportPlotSlot)
		self.pb_exportBits.clicked.connect(self.exportBitSlot)
		self.pb_plot.clicked.connect(self.plotSlot)
		self.rb_textInput.clicked.connect(self.loadTextInput)
		self.rb_fileInput.clicked.connect(self.loadFile)
		self.le_textInput.returnPressed.connect(self.returnPressedSlot)
		self.le_textInput.textChanged.connect(self.loadTextInput)

	@pyqtSlot( )
	def loadFile(self):
		self.statusbar.showMessage("Reading file data...")
		self.data = dl.DataFile(self.fname)
		self.data.load()
		self.statusbar.showMessage("File loaded.", 3000)

	@pyqtSlot( )
	def loadTextInput(self):
		self.statusbar.showMessage("Reading text input data...")
		text = self.le_textInput.text()
		self.data = dl.DataString(text)
		self.statusbar.showMessage("Text data loaded.", 1000)

	@pyqtSlot( )
	def browseSlot(self):
		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
						None,
						"Load File",
						"",
						"All Files (*)",
						options=options)
		if fileName:
			self.statusbar.showMessage("Loading file: " + str(fileName))
			self.fname = str(fileName)
			self.loadFile()
			self.statusbar.showMessage("File loaded: " + fileName,5000)

	@pyqtSlot( )
	def exportPlotSlot(self):
		if(self.data.empty()):
			return self.warningMsgBox("No data!")

		if(not self.cb_nrz.isChecked() and not self.cb_digitalBits.isChecked() 
			and not self.cb_b8zs.isChecked()):
			return self.warningMsgBox("No encoding options set! Please set at least one.")

		self.loadPlot()

		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
						None,
						"Export Plot",
						"",
						"HTML Files (*.html)",
						options=options)

		if fileName:
			if(fileName[-5:] != ".html"):
				fileName +=  ".html"
			self.statusbar.showMessage("Exporting file: " + str(fileName))
			self.plotter.write_html(fileName)
			self.statusbar.showMessage("Plot file exported to: " + fileName, 5000)

	@pyqtSlot( )
	def exportBitSlot(self):
		if(self.data.empty()):
			return self.warningMsgBox("No data!")

		if(not self.cb_nrz.isChecked() and not self.cb_digitalBits.isChecked() 
			and not self.cb_b8zs.isChecked()):
			return self.warningMsgBox("No encoding options set! Please set at least one.")

		options = QtWidgets.QFileDialog.Options()
		options |= QtWidgets.QFileDialog.DontUseNativeDialog
		fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
						None,
						"Explort Bitstream",
						"",
						"CSV Files (*.csv)",
						options=options)

		if fileName:
			if(fileName[-4:] != ".csv"):
				fileName +=  ".csv"
			self.statusbar.showMessage("Exporting file: " + str(fileName))
			with open(fileName, 'w', newline='') as csvfile:
				if(self.cb_digitalBits.isChecked()):
					csvfile.write("RAW; " + str(self.data.raw())+"\n")				
				if(self.cb_nrz.isChecked()):
					csvfile.write("NRZ; " + str(self.data.nrz_unipolar())+"\n")
				if(self.cb_b8zs.isChecked()):
					csvfile.write("B8ZS; " + str(self.data.b8zs())+"\n")
			self.statusbar.showMessage("Bitstream file exported to: " + fileName, 5000)

	@pyqtSlot( )
	def plotSlot(self):
		if(self.data.empty()):
			return self.warningMsgBox("No data!")

		if(not self.cb_nrz.isChecked() and not self.cb_digitalBits.isChecked() 
			and not self.cb_b8zs.isChecked()):
			return self.warningMsgBox("No encoding options set! Please set at least one.")

		self.loadPlot()		
		html = self.plotter.to_html()
		self.webView.setHtml(html)
		# self.statusbar.showMessage("Data plotted.", 5000)

	@pyqtSlot( )
	def returnPressedSlot(self):
		self.loadTextInput()
		self.plotSlot()

	def warningMsgBox(self, text):
		msgDialog = QtWidgets.QMessageBox()
		msgDialog.setIcon(QtWidgets.QMessageBox.Warning)
		msgDialog.setWindowTitle("Warning!")
		msgDialog.setText(text)
		msgDialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
		msgDialog.exec_()

	def center(self):
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def loadPlot(self):
		del self.plotter
		self.plotter = self.plotter = dl.PlotlyDataPlotter()
		
		if(self.cb_digitalBits.isChecked()):
			self.plotter.add_data(self.data.raw(), "Raw")
		
		if(self.cb_nrz.isChecked()):
			self.plotter.add_data(self.data.nrz_unipolar(), "NRZ")

		if(self.cb_b8zs.isChecked()):
			self.plotter.add_data(self.data.b8zs(), "B8ZS")

		self.statusbar.showMessage("Plotting data...")
		self.plotter.plot()
		self.statusbar.showMessage("Loading HTML data. This may take a while depending on the file size...", 3000)


from PyQt5 import QtWebKitWidgets

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	# MainWindow = QtWidgets.QMainWindow()
	ui = FileEncoderApplication()
	# ui.setupUi(MainWindow)
	# MainWindow.show()
	sys.exit(app.exec_())
