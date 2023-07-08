# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 22:54:45 2023

@author: Felix Lupp
"""

import winreg
import pyautogui
import time
import PyQt5
from PyQt5 import QtWidgets as QT
from PyQt5 import QtCore as QTC
from PyQt5 import QtGui as QTG
from PyQt5.QtCore import QTimer

STATUS_PATH = "Software\\Microsoft\\Windows\\CurrentVersion\\CloudStore\\Store\\DefaultAccount\\Current\\default$windows.data.bluelightreduction.bluelightreductionstate\\windows.data.bluelightreduction.bluelightreductionstate"
STATE_VALUE_NAME = "Data"
GREY_PATH = "Software\Microsoft\ColorFiltering"
def get_night_light_state_data():
    try:
        hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STATUS_PATH, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(hKey, STATE_VALUE_NAME)
        winreg.CloseKey(hKey)

        if regtype == winreg.REG_BINARY:
            return value
    except:
        pass
    return False

def is_night_light_on():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\CloudStore\\Store\\DefaultAccount\\Current\\default$windows.data.bluelightreduction.bluelightreductionstate\\windows.data.bluelightreduction.bluelightreductionstate")
        value = winreg.QueryValueEx(key,'Data')
        winreg.CloseKey(key)
        if value[0][18] ==19:
            return False
        elif value[0][18]==21:
            return True
    except:
        pass
    return False
    
def get_greyscale_data():
    try:
        hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, GREY_PATH, 0, winreg.KEY_READ)
        active,regtype = winreg.QueryValueEx(hKey, "Active")
        winreg.CloseKey(hKey)

        if regtype == winreg.REG_DWORD:
            return bool(active)
    except:
        pass
    return False
    

def blink_reminder():
    
    
    app = QT.QApplication([])
    
    # Create the custom message box
    class CustomMessageBox(QT.QDialog):
        def __init__(self, *args, **kwargs):
            super().__init__()
            self.setWindowTitle('Pop-up Title')
            self.setFixedSize(1200, 200)
            self.setWindowFlags(QTC.Qt.FramelessWindowHint)
            self.setAttribute(QTC.Qt.WA_TranslucentBackground)
            self.setWindowFlags(QTC.Qt.FramelessWindowHint | QTC.Qt.WindowStaysOnTopHint)
    
            # Create the label
            label = QT.QLabel('!BLINK YOUR EYES!', self)
            label.setAlignment(QTC.Qt.AlignCenter)
            
            label.setStyleSheet('color: orange')
    
            # Set the label outline color
            effect = QT.QGraphicsDropShadowEffect(self)
            effect.setOffset(0, 0)
            effect.setBlurRadius(30)
            effect.setColor(QTG.QColor('blue'))
            label.setGraphicsEffect(effect)
    
            # Set the layout
            layout = QT.QVBoxLayout(self)
            layout.addWidget(label)
            
            
    
    
    font = app.font()
    font.setPointSize(90)
    app.setFont(font)
    
    # Show the message box
    app.messagebox = CustomMessageBox()
    app.messagebox.show()
    
    
    
    
    # Close the message box after 1 second
    QTimer.singleShot(3000, app.messagebox.close)
    
    app.exec_()
    
def eye_reminder():
    
    
    app = QT.QApplication([])
    
    # Create the custom message box
    class CustomMessageBox(QT.QDialog):
        def __init__(self, *args, **kwargs):
            super().__init__()
            self.setWindowTitle('Pop-up Title')
            self.setFixedSize(1200, 200)
            self.setWindowFlags(QTC.Qt.FramelessWindowHint)
            self.setAttribute(QTC.Qt.WA_TranslucentBackground)
            self.setWindowFlags(QTC.Qt.FramelessWindowHint | QTC.Qt.WindowStaysOnTopHint)
    
            # Create the label
            label = QT.QLabel('EYE EXERCISE', self)
            label.setAlignment(QTC.Qt.AlignCenter)
            
            label.setStyleSheet('color: blue')
    
            # Set the label outline color
            effect = QT.QGraphicsDropShadowEffect(self)
            effect.setOffset(0, 0)
            effect.setBlurRadius(30)
            effect.setColor(QTG.QColor('yellow'))
            label.setGraphicsEffect(effect)
    
            # Set the layout
            layout = QT.QVBoxLayout(self)
            layout.addWidget(label)
            
            
    
    
    font = app.font()
    font.setPointSize(90)
    app.setFont(font)
    
    # Show the message box
    app.messagebox = CustomMessageBox()
    app.messagebox.show()
    
    
    
    
    # Close the message box after 1 second
    QTimer.singleShot(5000, app.messagebox.close)
    
    app.exec_()




active = is_night_light_on()
while True:
    if is_night_light_on()==active and get_greyscale_data() == active:
        time.sleep(5)
    if (time.localtime(time.time()).tm_min+2)%20==0:
        eye_reminder()
        time.sleep(60)
        continue
    if time.localtime(time.time()).tm_min%5==0:
        blink_reminder()
        time.sleep(60)
        continue
    elif is_night_light_on()== (not get_greyscale_data()):        
        pyautogui.hotkey("win","ctrl","c")
        time.sleep(2)
        active = is_night_light_on()
