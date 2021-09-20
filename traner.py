import os 
import cv2
import numpy as np
from PIL import Image
recognizer=cv2.face.LBPHFaceRecognizer_create()
path="AHM"
def get_images_and_ides(path):
    image_paths=[os.path.join(path, f) for f in os.listdir(path)]
       
    faces=[]
    IDs=[]
    for image_path in image_paths:
        face_Img=Image.open(image_path).convert("L")
        faceNP=np.array(face_Img, "uint8")
        ID_people=1#int(os.path.split(image_path)[-1].split(".")[0])
        faces.append(faceNP)
        IDs.append(ID_people)
        cv2.imshow("training", faceNP)
        cv2.waitKey(10)
    return np.array(IDs), faces
ids,faces =get_images_and_ides(path)  
recognizer.train(faces, np.array(ids)) 
recognizer.save("recognizer/trainingData.yml")
cv2.destroyAllWindows()    
