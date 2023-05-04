from tkinter import *
from mfrc522 import SimpleMFRC522
import requests, time, RPi.GPIO as GPIO
import microbit

from ReconnaissanceFaciale import reconnaissanceFaciale
from insertLogAcces import insertLogAcces

widgets = []
window = Tk()
window.title("Authentification - AP4")

width = 350
height = 180
x = (window.winfo_screenwidth()/2) - (width/2)
y = (window.winfo_screenheight()/2) - (height/2)
window.geometry('%dx%d+%d+%d' % (width,height,x,y))

VALID = microbit.Image.YES
INVALID = microbit.Image.NO

path_image_reco = "Images_Reco"

def formulaire():
    labelBienvenue = Label(window, text="Bienvenue !")
    labelBienvenue.pack(padx=5,pady=5)
    
    valueId = StringVar()
    valueId.set("")
    entryId = Entry(window, textvariable=valueId, width=15,font=("Helvetica",15))
    entryId.pack()
    
    valuePassword = StringVar()
    valuePassword.set("")
    entryPassword = Entry(window, textvariable=valuePassword, width=15,show="*",font=("Helvetica",15))
    entryPassword.pack(padx=5,pady=5)
    
    btnOk = Button(window, text="Ok",command=lambda:validation(valueId.get(),valuePassword.get()),width=10)
    btnOk.pack(side=RIGHT,padx=5,pady=5)
    
    btnCancel = Button(window, text="Quitter",command=lambda:window.destroy(),width=10)
    btnCancel.pack(side=LEFT,padx=5,pady=5)
    
    widgets.append(labelBienvenue)
    widgets.append(entryId)
    widgets.append(entryPassword)
    widgets.append(btnOk)
    widgets.append(btnCancel)
    
    window.mainloop()

def validation(identifiant,mdp):
    try:
        url = "https://www.btssio-carcouet.fr/ppe4/public/connect2/"+identifiant+"/"+mdp+"/infirmiere"
        payload = requests.get(url).json()
        if(not 'status' in payload):
            destroyWidgets()
            microbitShow(VALID)
            formBadge(identifiant)
        else:
            insertLog("1",identifiant,"0","Mauvaise combinaison login/password")
            microbitShow(INVALID)
    except Exception as s:
        print("Erreur de validation",s)

def formBadge(identifiant):
    labelBienvenue = Label(window, text="Bonjour "+identifiant+" !")
    labelBienvenue.pack()
    
    cptText = StringVar()
    cptText.set("")
    labelCpt = Label(window, textvariable=cptText)
    labelCpt.pack()
    
    widgets.append(labelBienvenue)
    widgets.append(labelCpt)
    
    reader = SimpleMFRC522()
    try:
        timer = time.time()
        id, text = None,None
        while time.time() - timer < 10:
            id, text = reader.read_no_block()
            if id is not None:
                break
            time.sleep(0.1)
            print(time.time() - timer)
        url = "https://www.btssio-carcouet.fr/ppe4/public/badge/" + identifiant + "/"+ str(id)
        payload = requests.get(url).json()
        
        if("true" in payload["status"]):
            destroyWidgets()
            microbitShow(VALID)
            formRecoFaciale(identifiant,str(id))
        else:
            insertLog("2",identifiant,str(id),"Mauvaise combinaison login/badge, temps écoulé ou erreur dans la requête API")
            microbitShow(INVALID)
    finally:
        GPIO.cleanup()

def formRecoFaciale(identifiant,idBadge):
    labelBienvenue = Label(window, text="Identifiant : "+identifiant)
    labelBienvenue.pack()
    
    labelReco = Label(window, text="Chargement...")
    labelReco.pack()
    
    btnCancel = Button(window, text="Quitter",command=lambda:window.destroy(),width=10)
    btnCancel.pack(side=LEFT,padx=5,pady=5)
    
    widgets.append(labelBienvenue)
    widgets.append(labelReco)
    widgets.append(btnCancel)
    
    val = reconnaissanceFaciale(identifiant,path_image_reco)
    if(val == "ok"):
        destroyWidgets()
        microbitShow(VALID)
        print("========*========\nAUTHENTIFICATION REUSSIE !\n========*========")
        window.after(2000,window.destroy)
    else:
        microbitShow(INVALID)
        insertLog("3",identifiant,idBadge,val)

def insertLog(numeroPhase,nom,numPhase,commentaire):
    window.destroy()
    insertLogAcces(numeroPhase,nom,numPhase,commentaire)

def destroyWidgets():
    for widget in widgets:
        widget.destroy()
    widgets.clear()
    
def microbitShow(image):
    microbit.display.show(image)
    microbit.sleep(2000)
    microbit.display.clear()

formulaire()