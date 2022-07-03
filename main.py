import cv2
#import tracker

#Obeject Detection From Stable Camera
cap = cv2.VideoCapture("2022-05-09-140553.webm")

width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Substract moving objects on camera
object_detector = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()

    #Object Detetection
    mask = object_detector.apply(frame)

    #retirando as sombras
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        #desenhando o retângulo de detecção
        area = cv2.contourArea(cnt)
        if area > 100:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
    
    cv2.imshow("Fly Detection", frame)
    #cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()