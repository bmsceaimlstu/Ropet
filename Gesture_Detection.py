#import serial
import time
import cv2
import os
import HandTrackingModule as hm
import numpy as np
import math

#Setting up webcam
wCam, hCam = 1280, 480

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)

#Initialisation
pTime = 0

detector = hm.handDetector(detectionCon=0.75)

Speed="WAITING"
Speed_Text="Z"
Speed_Text_prev="X"
Scheck=0

totalFingers_prev=-1
check=0
tipIds = [4, 8, 12, 16, 20]


if __name__=='main_':
    #ser =serial.Serial('COM15',9600,timeout=5)
    #ser.flush()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        
        if len(lmList) != 0:
            fingers = []

            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            totalFingers = fingers.count(1)

            if fingers==[1,1,0,0,0]:

                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                length = math.hypot(x2 - x1, y2 - y1)
                
                if length>180:
                    Speed="HIGH"
                    Speed_Text="H"
                if length>95 and length<180:
                    Speed="MEDIUM"
                    Speed_Text="M"
                if length<95:
                    Speed="LOW"
                    Speed_Text="L"
            if totalFingers == 0:
                Disp_text="STOPPING"
            if totalFingers == 1:
                Disp_text="MOVING BACK"
            if totalFingers == 2:
                Disp_text="MOVING FORWARD"
            if totalFingers == 3:
                if fingers==[1,1,0,0,1]:
                    totalFingers = 6
                    Disp_text = "GRASS TRIMMER ON"
                else:
                    Disp_text="TURNING RIGHT"
            if totalFingers == 4:
                if fingers==[1,1,1,0,1]:
                    totalFingers = 7
                    Disp_text = "GRASS TRIMMER OFF"
                else:
                    Disp_text="TURNING LEFT"
            if totalFingers == 5:
                Disp_text="SPINNING 360"
            if totalFingers!=2:
                Speed="WAITING"


            # On-screen printing 
            cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,10, (0, 0, 0), 25)
            cv2.putText(img, "Speed = "+str(Speed), (100, 70), cv2.FONT_HERSHEY_PLAIN,3, (0, 255, 0), 5)
            cv2.putText(img, "Fingers = "+str(totalFingers), (100, 120), cv2.FONT_HERSHEY_PLAIN,3, (0, 0, 255), 5)
            cv2.putText(img, "Action = "+str(Disp_text), (100, 170), cv2.FONT_HERSHEY_PLAIN,3, (0, 0, 255), 5)

            # Add delay library 
            if totalFingers_prev != totalFingers:
                check=check+1
                
                print(totalFingers)
                if check>3:
                    #ser.write(str(totalFingers).encode('utf-8'))
                    print("Sent the Number :",str(totalFingers))
                    totalFingers_prev = totalFingers
                    time.sleep(0.5)
                    check=0

            if Speed_Text_prev != Speed_Text:
                Scheck=Scheck+1
                #time.sleep(0.25)
                print(Speed_Text)
                if Scheck>3:
                    #ser.write(str(Speed_Text).encode('utf-8'))
                    print("Sent the Number :",str(Speed_Text))
                    Speed_Text_prev = Speed_Text
    
                    #time.sleep(0.5)
                    Scheck=0

        #Calculating, printing frames per second           
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime


        cv2.putText(img, f'FPS: {int(fps)}', (900, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 3)
                    

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        


    cv2.destroyAllWindows()
    cap.release()
    #push check 123
    