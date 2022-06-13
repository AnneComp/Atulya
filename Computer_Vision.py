import cv2
import math
import cv2.aruco as aruco
import numpy as np
import os
from pytest import approx
#######################
img= cv2.imread("Python/CVtask.jpg")
img_copy=img.copy()
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_edges=cv2.Canny(img_gray,70,70)
_,thresh=cv2.threshold(img_gray,200,255,cv2.THRESH_BINARY)

aruco_list=['Python/Ha.jpg','Python/LMAO.jpg','Python/XD.jpg','Python/HaHa.jpg']
aruco_id_dict={}

color_val={'green':[79,209,146],'orange':[9,127,240],'black':[0,0,0],'pink/peach':[210,22,228]}
color_id={'green':1,'orange':2,'black':3,'pink/peach':4}
#######################
def main():
    global aruco_id_dict
    for i in aruco_list:
        x=cv2.imread(i)
        (a,b,c)=find_aruco_prop(x)
        aruco_id_dict[i]=b
    get_squares(img_edges)
    abc=get_colors(img_copy)
    print(abc)
    #get_coordinates(img_gray)
    img_copy_1=img_copy[600:1600,600:1600]
    cv2.imshow("Contour",img_copy)
    cv2.imshow("Contour1",img_copy_1)
    #cv2.imshow("Canny",img_edges)
    cv2.waitKey(0)
#######################
def find_aruco_prop(the_img):
    gray_img=cv2.cvtColor(the_img,cv2.COLOR_BGR2GRAY)
    key=getattr(aruco,f'DICT_5X5_250')
    arucoDict=aruco.Dictionary_get(key)
    arucoParam=aruco.DetectorParameters_create()
    (corners,id_s,rejected)=cv2.aruco.detectMarkers(gray_img,arucoDict,parameters=arucoParam)
    return (corners,id_s,rejected)
#######################
def co_ord_aruco(an_aruco):
    (corners,ids,r)=find_aruco_prop
    if len(corners)>0:
        ids=ids.flatten()
        for (markerCorner,markerIds) in zip(corners,ids):
            corners=markerCorner.reshape((4,2))
            (topLeft,topRight,bottomRight,bottomLeft)=corners
            topLeft=(int(topLeft[0]),int(topLeft[1]))
            topRight=(int(topRight[0]),int(topRight[1]))
            bottomRight=(int(bottomRight[0]),int(bottomRight[1]))
            bottomLeft=(int(bottomLeft[0]),int(bottomLeft[1]))
        return topLeft,topRight,bottomLeft,bottomRight
#######################
def crop_aruco(ar_img):
    topLeft,topRight,bottomLeft,bottomRight=co_ord_aruco(ar_img)
    q=[topLeft,topRight,bottomLeft,bottomRight]
    x_min,y_min,x_max,y_max=ord_of_co_ord(q)
    crp_img=ar_img[y_min:y_max,x_min:x_max]
    return crp_img
#######################
def aruco_angle(aruco_img):
    topLeft,topRight,bottomLeft,bottomRight=co_ord_aruco(aruco_img)
    centre_x=int((topLeft[0]+bottomRight[0])/2.0)
    centre_y=int((topLeft[1]+bottomRight[1])/2.0)
    centre=(centre_x,centre_y)
    line_x=int((topLeft[0]+topRight[0])/2.0)
    line_y=int((topLeft[1]+topRight[1])/2.0)
    line_mid=(line_x,line_y)
    if line_x!=centre_x:
        ar_angle=(math.atan((centre_y-line_y)/(centre_x-line_x)))*180/math.pi
    else:
        ar_angle=90
    return centre,line_mid,ar_angle
#######################
def rotate(sq_size,thetha,aruco_centre,aruco_image):
    M=cv2.getRotationMatrix2D(aruco_centre,thetha,1.0)
    marker=cv2.imread(aruco_image)
    rotated_marker=cv2.warpAffine(marker,M,(sq_size[0],sq_size[1]))
    return rotated_marker
#######################
def ord_of_co_ord(sm_list):
    x_min=sm_list[0][0]
    x_max=sm_list[0][0]
    y_min=sm_list[0][1]
    y_max=sm_list[0][1]
    for i in sm_list:
        if i[0]>x_max:
            x_max=i[0]
        if i[1]>y_max:
            y_max=i[1]
        if i[0]<x_min:
            x_min=i[0]
        if i[1]<y_min:
            y_min=i[1]
    return x_min,y_min,x_max,y_max
