import cv2
import os
import numpy as np

# Récupération des images d'entraînement
path = 'Images_Reco'
images = []
labels = []
label = 0
for subdir in os.listdir(path):
    subpath = os.path.join(path, subdir)
    if not os.path.isdir(subpath):
        continue
    for filename in os.listdir(subpath):
        imgpath = os.path.join(subpath, filename)
        img = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)
        print('Chargement de', imgpath)
        if img is not None:
            images.append(np.asarray(img, dtype=np.uint8))
            labels.append(label)
        else:
            print('Impossible de charger', imgpath)
    label += 1

# Entraînement du modèle
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(images, np.array(labels))

# Sauvegarde du modèle dans un fichier YAML
recognizer.save('trainer.yml')
