import cv2
def draw_label(img, label):
    cv2.circle(img, label, 55, (0, 0, 255))
    return img
img=cv2.imread("E:\\train\JPCLN021.png")
img = draw_label(img,(50,100))
cv2.imshow('m',img)
cv2.waitKey(0)

