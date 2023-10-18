'''
识别图片的脸部坐标,转为灰图,保存用以模型训练
'''
import os,cv2
def main_image():
    c = open('./user_name.txt','r',encoding='utf-8')#存放样本id名字
    count = len(c.readlines())*20
    c.close()
    path = './drill_img'
    imagePaths = [os.path.join(path, f)for f in os.listdir(path)]#列出所有图像样本
    ima_name = [f[:-4] for f in os.listdir(path)]
    images_deceted = cv2.CascadeClassifier('./haarshare/haarcascade_frontalface_default.xml')#使用分类器
    f = open('./user_name.txt','a',encoding='utf-8')
    for imagePath,Iname in zip(imagePaths,ima_name):#依次列出每条图片名称连接
        scou = 0
        img = cv2.imread(imagePath)
        faces = images_deceted.detectMultiScale(img, 1.3,5)#返回脸坐标
        while True:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#原图片转灰图
            if faces == ():break
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))#截取脸部位置
                cv2.imshow('image',img)
                count += 1
                scou += 1
                cv2.imencode('.jpg', gray[y:y+h,x:x+w])[1].tofile("./face_data/User."+Iname+'.'+str(count)+'.jpg')#脸部位置保存
            if scou == 20:
                break
        f.write(Iname)
        f.write('\n')
        k = cv2.waitKey(1)
        
        if k==27:
            break
    f.close()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main_image()