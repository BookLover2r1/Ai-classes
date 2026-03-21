import cv2
face_cascade = cv2.CascadeClassifier("haarcascade.xml")
cap = cv2.VideoCapture(0)

print(cap.read())
while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor = 2,minNeighbors = 2, minSize = (30,30))
    print(faces)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y),(x+w, y+h),(255,0,0),2)
        
    cv2.imshow("capture", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cap.destroyAllWindows()

