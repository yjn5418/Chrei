import cv2,os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
 


def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=30):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)# 创建一个可以在给定图像上绘图的对象
    fontStyle = ImageFont.truetype("./ttc/simsun.ttc", textSize, encoding="utf-8")# 字体的格式
    draw.text(position, text, textColor, font=fontStyle) # 绘制文本
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)# 转换回OpenCV格式

def main_see():
    #准备好识别方法
    if not os.path.exists('trainner/trainner.yml'):
        return '模型不存在，请先进行训练'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainner/trainner.yml')
    cascade_path = "./haarshare/haarcascade_frontalface_default.xml" 
    face_cascade = cv2.CascadeClassifier(cascade_path)
    font = cv2.FONT_HERSHEY_SIMPLEX

    f = open('./user_name.txt','r',encoding='utf-8')
    names = f.readlines()
    right = len(names)*20
    r = open('ttc/chios.txt','r',encoding='utf-8')
    cam = cv2.VideoCapture(int(r.read()))
    r.close()
    while True:
        ret,img = cam.read()
        img = cv2.flip(img, 1, dst=None)#镜像翻转
        cv2.imshow('camera',img)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3,5)
        for(x,y,w,h) in faces:#进行校验
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            idnum,confidence = recognizer.predict(gray[y:y+h,x:x+w])#使用LBPH算法进行识别
            #计算出一个检验结果
            if 1 <= idnum <= right and 20 < confidence < 80:
                idum = names[(idnum-1)//20][:-1]
                confidence = round(100-confidence)
            else:
                idum = "无法识别"
                confidence = round(100-confidence)
            #输出检验结果以及用户名
            cv2.putText(img,str(confidence),(x+5,y+h-5),font,1,(176,48,96),4)
            frame=cv2AddChineseText(img,idum, (x+5,y-5),(0, 255, 0), 30)
            cv2.imshow('camera',frame)
        k = cv2.waitKey(20)
        if k == 27:
            break
    #释放资源
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main_see()