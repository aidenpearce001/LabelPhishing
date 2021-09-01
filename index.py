from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import os
import json
from selenium import webdriver

from utils.utils import readTxt, labelFolder
from utils.info_extraction import *
from utils.screenshot import screenshot

main,_ = loadUiType('UI/MainWin.ui')

class Index(QMainWindow, main):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.label_11.setOpenExternalLinks(True)
        self.actionOpen.triggered.connect(self.browseFile)

    def browseFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', filter='*.txt')
        urls = readTxt(fname[0])
        labelFolder("images")
        labelFolder("labeled")
        self.data_info(urls[0])
        self.handel_data(urls)
        
    def handel_data(self, urls):
        ls = urls
        self.n = 0
        self.commandLinkButton.clicked.connect(lambda: self.next(self.n, urls))
        self.commandLinkButton_2.clicked.connect(lambda: self.prev(self.n, urls))
    
    def next(self, n, urls):
        label_path = 'labeled/'+urls[n].split("/")[2]+'.txt'
        data = extract(urls[n])
        data['label'] = self.comboBox.currentText()
        self.save_file(label_path, data)

        self.n = n + 1
        self.listWidget_2.clear()
        self.data_info(urls[self.n])
    
    def prev(self, n, urls):
        label_path = 'labeled/'+urls[n].split("/")[2]+'.txt'
        data = extract(urls[n])
        data['label'] = self.comboBox.currentText()
        self.save_file(label_path, data)

        self.n = n - 1
        self.listWidget_2.clear()
        self.data_info(urls[self.n])    
    
    def data_info(self, url):
        screenshot(url)
        data = extract(url)

        image_path = 'images/'+url.split("/")[2]+'.png'
        if os.path.exists(image_path) == True:
            self.label_7.setPixmap(QPixmap(image_path).scaled(580, 550))
        else:
            self.label_7.setText("Cannot screenshot this url")

        self.label_11.setText(f"<a href=\"{str(url)}\">{url}</a>")
        self.label_5.setText("{} ký tự".format(str(data["url length"])))
        if str(data["Domain Age"]) == "None":
            self.label_9.setText("{} ngày".format(0))
        else:
            self.label_9.setText("{} ngày".format(str(data["Domain Age"])))
        self.label_12.setText(str(data["Authority Certificate"]))
        
        if data["js"] == None:
            for i in range(9):
                self.listWidget_2.addItem(str(0))
        else:
            for i in list(data["js"].values()):
                self.listWidget_2.addItem(str(i))
        
    def save_file(self, path, data):
        with open(path, "w") as f:
            f.write(json.dumps(data))

def main():
    app = QApplication(sys.argv)
    window = Index()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
