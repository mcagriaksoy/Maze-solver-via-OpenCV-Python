import numpy as np
import argparse
import cv2
import picamera
from matplotlib import pyplot as plt

camera = picamera.PiCamera()
camera.resolution = (640, 480)
#camera.capture(‘snapshot.jpg’, resize=(640, 480))
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

lowerBound=np.array([0,0,0])
upperBound=np.array([12,25,25])

while True:

# load the image
	img = cv2.imread(camera.capture(‘snapshot.jpg’))
#image=cv2.GaussianBlur(frame, (5,5), 3) #gaussian blur intense
	imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	imgHSV = cv2.medianBlur(img,5)
	imgHSV = cv2.GaussianBlur(frame, (5,5), 3)

	mask=cv2.inRange(imgHSV,lowerBound,upperBound)
	maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((5,5)))
	maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,np.ones((20,20)))
	
	ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
	th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\cv2.THRESH_BINARY,11,2)
	th3 = cv2.adaptiveThreshold(imgHSV,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\cv2.THRESH_BINARY,11,2)

	titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
	images = [img, th1, th2, th3]

	for i in xrange(4):
		plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
		plt.title(titles[i])
		plt.xticks([]),plt.yticks([])
	plt.show()

	#cv2.imshow("mask",mask)
	#cv2.imshow("cam",img)
	#cv2.imshow("maskClose",maskClose)
	#cv2.imshow("maskOpen",maskOpen)
	maskFinal=maskClose
	conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	cv2.drawContours(img,conts,-1,(255,0,0),3)