#######################
def get_color(cent):
    for i in color_val.keys():
        n=np.array(color_val[i])
        n.reshape(3,)
        #print('Cent: ',cent[1],cent[0])
        #print(img[cent[1],cent[0],:])
        if (n==img[cent[1],cent[0],:]).any():
            m=np.array(color_id[i])
            m.reshape(1,1)
#######################
def overlay_aruco(or_img,pix_val,sq_size,rot_aruco):
    upd_img=cv2.imread(or_img)
    marker=cv2.imread(rot_aruco,cv2.IMREAD_UNCHANGED)
    #resized_aruco=cv2.resize(rot_aruco,dsize=(sq_size,sq_size))
    upd_img[pix_val[0]:pix_val[1],pix_val[2]:pix_val[3]]=rot_aruco
#######################
colors=['']
#######################
''''list=[1,2,3,4]
def get_colors(image):
    imgcolor=image.copy()
    imghsv=cv2.cvtColor(imgcolor,cv2.COLOR_BGR2HSV)
    xx='None'
    green_lower = np.array([25, 144, 72], np.uint8)
    green_upper = np.array([102, 255, 255], np.uint8)
    green_mask = cv2.inRange(imghsv, green_lower, green_upper)
    orange_lower = np.array([5, 240, 220],np.uint8)
    orange_upper= np.array([255, 250, 255],np.uint8)
    orange_mask=cv2.inRange(imghsv,orange_lower,orange_upper)
    black_lower=np.array([0,0,0],np.uint8)
    black_upper=np.array([0,5,5],np.uint8)
    black_mask=cv2.inRange(imghsv,black_lower,black_upper)
    pink_lower = np.array([4, 0, 225]) 
    pink_upper = np.array([90,28,240])
    pink_mask=cv2.inRange(imghsv,pink_lower,pink_upper)
    masks=[green_mask,orange_mask,black_mask,pink_mask]
    global list
    for i in list:
        if i==1:
            get_square()

    if len(get_squares(green_mask))>0:
        #cv2.imshow('ggg',green_mask)
        print('green')
    if len(get_squares(orange_mask))>0:
        #cv2.imshow('ooo',orange_mask)
        print('orange')
    if len(get_squares(black_mask))>0:
        cv2.imshow('bbbb',black_mask)
        print('black')
    else:
        cv2.imshow('bbbb',black_mask)
    if len(get_squares(pink_mask))>0:
        #cv2.imshow('pppp',pink_mask)
        print('pink')
    else:
        print('Error')
'''

#######################
def get_squares(imgex):
    contours,heirarchy=cv2.findContours(imgex,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        cv2.drawContours(img_copy,cnt,-1,(0,255,0),2)
        list_for_sq=[]
        perimeter=cv2.arcLength(cnt,True)
        approxx=cv2.approxPolyDP(cnt,0.02*perimeter,True)
        x,y,w,h=cv2.boundingRect(approxx)
        #print('APPROXX: ',approxx)
        if len(approxx)==4:
            find_square=w/float(h)
            if find_square>0.95 and find_square<1.05:
                objectType='Square'
                co_ord=[all_co[0].tolist() for all_co in approxx]
                xmin,ymin,xmax,ymax=ord_of_co_ord(co_ord)
                #print(xmin,xmax,ymin,ymax)
                sq_img=imgex[ymin:ymax,xmin:xmax]
                sq_shape=sq_img.shape
                sq_x=sq_shape[0]
                sq_y=sq_shape[1]
                mid=(int((co_ord[0][0]+co_ord[1][0])/2),int((co_ord[0][1]+co_ord[1][1])/2))
                centre=(int((co_ord[0][0]+co_ord[2][0])/2),int((co_ord[0][1]+co_ord[2][1])/2))
                if centre[0]!=mid[0]:
                    theta=(math.atan((centre[1]-mid[1])/(centre[0]-mid[0])))*180/math.pi
                else:
                    theta=90     
                    global color_val,color_id
                    global aruco_id_dict               
                for i in color_val.keys():
                    vals=np.array(color_val[i])
                    vals.reshape((3,))
                    if (vals==img_copy[centre[1],centre[0],:]).any():
                        abc=np.array(color_id[i])
                        abc.reshape((1,1))
                        for j in aruco_id_dict.keys():
                            if (vals==aruco_id_dict[j]).any():
                                xx=j

                        mm=cv2.imread(xx)
                        cen,ar_an=aruco_angle(mm)
                        rot=rotate(sq_shape,ar_an-theta,cen,mm)
                list_for_sq.append(approxx)
            else: objectType='Rect'
        else: objectType='None'
        
        cv2.putText(img_copy,objectType,[x+(w//2)-5,y+(h//2)],cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),2)
    return list_for_sq

#######################
main()