import os
import cv2
import numpy as np
from PIL import Image


def get_images_and_labels(path,detector):#图片的命名格式必须为User.id.sampleNum
    image_paths = [os.path.join(path,f) for f in os.listdir(path)]
    face_samples = []
    ids = []
    for image_path in image_paths:
        img = Image.open(image_path).convert('L')#L为灰度图,RGB为彩色图
        img_np = np.array(img,'uint8')#将图片转化为数组
        if os.path.split(image_path)[-1].split(".")[-1] != 'jpg':
            continue
        id = int(os.path.split(image_path)[-1].split(".")[2])#获取id
        faces = detector.detectMultiScale(img_np)
        for(x,y,w,h) in faces:#将获取的图片和id添加到list中   
            face_samples.append(img_np[y:y+h,x:x+w])
            ids.append(id)
    return face_samples,ids
def main_discern():
    path = 'face_data'
    recog = cv2.face.LBPHFaceRecognizer_create()#初始化识别的方法
    detector = cv2.CascadeClassifier('./haarshare/haarcascade_frontalface_default.xml')#调用人脸分类器
    faces,ids = get_images_and_labels(path,detector)#调用函数并将数据喂给识别器训练
    recog.train(faces,np.array(ids))#训练模型
    recog.save('./trainner/trainner.yml')#保存模型

if __name__=="__main__":
    main_discern()

