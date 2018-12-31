import cv2
import numpy as np
import matplotlib.pyplot as plt
cap = cv2.VideoCapture('lane.mp4')
ww=0
while True:
	array1=[]
	array2=[]
	array3=[]
	_, img = cap.read()
	(xy,yx,zx)=img.shape
	cv2.imshow("Image", img)
	pts1 = np.float32([[0,100],[640,100],[0,300],[640,300]])
	pts2 = np.float32([[0,0],[640,0],[0,300],[640,300]])
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(img,M,(640,300))
	'''pts1 = np.float32([[200,450],[1200,450],[200,650],[1200,650]])
	pts2 = np.float32([[0,0],[540,0],[0,380],[540,380]])
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(img,M,(540,380))'''
	kernel = np.ones((5,5),np.uint8)
	erosion = cv2.erode(dst,kernel,iterations = 1)
	dilation = cv2.dilate(erosion,kernel,iterations = 1)
	dilation = cv2.dilate(dilation,kernel,iterations = 1)
	opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
	closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
	#plt.subplot(121),plt.imshow(img),plt.title('Input')
	#plt.subplot(122),plt.imshow(dst),plt.title('Output')
	#plt.show()
	gray = cv2.cvtColor(closing, cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray, 75, 150)
	lines = cv2.HoughLinesP(edges, 1, np.pi/360, 1, maxLineGap=1)
	
	c=dst
	x1=20
	x2=520
	y1=130
	y2=350
	c = cv2.rectangle(c, (x1,y1), (x2,y2), (0,255,0), 2)
	l1=int((x1+x2)/2)
	l2=int((y1+y2)/2) 
	center=(l1,l2)
	#print(center)
	a=int((center[0]+x1)/2)
	b=int((center[0]+x2)/2)
	d1=int(x1+30)
	d2=int(center[0]-30)
	#print(d2)
	d3=int(center[0]+30)
	d4=int(x2-30)
	d5=int(center[1]+15)
	d6=int(center[1]-15)
	#print(center,a,b,d1,d2,d3,d4,d5,d6)
	font=cv2.FONT_HERSHEY_SIMPLEX
	c = cv2.line(c, (d1,center[1]), (d2,center[1]), (0,0,255),2)
	c = cv2.line(c, (d3,center[1]), (d4,center[1]), (0,0,255),2)
	c = cv2.line(c, (center[0],d5,), (center[0],d6), (255,255,255),2)
	c = cv2.line(c, (d1,d5,), (d1,d6), (255,0,0),2)
	c = cv2.line(c, (d2,d5,), (d2,d6), (255,0,0),2)
	c = cv2.line(c, (d3,d5,), (d3,d6), (255,0,0),2)
	c = cv2.line(c, (d4,d5,), (d4,d6), (255,0,0),2)
	font=cv2.FONT_HERSHEY_SIMPLEX
	for line in (lines):
		x3, y3, x4, y4 = line[0]
		if ((x1+50<=x3<center[0]) and (y1<=y3<=y2)):
			cv2.line(dst, (x3, y3), (x4, y4), (150, 255, 0), 2)
		elif ((center[0]<x3<=x2-50) and (y1<=y3<=y2)):
			cv2.line(dst, (x3, y3), (x4, y4), (150, 255, 0), 2)
	
	y=center[1]
	i1=center[0];
	while(i1>=0):
		w=c[y,i1]
		if (w[0]==150 and w[1]==255 and w[2]==0):
			det1=i1
			#print(det)
			dis1=center[0]-det1
			#print(dis1)
			cv2.line(dst, (i1,y), (i1, y), (0, 0, 0), 2)
			break
		i1=i1-1
	for i in range(center[0],540):
		w=c[y,i]
		if (w[0]==150 and w[1]==255 and w[2]==0):
			det2=i
			dis2=det2-center[0]
			cv2.line(dst, (i, y), (i, y), (0, 0, 0), 2)
			break

	if (((a-15)<= i1 <=(a+15)) or ((b-15)<= i <=(b+15))):					#for forward
		if (ww!='f'):
			ww='f';
			print("forward")
			c = cv2.rectangle(c, (center[0]-15,center[1]-50), (center[0]+15,center[1]+50), (0,0,0), 2)

	elif (((a+15)< i1 <=(d2)) or ((b+15)< i <=(d4))):
		if (ww!='l'):
			ww='l';
			print("left")
		if (((d2)<= i1 <(d2-20)) or ((d4)<= i <=(d4-20))):
			if (ww!='80d'):
				ww='80dl';
				#print(ww)
				c = cv2.rectangle(c,(center[0]-(d2-80),center[1]-50), (center[0]+(d2-60),center[1]+50), (0,0,0), 2)
		elif (((d2-20)<= i1 <(d2-40)) or ((d4-20)<= i <=(d4-40))):			#for left
			if (ww!='60d'):
				ww='60dl'
				#print(ww)
				c = cv2.rectangle(c,(center[0]-(d2-60),center[1]-50), (center[0]+(d2-40),center[1]+50), (0,0,0), 2)
		elif (((d2-40)<= i1 <(d2-60)) or ((d4-40)<= i <=(d4-60))):
			if (ww!='40d'):
				ww='40dl'
				#print(ww)
				c = cv2.rectangle(c,(center[0]-(d2-40),center[1]-50), (center[0]+(d2-20),center[1]+50), (0,0,0), 2)
		elif (((d2-60)<= i1 <(d2-80)) or ((d4-60)<= i <(d4-80))):
			if (ww!='20d'):
				ww='20dl'
				#print(ww)
				c = cv2.rectangle(c,(center[0]-(d2-20),center[1]-50), (center[0]+(d2),center[1]+50), (0,0,0), 2)


	elif (((d1<= i1 <(a-15))) or (d3<= i <(b-15))):	
		if (ww!='r'):
			ww='r';
			print("right")	
		if (((d1)<= i1 <(d1+20)) or ((d3)<= i <=(d3+20))):
			if (ww!='80d'):
				ww='80d';
				#print(ww)
				c = cv2.rectangle(c, (center[0]-(d1+80),center[1]-50), (center[0]+(d1+60),center[1]+50), (0,0,0), 2)
		elif (((d1+20)<= i1 <(d1+40)) or ((d3+20)<= i <=(d3+40))):			#for right
			if (ww!='60d'):
				ww='60d'
				#print(ww)
				c = cv2.rectangle(c, (center[0]-(d1+60),center[1]-50), (center[0]+(d1+40),center[1]+50), (0,0,0), 2)
		elif (((d1+40)<= i1 <(d1+60)) or ((d3+40)<= i <=(d3+60))):
			if (ww!='40d'):
				ww='40d'
				#print(ww)
				c = cv2.rectangle(c, (center[0]-(d1+40),center[1]-50), (center[0]+(d1+20),center[1]+50), (0,0,0), 2)
		elif (((d1+60)<= i1 <(d1+80)) or ((d3+60)<= i <(d3+80))):
			if (ww!='20d'):
				ww='20d'
				#print(ww)
				c = cv2.rectangle(c, (center[0]-(d1+20),center[1]-50), (center[0]+d1,center[1]+50), (0,0,0), 2)

	'''if(ww=='f'):
		c = cv2.rectangle(c, (center[0]-50,center[1]-50), (center[0]+50,center[1]+50), (0,0,0), 2)
	elif(ww=='r'):
		c = cv2.rectangle(c, (center[0],center[1]-50), (center[0]+100,center[1]+50), (0,0,0), 2)
	elif(ww=='l'):
		c = cv2.rectangle(c,(center[0]-100,center[1]-50), (center[0],center[1]+50), (0,0,0), 2)'''
		
	cv2.imshow("Image", c)
	key = cv2.waitKey(1)
	if(key==27):
		break
#font=cv2.FONT_HERSHEY_SIMPLEX
#cv2.putText(img,'text',(x1,y1),font,6)
cap.release()
cv2.destroyAllWindows()
