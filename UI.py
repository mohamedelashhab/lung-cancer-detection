from CAD import CAD
import tkinter as tk
from PIL import Image,ImageTk
import numpy as np
import cv2
from tkinter.colorchooser import askcolor

Obj = CAD()
flag=0

# system3 level3 db3  ad  xgboost
# system4 level2 sym4 dd  xgboost

system = {
    '3':('db3',3,'ad'),
    '4':('sym4',2,'dd')
}


class Photoshop(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, width="1324", height="768", bd="5", bg="red")
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Load, test):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Load)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Load(tk.Frame):
    global Obj,system
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Left_frame = tk.Frame(self, width="1024", height="768", bd="5", bg="black")
        right_frame = tk.Frame(self, width="300", height="768", bd="5", bg="blue")
        Left_frame.pack(side="left", fill="both", expand=True)

        right_frame.pack(side="right", fill="both")
        load_button = tk.Button(right_frame, text="Load Image",
                                command=lambda: self.load(parent, controller, Left_frame, right_frame))
        self.put_image(load_button, 0, 1, "load.png")
        img = cv2.imread("m.jpg")
        img = cv2.resize(img, (1024, 768))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(Left_frame, image=img)
        panel.img = img
        panel.grid(column=0, row=0, sticky="nsew")
        # load_button.grid(row=0,column=1,sticky="nsew")

    def load(self, parent, controller, left_frame, right_frame):
        global flag ,families , image_type , level
        Obj.Load()
        if flag ==0:
            fvar = tk.StringVar() #families
            kvar = tk.IntVar() #levels
            ivar = tk.StringVar() # image type
            fvar.set("xgboost")
            kvar.set(4)
            ivar.set('ad')
            #classifier = tk.Label(right_frame, text="classifier :").grid(row=1, column=0)
            classifier_list = tk.OptionMenu(right_frame, fvar,*("svm","knn","xgboost")).grid(row=1, column=1)
            #select_level = tk.Label(right_frame, text="Level :").grid(row=3, column=0)
            #level = tk.OptionMenu(right_frame, kvar, 4).grid(row=3, column=1)
            #imType = tk.Label(right_frame, text="image type :").grid(row=5, column=0)
            #imgType = tk.OptionMenu(right_frame, ivar, "ad").grid(row=5, column=1)
            segment = tk.Button(right_frame, width=10, text="segment",
                                command=lambda: self.cut(parent,controller,left_frame,Obj.process_L(Obj.path_L),Obj.process_R(Obj.path_R))).grid(row=7,column=1)
            #extract = tk.Button(right_frame, width=10, text="apply",
            #                         command=lambda: self.wavelets(parent, controller, left_frame)).grid(row=9, column=1)

            clss = tk.Button(right_frame, width=10, text="check",
                             command=lambda: self.patches(parent, controller, left_frame,Obj.image,fvar.get())    ).grid(row=11,column=1)



            image = ImageTk.PhotoImage(file="0.png")
            image = ImageTk.PhotoImage(file="1.png", width=48, height=48)
            img = self.convert_array2image(Obj.image)
            Panel = tk.Label(left_frame, image=img)
            Panel.img = img
            Panel.grid(column=0, row=0, sticky="nsew")

            flag = 1
        elif flag > 0:
            for widget in left_frame.winfo_children():
                widget.destroy()
            img = Obj.image
            img = self.convert_array2image(img)
            Panel = tk.Label(left_frame, image=img)
            Panel.img = img
            Panel.grid(column=0, row=0, sticky="nsew")


    def wavelets(self,parent,controller,left_frame):
        bool = Obj.bool

        if bool == 0 :
            if Obj.wavelet(Obj.image, system['1'][0], system['1'][1], system['1'][2]):
                for widget in left_frame.winfo_children():
                    widget.destroy()
                new_image = Obj.temp
                new_image = self.convert_array2image(new_image)
                panel = tk.Label(left_frame, image=new_image)
                panel.new_image = new_image
                panel.grid(column=0, row=0, sticky="nsew")
        else:
            if Obj.wavelet(Obj.image, system['2'][0], system['2'][1], system['2'][2]):
                for widget in left_frame.winfo_children():
                    widget.destroy()
                new_image = Obj.temp
                new_image = self.convert_array2image(new_image)
                panel = tk.Label(left_frame, image=new_image)
                panel.new_image = new_image
                panel.grid(column=0, row=0, sticky="nsew")



    def cut(self,parent,controller,left_frame,left,right):
        if Obj.run(left,right):
            for widget in left_frame.winfo_children():
                widget.destroy()
            new_image = Obj.image
            new_image = self.convert_array2image(new_image)
            panel = tk.Label(left_frame, image=new_image)
            panel.new_image = new_image
            panel.grid(column=0, row=0, sticky="nsew")



    def classify(self,parent,controller,left_frame,feature,classifier):
        Result = Obj.classify(feature,classifier)
        if Result==1:
            Obj.print_mssg("check Result","Noduled")
        else:
            Obj.print_mssg("check Result", "Non-Noduled")



    def patches(self,parent,controller,left_frame,img,classifier):
        if Obj.bool == 1 :
            if Obj.patches(img,system['4'],classifier)!=2:
                for widget in left_frame.winfo_children():
                    widget.destroy()
                new_image = Obj.marked_image
                new_image = self.convert_array2image(new_image)
                panel = tk.Label(left_frame, image=new_image)
                panel.new_image = new_image
                panel.grid(column=0, row=0, sticky="nsew")
                Obj.print_mssg("check Result", "Noduled")
            else:
                Obj.print_mssg("check Result", "Non-Noduled")
        else:
            if Obj.patches(Obj.image,system['3'],classifier)!=2:
                for widget in left_frame.winfo_children():
                    widget.destroy()
                new_image = Obj.marked_image
                new_image = self.convert_array2image(new_image)
                panel = tk.Label(left_frame, image=new_image)
                panel.new_image = new_image
                panel.grid(column=0, row=0, sticky="nsew")
                Obj.print_mssg("check Result", "Noduled")
            else:
                Obj.print_mssg("check Result", "Non-Noduled")


    def convert_array2image(self,image):
        height, width = image.shape[:2]
        if(height>768 and width>1024):
            image = cv2.resize(image,(1024,768))
        elif(height > 768):
            image = cv2.resize(image,(width,768))
        elif(width > 1024):
            image = cv2.resize(image,(1024,height))
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        return image
    def put_image(self,tkobject,row,col,path):
        image = ImageTk.PhotoImage(file=path)
        tkobject.config(image=image)
        tkobject.image = image
        tkobject.grid(row=row,column=col,sticky="ew",columnspan=1)



class test(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


app = Photoshop()
app.mainloop()
