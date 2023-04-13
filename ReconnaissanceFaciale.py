import cv2,os,numpy, time

def reconnaissanceFaciale(identifiant, path_dir): #return true if the face correspond with the identifiant
    id=0
    size = 2
    path = path_dir
    time_start = time.time()
    fn_haar = "haarcascade_frontalface_default.xml"
    font = cv2.FONT_HERSHEY_SIMPLEX
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer.yml')
    haar_cascade = cv2.CascadeClassifier(fn_haar)
    cam = cv2.VideoCapture(0)
    pasreconnu=True
    vretour= ""
    compteur=0
    identifiants={}
    (im_width, im_height) = (112, 92)

    for subdir in os.listdir(path):
        identifiants[id]=subdir
        id+=1
        
    while pasreconnu:
        ret, frame = cam.read()
        # Flip the image (optional)
        frame=cv2.flip(frame,1,0)
        # Convert to grayscalel
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Resize to speed up detection (optinal, change size above)
        mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))
        # Detect faces and loop through each one
        faces = haar_cascade.detectMultiScale(mini)
        
        if len(faces)>1:
            vretour = "Plusieurs visages détectés"
            pasreconnu=False
            
        for i in range(len(faces)):
            face_i = faces[i]
            
            # Coordinates of face after scaling back by `size`
            (x, y, w, h) = [v * size for v in face_i]
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (im_width, im_height))

            prediction = recognizer.predict(face_resize)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (232, 1, 253), 2)
            
            if prediction[1]<90:
                cv2.putText(frame, '%s' % (identifiants[prediction[0]]), (x+5,y-5), font, 1, (203,204,0), 2)
                cv2.putText(frame, '%.0f' %  (prediction[1]), (x+5,y+h-5), font, 1, (0,255,0), 1)
                if identifiants[prediction[0]]==identifiant:
                    compteur+=1
                    if compteur >= 5:
                        vretour= "ok"
                        pasreconnu=False
            else:
                cv2.putText(frame,'Inconnu',(x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 0, 255))

        time_current = time.time()
        if (time_current - time_start) > 60:
            pasreconnu = False
            vretour = "Temps dépassé, aucune personne reconnu"
        cv2.imshow('OpenCV', frame)
        k = cv2.waitKey(10) & 0xff
    cam.release()
    cv2.destroyAllWindows()
    return vretour

def insertLog(numPhase,identifiant,numBadge,commentaire):
    insertLogAcces(numPhase,identifiant,numBadge,commentaire)