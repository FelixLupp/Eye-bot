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


#adress of registriy for greyscale filter
GREY_PATH = "Software\Microsoft\ColorFiltering"


#get night light state
def is_night_light_on():
    try: #adress for nightlight registry entry
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
#get greyscale state
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
    
#function to remind you to blink (choose any message, color, size, duration of display. copy function and rename for additional reminder)
def blink_reminder():    
    app = QT.QApplication([])
    
    # Create the custom message box
    class CustomMessageBox(QT.QDialog):
        def __init__(self, *args, **kwargs):
            super().__init__()
            self.setWindowTitle('Pop-up Title')
            #set size
            self.setFixedSize(1200, 200)
            #make everything translucent exept for the message
            self.setWindowFlags(QTC.Qt.FramelessWindowHint)
            self.setAttribute(QTC.Qt.WA_TranslucentBackground)
            self.setWindowFlags(QTC.Qt.FramelessWindowHint | QTC.Qt.WindowStaysOnTopHint)
    
            # set message to display
            label = QT.QLabel('!BLINK YOUR EYES!', self)
            label.setAlignment(QTC.Qt.AlignCenter)
            #set primary color
            label.setStyleSheet('color: orange')
    
            # Set message outline offset, blur radius, color
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
    
    
    
    
    # Close the message afer 3000 ms (3 seconds)
    QTimer.singleShot(3000, app.messagebox.close)
    
    app.exec_()

#additional function, for documentaion refer to blink_reminder()
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



#initialize
active = is_night_light_on()
#main loop
while True:
    #check every 5 seconds if night light state or greyscale state has changed
    if is_night_light_on()==active and get_greyscale_data() == active:
        time.sleep(5)
    #timer for eye reminder
    if (time.localtime(time.time()).tm_min+2)%20==0:
        eye_reminder()
        time.sleep(60)
        continue
    #timer for blink reminder
    if time.localtime(time.time()).tm_min%5==0:
        blink_reminder()
        time.sleep(60)
        continue
    #use shortcut to switch greyscale state if not matching
    elif is_night_light_on()== (not get_greyscale_data()):        
        pyautogui.hotkey("win","ctrl","c")
        time.sleep(2)
        active = is_night_light_on()
