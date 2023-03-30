import sqlite3
from tkinter import *
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests

import cv2
import numpy as np
import time
import os

from ReconnaissanceFaciale.py import reconnaissanceFaciale
import insertLogAcces

path_image_reco = "Images_Reco"
form = Tk()

def formulaire():
    form.geometry("500x250")
    
    label = Label(form, text="BONJOUR")
    label.pack(padx=5,pady=5)
    
    valueId = StringVar()
    valueId.set("")
    identifiant = Entry(form, textvariable=valueId, width=15)
    identifiant.pack()
    
    valueMdp = StringVar()
    valueMdp.set("")
    mdp = Entry(form, textvariable=valueMdp, width=15)
    mdp.pack(padx=5,pady=5)
    
    btnOK = Button(form, text="OK",command=lambda:validation(valueId.get(),valueMdp.get()))
    btnOK.pack(side=RIGHT,padx=5,pady=5)
    
    btnCANCEL = Button(form, text="ANNULER",command=form.destroy)
    btnCANCEL.pack(side=LEFT,padx=5,pady=5)

def validation(identifiant,mdp):
    try:
        url = "https://www.btssio-carcouet.fr/ppe4/public/connect2/"+identifiant+"/"+mdp+"/infirmiere"
        req = requests.get(url)
        data = req.json()
        
        if(not 'status' in data):
            formBadge(identifiant)
        else:
            print("erreur")
        form.destroy()
    except:
        print("Erreur de validation")

def formBadge(identifiant):
    window = Tk()
    window.geometry("250x150")
    
    label = Label(window, text="Placer votre badge")
    label.pack(padx=5,pady=5)
    
    btnCANCEL = Button(window, text="Ecouter",command=lambda:validationBadge(identifiant,window))
    btnCANCEL.pack(side=LEFT,padx=5,pady=5)

def validationBadge(identifiant,window):
    reader = SimpleMFRC522()
    try:
        id, text = reader.read()
        url = "https://www.btssio-carcouet.fr/ppe4/public/badge/" + identifiant + "/"+ str(id)
        req = requests.get(url)
        data = req.json()
        
        if("true" in data["status"]):
            formRecoFaciale(identifiant)
        window.destroy()
    finally:
        GPIO.cleanup()




def formRecoFaciale(identifiant):
    window = Tk()
    window.geometry("250x150")
    
    label = Label(window, text="Bonjour "+identifiant)
    label.pack(padx=5,pady=5)
    
    btnCANCEL = Button(window, text="IOEZG",command=lambda:reconnaissanceFaciale(identifiant,path_image_reco))
    btnCANCEL.pack(side=LEFT,padx=5,pady=5)

formulaire()
    
    