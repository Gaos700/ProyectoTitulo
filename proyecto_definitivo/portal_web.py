from flask import Flask
from flask import render_template
from flask import Response
import cv2
import numpy as np
import pytesseract
from PIL import Image
import funciones
import re
import datetime
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

#Listas de informacion que vamos a guardar
placa=[]
placas=[]
fechas=[]
horas=[]
ubicaciones =[]
cap = cv2.VideoCapture(0)


app = Flask(__name__)
def generate():
    while True:
        horario = datetime.datetime.now()
        hour = str(horario.strftime('%H:%M:%S'))
        date = str(horario.strftime('  %d/%m/%Y'))
        ret , frame = cap.read()
        if ret == False:
            break
        al, an, c = frame.shape
        cv2.putText(frame, hour + date , (0,15),cv2.FONT_HERSHEY_PLAIN ,1,(255,255,255),1,cv2.LINE_AA)

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
                    if len(text) ==8 and funciones.verificacionLetras(text)==True and funciones.verificacionNumeros(text) ==True:
                        text=funciones.removerString(text)
                        print(text)
                        if not text in placas:
                            ahora = datetime.datetime.now()
                            fecha = str(ahora.strftime('%d/%m/%Y'))
                            hora = str(ahora.strftime('%H:%M:%S'))
                            placas.append(text)
                            fechas.append(fecha)
                            horas.append(hora)
        (flag, encodedImage) = cv2.imencode(".jpg",frame)
        if not flag:
            continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html",len=len(placas),placas = placas, fechas = fechas,horas=horas)
@app.route("/video")
def video():
    return Response(generate(),mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)
cap.release()