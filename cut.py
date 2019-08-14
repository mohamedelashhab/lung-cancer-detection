import os
import os.path

import numpy as np
import pywt

import cv2
import matplotlib.path as mplPath


def convert(string):
    try:
        a, b = string[:-1].split(' ')
    except:
        if len(string[:-1].split(' ')) == 4:
            x, a, b, y = string[:-1].split(' ')
        else:
            s, x, y, a, b, z = string[:-1].split(' ')
    return float(a), float(b)


def process_L(path_L,image_name):
    new = []
    if image_name[-3:] == 'txt':
        with open(path_L + image_name) as fi:
            content = fi.readlines()
        content = list(map(convert, content[2:-1]))
        for i in content:
            i = list(i)
            i.reverse()
            new.append(i)
        #print(np.array(new))
        return np.array(new)



def process_R(path_R,image_name):
    new = []
    if image_name[-3:] == 'txt':
        with open(path_R + image_name) as fi:
            content = fi.readlines()
            # print(content[2:-2])[0]
        content = list(map(convert, content[2:-1]))
        for i in content:
            i = list(i)
            i.reverse()
            new.append(i)
        #print(np.array(new))
        return np.array(new)




def run(points_L, points_R,path):
    a = points_L
    b = points_R
    newImage = cv2.imread(path)
    newImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    bbPath_L = mplPath.Path(a * 2)
    bbPath_R = mplPath.Path(b * 2)
    print(bbPath_R)
    for x in range(0, 2048):
        for y in range(0, 2048):
            if (bbPath_L.contains_point((x, y)) != 1 and bbPath_R.contains_point((x, y)) != 1):
                newImage[x][y] = 255;
    return newImage


def main():
    path = 'E:\\ashhab\dataset\JPCLN001.png'
    path_L = 'E:\\CAD\L\\'
    path_R = 'E:\\CAD\R\\'
    img=run(process_L(path_L,'JPCLN001.txt'), process_R(path_R,'JPCLN001.txt'), path)
    img = cv2.resize(img,(200,200))
    cv2.imshow('img',img)
    cv2.waitKey(0)
    pass


if __name__ == '__main__':
    print("**********************************************   start   ********************************************************")
    main()

'''
path_to_images = '/run/media/a4hab/1ECA933908590CB5/dataset/new/'
path_to_save_segmentation = '/run/media/a4hab/1ECA933908590CB5/sdataset'
path_L = '/run/media/a4hab/1ECA933908590CB5/dataset/L/'
path_R = '/run/media/a4hab/1ECA933908590CB5/dataset/R/'

points_L=process_L(path_L)
points_R=process_R(path_R)
print(process_L(path_L))
a = points_L['JPCLN076.png']
b = points_R['JPCLN076.png']
print(a)
img =cv2.imread('/run/media/a4hab/1ECA933908590CB5/dataset/JPCLN076.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
bbPath_L = mplPath.Path(a*2)
bbPath_R = mplPath.Path(b*2)
for x in range(0,2048):
    for y in range(0,2048):
        if (bbPath_L.contains_point((x, y))!=1 and bbPath_R.contains_point((x, y))!=1):
            img[x][y]=255;



img = cv2.resize(img,(500,500))
cv2.imshow('img',img)
cv2.waitKey(0)
'''
