import cv2

img = cv2.imread("open.jpg")

img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

print(img_gray.shape)
resized = cv2.resize(img,(2000,2000))

cv2.imshow("bank",resized)

key = cv2.waitKey(0)
if key==ord("s"):
    cv2.imwrite("grayimage.png",img)
    print("image saved")

cv2.destroyAllWindows()