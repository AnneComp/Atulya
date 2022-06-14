import cv2
import math
from cv2 import waitKey
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
    final_copy=img.copy()
    Result=cv2.imwrite('Python/Output.jpg',final_copy)
    cv2.imshow("Output",Result)
    cv2.waitKey(0)
#######################
def find_aruco_prop(the_img):
    gray_img=cv2.cvtColor(the_img,cv2.COLOR_BGR2GRAY)
    key=getattr(aruco,f'DICT_5X5_250')
    arucoDict=aruco.Dictionary_get(key)
    arucoParam=aruco.DetectorParameters_create()
    (corners,id_s,rejected)=cv2.aruco.detectMarkers(gray_img,arucoDict,parameters=arucoParam)
    return corners,id_s,rejected
#######################
def co_ord_aruco(an_aruco):
    corners,ids,r=find_aruco_prop(an_aruco)
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
    l1=[topLeft,topRight,bottomLeft,bottomRight]
    xmin,ymin,xmax,ymax=ord_of_co_ord(l1)
    crp_img=ar_img[ymin:ymax,xmin:xmax]
    crp_cor=np.array([[0,0],[crp_img.shape[1],0],[crp_img.shape[1],crp_img.shape[0]],[0,crp_img.shape[0]]])
    return crp_img,crp_cor
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
def rotate(thetha,aruco_centre,aruco_image):
    M=cv2.getRotationMatrix2D(aruco_centre,thetha,1.0)
    ar_img=cv2.warpAffine(aruco_image,M,aruco_image.shape[1::-1])
    return ar_img
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
def get_squares(imgex):
    global color_val,color_id
    global aruco_id_dict
    contours,heirarchy=cv2.findContours(imgex,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        cv2.drawContours(img_copy,cnt,-1,(0,255,0),2)
        perimeter=cv2.arcLength(cnt,True)
        approxx=cv2.approxPolyDP(cnt,0.02*perimeter,True)
        x,y,w,h=cv2.boundingRect(approxx)
        if len(approxx)==4:
            find_square=w/float(h)
            if find_square>0.95 and find_square<1.05:
                co_ord=[all_co[0].tolist() for all_co in approxx]
                centre=(int((co_ord[0][0]+co_ord[2][0])/2),int((co_ord[0][1]+co_ord[2][1])/2))
                for i in color_val.keys():
                    vals=np.array(color_val[i])
                    vals.reshape((3,))
                    if (vals==img_copy[centre[1],centre[0],:]).any():
                        abc=np.array(color_id[i])
                        abc.reshape((1,1))
                        for j in aruco_id_dict.keys():
                            if (abc==aruco_id_dict[j]).any():
                                pt1=approxx
                                xx=j
                                mm=cv2.imread(xx)
                                cen,lm,ar_an=aruco_angle(mm)    
                                rot=rotate(ar_an,cen,mm)                            
                                updated_aruco,pt2=crop_aruco(rot)                           
                                M,_=cv2.findHomography(pt2,pt1)
                                global img
                                warp_img=cv2.warpPerspective(updated_aruco,M,(img.shape[1],img.shape[0]))
                                cv2.fillConvexPoly(img,pt1,(0,0,0))
                                img=img+warp_img                                
                                waitKey(0)
#######################
main()
