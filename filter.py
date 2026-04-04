import cv2
import numpy as np

def a_f(image, f_type):
    img = image.copy()
    if f_type == 'red_tint':
        img[:,:,1] = img[:,:,0] = 0
    elif f_type == 'green_tint':
        img[:,:,0] = img[:,:,2] = 0
    elif f_type == 'blue_tint':
        img[:,:,1] = img[:,:,2] = 0
    elif f_type == 'sobel':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize = 3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize = 3)
        sob = cv2.bitwise_or(sx.astype('uint8'),sy.astype('uint8'))
        img = cv2.cvtColor(sob, cv2.COLOR_GRAY2BGR)
    elif f_type == 'canny':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        can = cv2.Canny(gray, 100, 200)
        img = cv2.cvtColor(can, cv2.COLOR_GRAY2BGR)
    elif f_type == 'cartoon':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(image, 9 , 300, 300)
        img = cv2.bitwise_and(color, color, mask = edges)
    return img

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Your camera aint opening")
        return
    f_type = 'original'
    print("Keys: r=Red g = Green b = Blue s = Sobel c = Canny t = Cartoon q = Quit")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No frames recieved")
            break
        out = a_f(frame, f_type)
        cv2.imshow("Filter", out)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            f_type = "red_tint" 
        elif key == ord('g'):
            f_type = "green_tint"   
        elif key == ord('b'):
            f_type = "blue_tint"  
        elif key == ord('s'):
            f_type = "sobel"   
        elif key == ord('c'):
            f_type = "canny"       
        elif key == ord('t'):
            f_type = "cartoon"
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()                                