import cv2,time

def get_image(count,face_id,fDE,cap):
    sou = 0
    liucha = 0
    while True:      
        success,img = cap.read() #从摄像头读取图片
        img = cv2.flip(img, 1, dst=None)#镜像翻转
        cv2.imshow('image',img)
        if success is True:gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #转为灰度图片，减少程序符合，提高识别度
        else:break
        faces = fDE.detectMultiScale(gray, 1.3,5)#检测人脸坐标,并缩放至1.3倍

        # if faces == ():continue
        liucha += 1
        if liucha%2!=0:continue
        for (x, y, w, h) in faces: #框选人脸，for循环保证一个能检测的实时动态视频流
            cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))
            count += 1  
            sou += 1
            cv2.imencode('.jpg', gray[y:y+h,x:x+w])[1].tofile("./face_data/User."+face_id+'.'+str(count)+'.jpg')#保存图像，把灰度图片看成二维数组来检测人脸区域
            cv2.imshow('image',img) #显示图片
        
        k = cv2.waitKey(1)   #保持画面的连续。waitkey方法保证画面的收放          
        if k == 27: #按下esc键退出
            cv2.destroyWindow('image')
            break
        elif sou >= 20: #得到30个样本后退出摄像
            cv2.destroyWindow('image')
            print(face_id,'样本已采集完成')
            time.sleep(2)
            break
    return count

def main_face():
    r = open('./user_name.txt','r',encoding='utf-8')
    lenr = r.readlines()
    try:
        face_id = lenr[-1][:-1]
    except:
        # print('无样本id')
        exit()

    count = (len(lenr)-1)*20  #计数样本编号
    r.close()

    # print('开始采集人脸样本')
    r = open('./ttc/chios.txt','r',encoding='utf-8')
    cap = cv2.VideoCapture(int(r.read())) #打开摄像头，0为内置摄像头，1为外置摄像头
    r.close()
    face_detector = cv2.CascadeClassifier('./haarshare/haarcascade_frontalface_default.xml') #选择人脸分类器

    get_image(count,face_id,fDE=face_detector,cap=cap)

    #关闭摄像头，释放资源
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main_face()