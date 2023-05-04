import cv2
import sys
from datetime import datetime
from time import sleep

i=0

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

video_capture = cv2.VideoCapture(0)

while True and i < 50:
    if not video_capture.isOpened():
        print("erreur vidéo")
        break;
    
    ret, frame = video_capture.read()
    flipframe = cv2.flip(frame,1)
    gray = cv2.cvtColor(flipframe, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(80, 80),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(flipframe, (x, y-50), (x+w, y+30+h), (0, 255, 0), 2)
        cv2.imwrite("Images_Reco/jeanne/image_"+str(i)+".jpg",flipframe[y-50:y+30+h,x:x+w])
        sleep(0.5)
        i = i+1
    
    cv2.imshow("Vidéo", flipframe)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
