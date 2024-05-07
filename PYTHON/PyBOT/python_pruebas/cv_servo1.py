import RPi.GPIO as GPIO
from time import sleep
import numpy as np
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__, template_folder='template')
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)
pwm=GPIO.PWM(4, 50)

pwm.start(0)

def SetAngle(angle):
	duty = angle / 18 + 3
	pwm.ChangeDutyCycle(duty)

	
# Función para detectar un color en una región específica de la imagen
def detect_color(image, lower_bound, upper_bound, t2,side):
    p=0
    key = False 
    # Convertir la imagen al espacio de color HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Crear una máscara para el rango de colores especificado
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    # Encontrar contornos en la máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Dibujar los contornos en la imagen original
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    height1, width1, _1 = image.shape
    cont=0
    x,y=0,0

    for c in contours:
            #----AREA DE LOS CONTORNOS----
            area=cv2.contourArea(c)
            if area > 1500 and cont<=0:

                #----Deteccion del centro----
                m=cv2.moments(c)
                if (m["m00"]==0): m['m00']=1
                x=int(m['m10']/m['m00'])
                y=int(m['m01']/m['m00'])

                cont+=1
              
                if side == 'right':
                    p=abs(x)

                elif side == 'left':
                    p=abs(x-t2)
                    

                cv2.circle(image,(x,y),3,(0, 255, 0), -1)
                suavizacion_contorno=cv2.convexHull(c)
                cv2.drawContours(image, [suavizacion_contorno], 0, (255,0,0),2)
                cv2.line(image,(x,0),(x,height1),(255,0,0),1)
                key = True

    return key,p, x, y

def generate_frames():
    
    # Access the webcam
    cap = cv2.VideoCapture(0)
    #SetAngle(90)
    pwm.start(0)
    cc=0
    middle=0
    while True:
        pwm.start(0)
        ret, frame = cap.read()
        if not ret:
            break
        else:
            # Get frame dimensions
            
            height, width, _ = frame.shape
            t2 = width // 2
            
            cv2.circle(frame,(width//2,height//2),2,(0, 255, 0), -1)
            # Define color range for detection(
            lower_bound = np.array([18, 120, 76])
            upper_bound = np.array([100, 255, 255])
           

            # Select each third and detect the corresponding color
            first_third = frame[:, :t2]
            second_third = frame[:, t2:2*t2]

            key1, p1, x_1, y_1 = detect_color(first_third, lower_bound, upper_bound, t2, 'left')
            key2, p2, x_2, y_2 = detect_color(second_third, lower_bound, upper_bound, t2, 'right')

            if key1 and key2:
                cv2.line(first_third,(x_1,height//2),(320,height//2),(255,0,0),1)
                cv2.line(second_third,(0,height//2),(x_2,height//2),(255,0,0),1)
                if p1 >= p2:
                    middle=((abs(x_1-320)+x_2)//2)+x_1
                    cv2.circle(first_third,(middle,height//2),3,(0, 255, 0), -1)
                    x11 = 90-(abs(middle-320)/t2)*90
                    # SetAngle(int(x11))
                    # print('x1 ',x11)
                else:
                    middle=((abs(x_1-320)+x_2)//2)-abs(x_1-320)
                    cv2.circle(second_third,(middle,height//2),3,(0, 255, 0), -1)
                    x22 = 90+(middle/t2)*90
                    # SetAngle(int(x22))
                    # print('x2 ',x22)
                
                cc=1

            elif key1:
                x1 = 90-(p1/t2)*90
                cv2.line(first_third,(x_1,y_1),(320,y_1),(255,0,0),1)
                # SetAngle(int(x1))
                cc=1

            elif key2:
                x2 = 90+(p2/t2)*90
                # SetAngle(int(x2))
                cv2.line(second_third,(0,y_2),(x_2,y_2),(255,0,0),1)
                cc=1

            else:
                #pwm.ChangeDutyCycle(0)
                if cc == 1:
                    # SetAngle(90)
                    sleep(0.1)
                    cc=0
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=56)