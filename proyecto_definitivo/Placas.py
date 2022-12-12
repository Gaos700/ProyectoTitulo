import cv2
import numpy as np
import pytesseract
from PIL import Image
import funciones
import re
import datetime
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

placa=[]
placas=[]
fechayhora=[]
letras= ['B','C','D','F','G','H','J','K','L','P','R','S','T','V','W','X','Y','Z'] #las PPU utilizan estas 18 letras
numeros= ['1','2','3','4','5','6','7','8','9','0']
cap = cv2.VideoCapture(0)
while True:
    ret , frame = cap.read()
    if ret == False:
        break
    al, an, c = frame.shape

    x1= int(an/5)
    x2= int(x1*4)

    y1= int(al/3)
    y2= int(y1*2)

    cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0),2)
    recorte = frame[y1:y2,x1:x2]
    gray = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(3,3))
    gauss = cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(gray,150,200)
    canny = cv2.dilate(canny,None,iterations=1)
    cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(recorte,cnts,-1,(255,0,0),2)
    for c in cnts:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        epsilon = 0.1*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)

        if len(approx)==4 and area > 1000:
            #cv2.drawContours(recorte,[c],0,(255,0,0),2)
            aspect_ratio = float(w)/h
            if aspect_ratio > 2.4:
                cv2.drawContours(recorte,[c],0,(255,0,0),2)
                placa= gray[y:y+h, x:x+w]
                text = pytesseract.image_to_string(placa, config='--psm 9')
                text=text.rstrip()
                if len(text) ==8 and funciones.verificacionLetras(text,letras)==True and funciones.verificacionNumeros(text,numeros) ==True:
                    text=funciones.removerString(text)
                    print(text)
                    if not text in placas:
                        ahora = datetime.datetime.now()
                        fechaHora = str(ahora.strftime('%d/%m/%Y %H:%M:%S'))
                        placas.append(text)
                        fechayhora.append(fechaHora)

    cv2.imshow("Vehiculos", frame)
    # leemos una tecla
    t = cv2.waitKey(1)
    if t == 27:
        break

cap.release()
print(placas)
print(fechayhora)
cv2.destroyAllWindows()
