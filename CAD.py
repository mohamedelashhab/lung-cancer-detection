from PIL import Image
from PIL import ImageTk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
import cv2
import numpy as np
import re
import os
import os.path
import pywt
from sklearn.feature_selection import VarianceThreshold
import matplotlib.path as mplPath
from sklearn import preprocessing, cross_validation, neighbors , svm
import pandas as pd
from xgboost import XGBClassifier
import pickle



def stretch(image):
    image = cv2.resize(image, (1024, 768))
    return image



class CAD:
    def __init__(self):
        self.bool=0
        self.clf = None
        self.path=None
        self.image=None
        self.feature=None
        self.temp=None
        self.image_name=None
        self.result=None
        self.label=None
        self.marked_image=None
        self.path_L = "L\\"
        self.path_R = "R\\"
        self.info=self.Read_info('CLNDAT_EN.txt')



    def print_mssg(self,error,error_type):
        tkMessageBox.showinfo(error, error_type)

    def Load(self):
        r_image = re.compile(r".*\.(jpg|png|gif|JPG|PNG|GIF|tiff|TIFF)$")
        while True:
            try:
                self.path = tkFileDialog.askopenfilename(initialdir = "E:\\ashhab\dataset")
                if not self.path:
                    break
                elif not r_image.match(self.path):
                    raise Exception("Select An Image")
                _, self.image_name = os.path.split(self.path)
                self.image = cv2.imread(self.path)
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                self.marked_image=self.image
                self.bool=0
                return True
            except Exception as error:
                self.print_mssg("File Type Error",error)

    def wavelet(self,img, mode='db1', level=6, img_type='ad'):
        try:
            Coefficients = pywt.wavedecn(img, mode, level=level)
            Result = Coefficients[1][img_type]
            feature = Result.ravel()
            self.feature=np.array([feature])

            return True
        except Exception as error:
            self.print_mssg("No features Returned",error)

    def convert(self,string):
        try:
            a, b = string[:-1].split(' ')
        except:
            if len(string[:-1].split(' ')) == 4:
                x, a, b, y = string[:-1].split(' ')
            else:
                s, x, y, a, b, z = string[:-1].split(' ')

        return float(a), float(b)

    def process_L(self,path_L):
        image_name = self.image_name
        image_name = image_name[:-3] + 'txt'
        new = []
        if image_name[-3:] == 'txt':
            with open(path_L + image_name) as fi:
                content = fi.readlines()
            content = list(map(self.convert, content[2:-1]))
            for i in content:
                i = list(i)
                i.reverse()
                new.append(i)

            return np.array(new)

    def process_R(self,path_R):
        image_name = self.image_name
        image_name = image_name[:-3]+'txt'
        new = []
        if image_name[-3:] == 'txt':
            with open(path_R + image_name) as fi:
                content = fi.readlines()
                # print(content[2:-2])[0]
            content = list(map(self.convert, content[2:-1]))
            for i in content:
                i = list(i)
                i.reverse()
                new.append(i)

            return np.array(new)

    def run(self,points_L, points_R):
        if self.bool==1:
            self.print_mssg("information message","already segmented")
            return
        a = points_L
        b = points_R

        newImage = self.image
        bbPath_L = mplPath.Path(a * 2)
        bbPath_R = mplPath.Path(b * 2)
        for x in range(0, 2048):
            for y in range(0, 2048):
                if (bbPath_L.contains_point((x, y)) != 1 and bbPath_R.contains_point((x, y)) != 1):
                    newImage[x][y] = 255;
        self.image = 255-newImage
        self.bool=1
        return True

    def classify(self, feature,classifier):
        self.clf=None
        if self.bool==1:
            #system2
            self.clf = pickle.load(open('Data\{}_4.pickle'.format(classifier), 'rb'))
        else:
            #system1
            self.clf=pickle.load(open('Data\{}_3.pickle'.format(classifier), 'rb'))
        feature=self.feature
        return self.clf.predict(feature)

    def patches(self, img,system,classifier):
        self.marked_image=np.array(self.image)
        counter = 0
        img = self.image
        width, height = 0, 0
        while height + 64 <= img.shape[0]:
            width = 0
            while width + 64 <= img.shape[1]:
                new = img[width:width + 64, height:height + 64]
                width = width + 64
                if np.count_nonzero(new == 0) == 0:
                    # cv2.imshow('new',new)
                    # cv2.waitKey(0)
                    self.temp=new
                    self.wavelet(self.temp,system[0],system[1],system[2])

                    if self.classify(self.feature,classifier)==1:
                        counter=counter+1
                        #print("**************** counter ************ = "+str(counter))
                        self.label=(height+64,width+64)
                        #print(self.label)
                        self.draw_label(self.label,(255,0,255))
            height = height + 64
        try:
            self.draw_label(self.info[self.image_name],(0,0,255))
        except:
            return 0
        return 0

    def draw_label(self,label,color):
        cv2.circle(self.marked_image,label,80,color,thickness=5)

    def Read_info(self,file):
        info={}
        with open(file) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        for i in content:
            width = int(i.split('\t')[5])
            height = int(i.split('\t')[6])
            name = str(i.split('\t')[0][:-3]) + 'png'
            info[name] = (width, height)
        return info




