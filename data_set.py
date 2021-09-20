
import os 
import cv2
import numpy as np
from PIL import Image
path="ahm"

face_detection= cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

rec=cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer\\trainingData.yml")

def get_images_and_ides(path):
    image_paths=[os.path.join(path, f) for f in os.listdir(path)]
       
    faces=[]
    IDs=[]
    for image_path in image_paths:
        face_Img=Image.open(image_path).convert("L")
        gray=np.array(face_Img, "uint8")
        #gray=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        faces=face_detection.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            #cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
            id, conf=rec.predict(gray[y:y+h, x:x+w]) 
            print(id)
faces =get_images_and_ides(path)  