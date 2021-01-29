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
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QTextCursor

import pathlib
from stegano import lsb
from os.path import splitext

qtcreator_file = "Encryption_stegano.ui" 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

imagename = ""
limit = 400 #limit for number of characters in input text box

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.quitButton.clicked.connect(self.on_Quitclick)
        self.loadButton.clicked.connect(self.on_loadclick)        
        self.encryptButton.clicked.connect(self.on_encyptclick)
        self.textEditIN.textChanged.connect(self.updatecounter)
        self.encryptButton.setEnabled(False)
        self.textEditIN.setText('Type your message to be encypted here - limit is 400 characters')  
            
    def on_Quitclick(self): #Quit button has been pressed         
        self.close()

    def on_loadclick(self):
        print('Button select image clicked')
        self.openFileNameDialog()

    def openFileNameDialog(self):
        global imagename
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "Select file","Portable Network Graphics  Files (*.png)", options=options)
        if fileName:
            print(fileName)  
            imagename = fileName
            self.encryptButton.setEnabled(True)
            self.pixmap = QPixmap(fileName)
            scaled = self.pixmap.scaled(self.Imagelabel.size(), Qt.KeepAspectRatio)
            self.Imagelabel.setPixmap(scaled)
            imagewidth = int(self.Imagelabel.width())
            imageheight = int(self.pixmap.height()/(self.pixmap.width()/self.Imagelabel.width()))            
            self.Imagelabel.resize(imagewidth, imageheight)
            self.Imagelabel.repaint() 
            
    def on_encyptclick(self):
        print('Button encrypt clicked')
        secret = lsb.hide(imagename, self.textEditIN.toPlainText()) 

        file_name,extension = splitext(imagename)
        file_name += '-secret'
        file_name += extension

        file = pathlib.Path(file_name)
        if file.exists ():
            print ("encrypted file already exist")

            buttonReply = QMessageBox.question(self, 'Encrypted file already exist', "Do you wish to overwrite?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes: #files already exist but overwrite
                print('Overwrite file')
                secret.save(file_name)
                print("\n")
                print("Message saved to image")
            else: #files exist so don't overwrite
                print('Cancel save file')
        else:        
            secret.save(file_name)
            print("\n")
            print("Message saved to image")

    def updatecounter(self): 
        msg = self.textEditIN.toPlainText()
        global limit
        if len(msg)>limit:   
            print('Input testbox limit reached')
            TextData = msg[:limit]
            self.textEditIN.setText(TextData)  
            self.textEditIN.moveCursor(QTextCursor.End)
        msg = self.textEditIN.toPlainText()  
        self.wordcountlabel.setText(f"Characters remaining: {round(int(limit - len(msg)),0)} chars")    
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())