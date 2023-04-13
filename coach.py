import cv2
import os
import numpy

def Coach(): #return true if the face correspond with the name, else false
    size = 2
    fn_haar = "haarcascade_frontalface_default.xml"
    fn_dir = 'Images_Reco'
    font = cv2.FONT_HERSHEY_SIMPLEX

    (images, lables, names, id) = ([], [], {}, 0)
    for (subdirs, dirs, files) in os.walk(fn_dir):
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(fn_dir, subdir)
            for filename in os.listdir(subjectpath):
                f_name, f_extension = os.path.splitext(filename)
                if(f_extension.lower() not in ['.png','.jpg','.jpeg','.gif','.pgm']):
                    continue
                path = subjectpath + '/' + filename
                lable = id
                images.append(numpy.asarray(cv2.imread(path, 0), dtype=numpy.uint8))
                #images.append(cv2.imread(path, 0))
                lables.append(int(lable))
            id += 1
    (im_width, im_height) = (112, 92)

    # Create a Numpy array from the two lists above

    model = cv2.face.LBPHFaceRecognizer_create()

    model.train(images, numpy.array(lables))

    model.save('trainer.yml')

Coach()


