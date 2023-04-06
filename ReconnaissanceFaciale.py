def reconnaissanceFaciale(identifiantAReconnaitre,path_dir):
    try:
        # Chargement du modèle d'entraînement
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer.yml')

        # Chargement du classificateur de visages
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Initialisation du flux vidéo
        cap = cv2.VideoCapture(0)

        # Initialisation des variables pour le renforcement de la confiance
        current_id = identifiantAReconnaitre
        confidence_threshold = 90
        confidence_counter = 0
        name = 'Inconnu'
        path = path_dir
        names = {}
        pasreconnu = True
        id=0

        for subdir in os.listdir(path):
            names[id]=subdir
            id+=1

        while pasreconnu:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

            if len(faces)>1:
                pasreconnu = False
            # Reconnaissance des visages détectés
            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                label, confidence = recognizer.predict(roi)
                if confidence < confidence_threshold:
                    name = "Personne {}".format(names[label])
                    if current_id == names[label]:
                        confidence_counter += 1
                        print(confidence_counter+" -> Reconnu :"+names[label])
                        if confidence_counter >= 5:
                            pasreconnu = False
                else:
                    name = "Inconnu"
                    
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(img, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,141,247), 2)
                cv2.putText(img, str(int(confidence))+"%", (x, y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (88,181,247), 2)

            cv2.imshow('Reconnaissance de visages', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                pasreconnu = False

        cap.release()
        cv2.destroyAllWindows()
        return "OK"
    except:
        print("Erreur")