import os
import time
import tkinter as Tk
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno

from face_discern import *
from face_see import *
#导入 四个模块
from face_text import *
from image_text import *

'''主界面'''
def main_GUI():

    #管理用户界面
    def user_info():
        def del_user():
            pass
        def change_user():
            pass
        def show_user():
            open_file = open('./user_name.txt','r',encoding='utf-8')
            user_name = open_file.readlines()
            if user_name == []:
                kis = '没有用户'
                li2.insert(END,kis)
                return False
            open_file.close()
            for i in range(len(user_name)):
                li2.insert(END,'用户： '+user_name[i]+'\t        id范围：'+str(i*20+1)+'~'+str((i+1)*20))
            return True
        def delall_user():
            if not askyesno('警告','确定要删除所有用户吗？\n内容包括（样本，样本名，模型）'):
                return
            open("user_name.txt",'w').close()
            path = 'face_data'
            for f in os.listdir(path):
                os.remove(path+'\\'+f)
            try:
                os.remove('.\\trainner\\trainner.yml')
            except:
                pass
            li.insert(END,'用户信息已清空')
        def re_user():
            # li2.insert(END,'排列完毕')
            user_pool.set('排列完毕')
        #用户界面GUI
        root2 = Tk()
        root2.title("用户信息")
        root2.geometry('350x200')
        root2.resizable(False,False)
        root2.configure(background='gray')
        root2.attributes("-alpha", 0.85)

        kis = '用户信息'
        user_pool = StringVar()
        user_pool.set(kis)

        li2 = Listbox(root2,width=33,listvariable=user_pool,height=10)
        li2.grid(row=0,column=0,rowspan=5)
        Show = Button(root2,text='查看用户',command=show_user)
        Show.grid(row=0,column=1,padx=20)
        Del = Button(root2,text='删除用户',bg='Gray',command=del_user)
        Del.grid(row=1,column=1,padx=20)
        Cha = Button(root2,text='修改用户',bg='Gray',command=change_user)
        Cha.grid(row=2,column=1,padx=20)
        Reu = Button(root2,text='重排编号',bg='Gray',command=re_user)
        Reu.grid(row=3,column=1,padx=20)
        Dal = Button(root2,text='清空用户',bg='red',command=delall_user)
        Dal.grid(row=4,column=1,padx=20)
        
        mainloop()
    #说明界面
    def explain_GUI():
        root = Tk()
        root.geometry('600x200')
        root.resizable(False,False)
        root.title("说明")
        sm ='*识别验证：开始验证人脸识别（前提已经训练好模型)\n\
        *安全退出：释放python所有程序，并退出程序\n\
        *训练模型：将样本图片喂给分类器中的\'识别训练\'\n\
        *照片录入：将样本图片变成灰图，并采集样本（请先完成照片路径）\n\
        *照片路径：选择照片路径，将照片[\"命名\".jpg]放进照片路径中\n\
        *样本录入：使用摄像头帧图变成灰图，并采集样本\n\
        *重新训练：重新训练人脸识别模型\n\
        *追加训练：追加训练人脸识别模型（未完成N）\n\
        *注意：图片训练时注意命名\n' 

        shuom = Label(root,text=sm,font=('微软雅黑',12),fg='red')
        shuom.pack()
        shuom.grid(sticky='N')
        mainloop()
    '''路径设置'''
    def selectPath():
        path_ = askdirectory() #使用askdirectory()方法返回文件夹的路径
        if path_ == "":
            path.get() #当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
        else:
            path_ = path_.replace("/", "\\")  # 实际在代码中执行的路径为“\“ 所以替换一下
            path.set(path_)
    '''路径打开'''
    def openPath_one():
        dir = os.path.dirname('.\\drill_img\\')
        os.system('start ' + dir)

    def openPath_two():
        dir = os.path.dirname('.\\face_data\\')
        os.system('start ' + dir)
    '''导入使用face_text.py'''
    def face_text():
        names = name.get()
        if names == "":
            li.insert(END, "请输入样本id")
            return
        else :
            x = open('user_name.txt', 'a',encoding='utf-8')
            x.write(names + '\n')
            x.close()
            li.see(END)
        try:
            main_face()
        except:
            li.insert(END, "无法连接到face_text.py")
            li.see(END)
            return 
        li.insert(END,'已完成当前样本录入:'+names)
        return True
    '''导入使用image_text.py'''
    def image_text():
        li.see(END)
        try:
            main_image()
        except:
            li.insert(END, "无法连接到image_text.py")
            return 
        li.insert(END,'已完成照片录入')
        return True
    '''导入使用face_discern.py'''
    def face_discern():
        li.see(END)
        try:
            main_discern()
        except:
            li.insert(END, "无法连接到face_discern.py")
            return 
        li.insert(END,'已完成训练模型')
        return True
    '''导入使用face_see.py'''
    def face_see():
        li.see(END)
        try:
            chos = main_see()
        except:
            return 
        li.insert(END,chos)
        li.insert(END,'已关闭人脸识别')
        li.see(END)
        return True
    '''安全退出'''
    def exit():
        if askyesno('提示','确定退出吗？'):
            os._exit(0) and root.quit()
    '''切换摄像头'''
    def video():
        r = open('./ttc/chios.txt','r',encoding='utf-8')
        a = int(r.read())
        r.close()
        f = open('./ttc/chios.txt','w',encoding='utf-8')
        if a == 0:
            f.write('1')
            f.close()
            li.insert(END,'以切换 外置摄像头')
            return a
        else:
            f.write('0')
            f.close()
            li.insert(END,'以切换 内置摄像头')
            return a
            
    #主界面    
    root = Tk()
    root.geometry('430x500')
    root.resizable(False,False)
    root.protocol("WM_DELETE_WINDOW", quit)
    root.title("OWO")

    '''容器区域'''
    path = StringVar()
    path.set('./drill_img/')
    tishi = StringVar()

    '''按钮区域'''
    Button(root,text='管理',bg='Khaki',command=lambda:user_info()).grid(row=1,column=0,sticky='W')
    Button(root,text='说明',bg='Moccasin',command= lambda: explain_GUI()).grid(row=1,column=0)
    Button(root,text='切换',bg='LightSteelBlue',command=lambda:video()).grid(row=1,column=0,sticky='E')
    Button(root,text='识别验证',bg='Skyblue',command=lambda :face_see()).grid(row=1,column=2)
    Button(root, text="安全退出",bg='Coral' ,command=lambda: exit()).grid(row=1, column=3)
    # Button(root,text='确定',command=lambda: name_get()).grid(row=2,column=1,sticky='e')
    sample_into = Button(root, text='样本录入',command=lambda: face_text())
    sample_into.grid(row=2, column=2, sticky=W, pady=4)
    sample_index = Button(root, text='样本查看',command=openPath_two)
    sample_index.grid(row=2, column=3, sticky=W, pady=4)
    Button(root, text="照片路径", command=openPath_one).grid(row=3, column=2)
    Button(root, text="照片录入", command=lambda: image_text()).grid(row=3, column=3)
    model_re = Button(root, text='重新训练',command=lambda: face_discern())
    model_re.grid(row=6, column=0,columnspan=2,ipadx=70,sticky='w')
    model_ad = Button(root, text='追加训练(未)',bg='Gray')
    model_ad.grid(row=6, column=1,columnspan=3,ipadx=70,sticky='E')

    '''标签区域'''
    Label(root, text='~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~').grid(row=0, column=0,columnspan=4,sticky='w')
    Label(root, text='👇样   本   录   入👇').grid(row=1, column=1, pady=4)
    Label(root, text="   输入样本名称:").grid(row=2, column=0,sticky=E)
    Label(root, text="   图片样本目录:").grid(row=3, column=0,sticky=E)
    Label(root, text="👇模   型   训   练👇").grid(row=5, column=1)
    Label(root, text="提示").grid(row=7, column=1)
    Label(root, text='~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~').grid(row=8, column=0,columnspan=4,sticky='w')

    '''输入框区域'''
    name = Entry(root,fg='red')
    name.grid(row=2, column=1,ipadx=30,sticky='w')
    pathx = Entry(root, textvariable=path,state="readonly")
    pathx.grid(row=3, column=1,ipadx=30,sticky='w')

    '''文本域区域'''
    li = Listbox(root, listvariable = tishi,height = 15,width=50)
    li.grid(row=9,column=0,columnspan=4) 
    '''主窗口循环'''
    root.mainloop()
    
#不可被调用主区域
if __name__ == "__main__":
    main_GUI()



    

    