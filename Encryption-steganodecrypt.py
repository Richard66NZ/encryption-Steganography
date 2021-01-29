# -*- coding: utf-8 -*-
"""
Steganography is the science of writing hidden messages in such a way that no one, apart from the sender and intended 
recievert, suspects the existence of the message (i.e. security through obscurity). This script only hides messages,
without encryption. However it can be modified easily to hide an encrypted message if necessary.

The following script is not intended as a full application, but just a demonstration of the technique. Use script 
Encryption-stegano.py to select an image file (PNG only), type a plaintext message in the text box and press 
'Encrypt and Save' button. Original PNG file will be saved to the same directory with '-secret' appended to filename.

Then using script Encryption-steganodescrypt.py press button 'Select Image and Descrypt' and choose a PNG file that
has embedded message. Message should be displayed as plaintext.

@date: 30 January 2021

This source code is provided by Richard J Smith 'as is' and 'with all faults'. The provider makes no 
representations or warranties of any kind concerning the safety, suitability, inaccuracies, 
typographical errors, or other harmful components of this software.
"""

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap

from stegano import lsb

qtcreator_file = "Encryption_stegano-decrypt.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

imagename = ""

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.quitButton.clicked.connect(self.on_Quitclick)
        self.loadButton.clicked.connect(self.on_loadclick)        
        self.textEditIN.setText('')  
            
    def on_Quitclick(self): #Quit button has been pressed         
        self.close()

    def on_loadclick(self):
        print('Button select image clicked')
        self.openFileNameDialog()

    def openFileNameDialog(self):
        global imagename
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "Load a file", "Portable Network Graphics Files (*.png)", options=options)
        if fileName:
            self.loadButton.setEnabled(False)
            print(fileName)  
            imagename = fileName
    
            self.textEditIN.setText('')  
            self.textEditIN.repaint() 
            pixmap = QPixmap(fileName)
            self.Imagelabel.setPixmap(pixmap)
            
            clear_message = lsb.reveal(fileName)
            print("\n")
            print("Message extracted from image - ", clear_message)
            self.textEditIN.setText(clear_message)  
            self.loadButton.setEnabled(True)
            self.loadButton.repaint() 
        self.textEditIN.repaint()  
            
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())