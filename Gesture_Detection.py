import serial
import time
import cv2
import os
import HandTrackingModule as hm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)

detector = hm.handDetector(detectionCon=0.75)

totalFingers_prev=-1
check=0
tipIds = [4, 8, 12, 16, 20]

if __name__=='main_':
    ser =serial.Serial('COM15',9600,timeout=5)
    ser.flush()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        # print(lmList)

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

            # print(fingers)
            totalFingers = fingers.count(1)
    


        #add delay library 
            cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,10, (0, 0, 0), 25)
            if totalFingers_prev != totalFingers:
                check=check+1
                #time.sleep(0.25)
                print(totalFingers)
                if check>3:
                    ser.write(str(totalFingers).encode('utf-8'))
                    print("Sent the Number :",str(totalFingers))
                    totalFingers_prev = totalFingers
                    time.sleep(0.5)
                    check=0
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime


        cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 3)
                    

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        


    cv2.destroyAllWindows()
    cap.release()