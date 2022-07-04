import cv2
import numpy as np

#全局变量
RECOGNIZER=cv2.face.LBPHFaceRecognizer_create()
PASS_CONF=45
FACE_CASCADE=cv2.CascadeClassifier('C://Users/Administrator.DESKTOP-RI02F1I/AppData/Roaming/Python/Python39/site-packages/cv2/data/haarcascade_frontalface_default.xml')

#训练识别器
def train(photos,labels):
    RECOGNIZER.train(photos,np.array(labels))

#判断图像中是否有正面人脸
def found_face(gray_img):
    faces=FACE_CASCADE.detectMultiScale(gray_img,1.15,4)
    return len(faces)>0

#识别器识别图像中的人脸
def recognise_face(photo):
    label,confidence=RECOGNIZER.predict(photo)
    if confidence>PASS_CONF:
        return -1
    return label