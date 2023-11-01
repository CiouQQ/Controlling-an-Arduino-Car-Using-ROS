#! /usr/bin/env python3
import rospy
import numpy as np
import cv2
from std_msgs.msg import String
if __name__ == '__main__':
    rospy.init_node('talker',anonymous=True)
    pub0 = rospy.Publisher('stop', String, queue_size=10)
    pub1 = rospy.Publisher('slow', String, queue_size=10)
    pub2 = rospy.Publisher('normal', String, queue_size=10)
    pub3 = rospy.Publisher('fast', String, queue_size=10)
    pubR = rospy.Publisher('right', String, queue_size=10)
    pubL = rospy.Publisher('left', String, queue_size=10)
    rate = rospy.Rate(1000)
    

    frameWidth = 640
    frameHeight = 480
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('01.avi', fourcc, 10.0, (640, 480))
    deadZone=130
    global imgContour
    global hello
    hello = "1"
    i = 0

    def getContours(img,imgContour):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        message = "0"
        
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            areaMin = 300
            if area > areaMin:
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x , y , w, h = cv2.boundingRect(approx)

                cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)#綠色方形
                cv2.putText(imgContour, "Wid: " + str(w)+ "Hei: " +str(h), (20, frameHeight -100), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 255, 0), 2) #打印長跟寬

                w_distance = "{:.2f}".format(577 * 5.2 / w)
                l_distance = "{:.2f}".format(577 * 5.2 / h)
                text = "wDistance: {} cm, lDistance: {} cm".format(w_distance, l_distance)
                cv2.putText(imgContour, text, ( 20,frameHeight-50 ), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)#印出距離
                # message = f'wdistance = {w_distance} ldistance= {l_distance}  '
                if 577 * 5.2 / h > 60 or 577 * 5.2 / w >60:
                    message = "3"
                elif 577 * 5.2 / h > 13 or 577 * 5.2 / w >13:
                    message = "2"
                elif 577 * 5.2 / h > 5 or 577 * 5.2 / w >5:
                    message = "1"
                


                cx = int(x + (w / 2))#中心點X
                cy = int(y + (h / 2))#中心點y
                cv2.putText(imgContour, " " + str(int(cx))+ " "+str(int(cy)), (x - 20, y- 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                        (0, 255, 0), 2) #印出中心點
                #塗滿紅色&位置標示
                if (cx <int(frameWidth/2)-deadZone):
                    cv2.putText(imgContour, " GO LEFT " , (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                    message = "L"
                elif (cx > int(frameWidth / 2) + deadZone):
                    cv2.putText(imgContour, " GO RIGHT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255), 3)
                    message = "R"
                cv2.line(imgContour, (int(frameWidth/2),int(frameHeight/2)), (cx,cy),
                        (0, 0, 255), 3)#畫連接線
                
        return message

    def display(img): #畫九宮格的線
        cv2.line(img,(int(frameWidth/2)-deadZone,0),(int(frameWidth/2)-deadZone,frameHeight),(255,255,0),3)
        cv2.line(img,(int(frameWidth/2)+deadZone,0),(int(frameWidth/2)+deadZone,frameHeight),(255,255,0),3)

        cv2.circle(img,(int(frameWidth/2),int(frameHeight/2)),5,(0,0,255),5)

    while not rospy.is_shutdown():
        i = i+1
        _, img = cap.read()
        imgContour = img.copy()
        imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        


        h_min = 19
        h_max = 35
        s_min = 107
        s_max = 255
        v_min = 89
        v_max = 255
        

        lower = np.array([h_min,s_min,v_min])
        upper = np.array([h_max,s_max,v_max])
        mask = cv2.inRange(imgHsv,lower,upper)
        result = cv2.bitwise_and(img,img, mask = mask)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        imgBlur = cv2.GaussianBlur(result, (7, 7), 1)
        imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
        threshold1 = 166
        threshold2 = 171
        imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
        kernel = np.ones((5, 5))
        imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
        hello = getContours(imgDil, imgContour)#判斷
        display(imgContour)#畫九宮格的線

        out.write(imgContour)
        cv2.imshow('Horizontal Stacking', imgContour)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            i = i+1
        rate.sleep()
        if i >1:
            i = 0
            if(hello == "R"):
                pubR.publish(hello)
                rospy.loginfo(hello)
            elif(hello == "L"):
                pubL.publish(hello)
                rospy.loginfo(hello)
            elif(hello == "3"):
                pub3.publish(hello)
                rospy.loginfo(hello)
            elif(hello == "2"):
                pub2.publish(hello)
                rospy.loginfo(hello)
            elif(hello == "1"):
                pub1.publish(hello)
                rospy.loginfo(hello)
            else:
                pub0.publish(hello)
                rospy.loginfo(hello)
                
        
    cap.release()
    out.release()
    cv2.destroyAllWindows()

