import cv2, sys, numpy, os
size = 4
fn_haar = 'haarcascade_frontalface_default.xml'
fn_dir = 'Images_Reco'
count_max = 30
try:
    print("Identifiant de l'infirmière")
    fn_name = input()
    if len(fn_name)==0:
        print("Vous devez fournir un identifiant valide !")
        sys.exit(0)       
    print("Nom du dossier des Photos, enter si 'Photos'")
    fn_dir1 = input()
    if len(fn_dir1)>0:
        fn_dir=fn_dir1
    print("Nombre de photos, par défaut 30 enter si ok")
    count_max1=input()
    if len(count_max1)>0:
        count_max=int(str(count_max1)) 
except:
    print("Erreur de saisie !")
    sys.exit(0)
path = os.path.join(fn_dir, fn_name)
if not os.path.isdir(path):
    os.mkdir(path)
(im_width, im_height) = (112, 92)
haar_cascade = cv2.CascadeClassifier(fn_haar)
webcam = cv2.VideoCapture(0)

# récupérant le dernier numéro de photos +1 car la sauvegarde des nom de photos est n.png,
# Pour chaque nom de fichier n on trouve la position du . et on extrait jusqu'à la position du .
#  sorted trie la list en descendant
# [-1] récupère le dernier et ajoute 1
#pour comprendre :
#for n in os.listdir(path):
    #print(n)
    #print(n.find('.'))
    #print(n[:n.find('.')])
    #print(int(n[:n.find('.')]))
pin=sorted([int(n[:n.find('.')]) for n in os.listdir(path)
     if n[0]!='.' ]+[0])[-1] + 1
#print("pin="+str(pin))
# Message
print("\n\033[94mLe programme va enregistrer "+str(count_max)+" photos. \
Veuillez bouger la tête pour prendre des photos de face différenciées.\033[0m\n")

# Boucle sur le nombre de photos attentues
count = 0
pause = 0

while count < count_max:

    # Boucle en attendant que la caméra soit ok
    rval = False
    while(not rval):
        # ouvre une fenetre pour le flux caméra
        (rval, frame) = webcam.read()
        if(not rval):
            print("Problème ouverture caméra. Tentative...")

    # Get image size
    height, width, channels = frame.shape

    # Flip frame
    frame = cv2.flip(frame, 1, 0)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Scale down for speed
    mini = cv2.resize(gray, (int(gray.shape[1] / size), int(gray.shape[0] / size)))

    # Detect faces
    faces = haar_cascade.detectMultiScale(mini)

    # We only consider largest face
    faces = sorted(faces, key=lambda x: x[3])
    if faces:
        face_i = faces[0]
        (x, y, w, h) = [v * size for v in face_i]

        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))

        # Dessine un rectangle et écrit l'identifiant
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(frame, fn_name, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,
            1,(0, 255, 0))

        # Ne prends pas en compte les faces trop petites
        if(w * 6 < width or h * 6 < height):
            print("Face trop petite")
        else:

            # To create diversity, only save every fith detected image
            if(pause == 0):

                print("Sauvegarde de la photo "+str(count+1)+"/"+str(count_max))

                # Save image file
                cv2.imwrite('%s/%s.png' % (path, pin), face_resize)

                pin += 1
                count += 1

                pause = 1

    if(pause > 0):
        pause = (pause + 1) % 5
    cv2.imshow('OpenCV', frame)
    key = cv2.waitKey(10)
    # si touche echap alors on stoppe la boucle !
    if key == 27:
        break
webcam.release()
cv2.destroyAllWindows()