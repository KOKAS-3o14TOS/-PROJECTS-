from flask import Flask, Response, render_template, request
from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
from time import sleep
import cv2
import numpy as np
import picar
import os

# Initialize default HSV values
H, S, V = 0, 21, 229
H2, S2, V2 = 255, 255, 255


SERVO = 0


picar.setup()

MIDDLE_TOLERANT = 5
PAN_ANGLE_MAX   = 180
PAN_ANGLE_MIN   = 0
TILT_ANGLE_MAX  = 180
TILT_ANGLE_MIN  = 0
FW_ANGLE_MAX    = 90+30
FW_ANGLE_MIN    = 90-30

SCAN_POS = [[20, TILT_ANGLE_MIN], [50, TILT_ANGLE_MIN], [90, TILT_ANGLE_MIN], [130, TILT_ANGLE_MIN], [160, TILT_ANGLE_MIN], 
            [160, 80], [130, 80], [90, 80], [50, 80], [20, 80]]

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(3)
picar.setup()

fw.offset = 10
pan_servo.offset = 0
tilt_servo.offset = 0
bw.speed = 20
pan_servo.write(90)
tilt_servo.write(22.5)
bw.stop()


app = Flask(__name__, template_folder='template')



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

    cc=0
    middle=0
    while True:
        ret, frame = cap.read()

        if not ret:
            break
        else:
            # Get frame dimensions
            
            height, width, _ = frame.shape
            t2 = width // 2
            h3 = height//2
            cv2.circle(frame,(width//2,height//2),2,(0, 255, 0), -1)
            # Define color range for detection(
            #Green
            '''
            lower_bound = np.array([18, 120, 76])
            upper_bound = np.array([100, 255, 255])
            '''
            # white
            '''
            lower_bound = np.array([82, 6, 108])
            upper_bound = np.array([128, 255, 255])
            '''
            # PINK
            '''
            lower_bound = np.array([0, 20, 255])
            upper_bound = np.array([227, 255, 255])
            '''
            lower_bound = np.array([H, S, V], np.uint8)
            upper_bound = np.array([H2,S2,V2], np.uint8)
            # Select each third and detect the corresponding color
            first_third = frame[h3:, :t2]
            second_third = frame[h3:, t2:2*t2]

            key1, p1, x_1, y_1 = detect_color(first_third, lower_bound, upper_bound, t2, 'left')
            key2, p2, x_2, y_2 = detect_color(second_third, lower_bound, upper_bound, t2, 'right')

            if key1 and key2:
                cv2.line(first_third,(x_1,h3//2),(320,h3//2),(255,0,0),1)
                cv2.line(second_third,(0,h3//2),(x_2,h3//2),(255,0,0),1)
                if p1 >= p2:
                    middle=((abs(x_1-320)+x_2)//2)+x_1
                    cv2.circle(first_third,(middle,h3//2),3,(0, 255, 0), -1)
                    x11 = 90-(abs(middle-320)/t2)*90
                    fw.turn(x11)
                    bw.speed = 45
                    bw.forward()
                else:
                    middle=((abs(x_1-320)+x_2)//2)-abs(x_1-320)
                    cv2.circle(second_third,(middle,h3//2),3,(0, 255, 0), -1)
                    x22 = 50+(middle/t2)*90
                    fw.turn(x22)
                    bw.speed = 45
                    bw.forward()
                cc=1

            elif key1:
                x1 = 50+(p1/t2)*90
                cv2.line(first_third,(x_1,y_1),(320,y_1),(255,0,0),1)
                fw.turn(x1)
                bw.speed = 50
                bw.forward()
                cc=1

            elif key2:
                x2 = 45-(p2/t2)*90
                # SetAngle(int(x2))
                cv2.line(second_third,(0,y_2),(x_2,y_2),(255,0,0),1)
                fw.turn(x2)
                bw.speed = 50
                bw.forward()
                cc=1

            else:
                #pwm.ChangeDutyCycle(0)
                if cc == 1:
                    fw.turn(90)
                    bw.stop()
                    cc=0
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():

    return render_template('index.html', H=H, S=S, V=V, H2=H2, S2=S2, V2=V2,SERVO=SERVO)
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/update_hsv', methods=['POST'])
def update_hsv():
    global H, S, V, H2, S2, V2, servo
    data = request.get_json()
    H = data['H']
    S = data['S']
    V = data['V']
    H2 = data['H2']
    S2 = data['S2']
    V2 = data['V2']
    SERVO = data['SERVO']
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=56,debug=True)