import os
import cv2
import sys
import numpy as np
import math
import serial
import time

ser = serial.Serial(port = "/dev/ttyUSB0", baudrate = 9600) #シリアル通信ポート指定
capture = cv2.VideoCapture(0) #OpenCVでコンピュータカメラによる画像読み取り開始
backSub = cv2.createBackgroundSubtractorKNN() #KNNバックグラウンド処理器の初期化
cv2.namedWindow("Capture")
res = 0
while True:
    ret, frame = capture.read()
    cv2.rectangle(frame, (460, 300), (660, 0), (0, 0, 0), 2) #手が入る領域の指定
    frame = cv2.putText(frame, 'Put hand here', (390, 325), cv2.FONT_HERSHEY_SIMPLEX, fontScale= 1, color = (0, 0, 0), thickness = 2)
    frame = cv2.putText(frame, 'And press ESC', (390, 350), cv2.FONT_HERSHEY_SIMPLEX, fontScale= 1, color = (0, 0, 0), thickness = 2)
    #モーターの起動状態の表示
    if res == 0:
        frame = cv2.putText(frame, 'Status : OFF', (390, 380), cv2.FONT_HERSHEY_SIMPLEX, fontScale= 1, color = (0, 0, 0), thickness = 2) 
    if res == 1 or res == 2:
        frame = cv2.putText(frame, 'Status: ON', (390, 380), cv2.FONT_HERSHEY_SIMPLEX, fontScale= 1, color = (0, 0, 0), thickness = 2)
    #読み取り画像の表示
    cv2.imshow("Capture", frame)
    im = frame[0:200, 400:960] #手だけが入る領域以外の切り取り
    im_mask = backSub.apply(im) #バックグラウンド処理
    c = cv2.waitKey(2)
    if c == 27: #ESCキーが押されたら
        cv2.imwrite('up1.png', im_mask) #マスクが付いている写真の保存
        cv2.imwrite('up2.png', im)
        src = cv2.imread('up1.png') #バックグラウンド処理済写真の読み込み
        dst = cv2.Canny(src, 50, 200, None, 3) #Cannyエッジ処理
        cdstP = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR) #イメージの二値化
        linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10) #Hough Linesの計算
        
        #Hough Linesの描画
        if linesP is not None:
            for i in range(0, len(linesP)):
                l = linesP[i][0]
                cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
        
        #Hough Linesの傾きの平均値計算
        m = 0
        if linesP is not None:
            for i in range(0, len(linesP)):
                l = linesP[i][0]
                r = (l[3]-l[1])/(l[2]-l[0])
                m = m + abs(math.floor(r))
        res = math.floor(abs(m/len(linesP)))

        print(res)
        cv2.imwrite('final.png', cdstP)

        #シリアル通信のための値の決定
        if res>5:
            res = 2
        elif res>1:
            res = 1
        else:
            res = 0

        print(res)
        #速度モードに対応する値の送信
        if res == 2:
            ser.write(b'2')
        elif res == 1:
            ser.write(b'1')
        else:
            ser.write(b'0')
        time.sleep(1)
        res = res