import numpy as np
import cv2
import matplotlib.pyplot as plt
boxScale=1
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
array=[]
cap = cv2.VideoCapture(1)
s=0
while 1:
	ret, img = cap.read()
	xx,yx,zx=img.shape
	#print(xx,yx,zx)
	acenter=(int(yx/2),int(xx/2))
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	cv2.line(img,(acenter[0],acenter[1]+300),(acenter[0],acenter[1]-300),(0,255,255),2)
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		center1=((int((x+(x+w))/2)),(int((y+(y+h))/2)))
		center=((center1[0]-x),(center1[1]-y))
		cv2.line(img,(center1[0],center1[1]+50),(center1[0],center1[1]-50),(255,255,255),2)
		roi_half=roi_color[y:center[1], x:center[0]]
		eyes = eye_cascade.detectMultiScale(roi_color)
		for (ex,ey,ew,eh) in eyes:
			if (((ex+ew)<center[0]) and (ex<center[0]) and (ey<center[1]) and ((ey+eh)>center[1])):		#left
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
				center2=(int((ex+ex+ew)/2),int((ey+ey+eh)/2))
				cv2.line(img,(center2[0]+x,center2[1]+y-10),(center2[0]+x,center2[1]+y+10),(255,0,255),5)
				eye= roi_color[ey:ey+eh, ex:ex+ew]
			elif (((ex+ew)>center[0]) and (ex>center[0]) and (ey<center[1]) and ((ey+eh)>center[1])):
				cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,255),2)
				eye= roi_color[ey:ey+eh, ex:ex+ew]
				center3=((int((ex+ex+ew)/2)),int((ey+ey+eh)/2))
				cv2.line(img,(center3[0]+x,center3[1]+y-10),(center3[0]+x,center3[1]+y+10),(255,0,255),2)
				eye= roi_color[ey:ey+eh, ex:ex+ew]
			else:
				break
	
	if(center1[0]<210):
		if(s!='l'):
			print('left')
		s='l'
	if(center1[0]>=210 and center1[0]<=420):
		if(s!='c'):
			print('center')
		s='c'
	if(center1[0]>420):
		if(s!='r'):
			print('right')
		s='r'
	
	cv2.imshow('face',img)
	#cv2.imshow('eye',eye)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break
cap.release()
cv2.destroyAllWindows()
