import cv2

class ReportPapper:
    def __init__(self):
        self.head = 'FlytType;Amount\n'
        self.amount = 0
        self.line = f'Tephritidae;{0}'
    

    def Registrer(self):
        try:
            with open('results.csv', 'r') as results:
                pass  
        except FileNotFoundError:
            with open('results.csv', 'w') as results:
                results.write(self.head)
                results.write(self.line)

    def Update(self):
        with open('results.csv', 'w') as results:
            self.line = f'Tephritidae;{self.amount}'
            results.write(self.head)
            results.write(self.line)


def selectROIfromFrame(frame):
    box = cv2.selectROI('Select ROI', frame, fromCenter=False, showCrosshair=False)
    return box

#Obeject Detection From Stable Camera
cap = cv2.VideoCapture("video1.webm")
if cap.isOpened():
    width, heigth = cap.get(3), cap.get(4)

#Substract moving objects on camera
object_detector = cv2.createBackgroundSubtractorMOG2()

select_frame = cv2.imread('mask_modelo.png')

box = selectROIfromFrame(select_frame)
#box -- x, y, w, h
tracker = cv2.TrackerCSRT_create()
modelo = tracker.init(select_frame, box)

flys = []
Report = ReportPapper()
Report.Registrer()

count_fly = 0

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    #Object Detetection
    mask = object_detector.apply(frame)


    #retirando as sombras
    _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    ok, box = tracker.update(mask)

    if 0 < box[1] <= box[3]:
        if len(flys) == 0:
            flys.append([1, box[3], True, False])
        else:
            for fly in flys:
                if fly[1] - box[3] <= 3:
                    continue
                else:
                    aux = flys[-1][0] + 1
                    flys.append([aux, box[3], True, False])
    if box[1] >= heigth - box[3]:
        for fly in flys:
            if fly[1] - box[3] <= 3:
                fly[3] = True
    
    """for cnt in contours:
        #desenhando o retângulo de detecção
        area = cv2.contourArea(cnt)
        if area > 100:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)"""

    if ok:
        p1 = (box[0], box[1])
        p2 = (box[0] + box[2], box[1] + box[3])
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    

    #Report Update
    for fly in flys:
        if fly[2] and fly[3]:
            Report.amount += 1
            fly[2], fly[3] = False, False

    Report.Update()
    

    cv2.imshow("Fly Detection", frame)

    key = cv2.waitKey(60)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()