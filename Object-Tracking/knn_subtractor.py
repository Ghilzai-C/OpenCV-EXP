import cv2 
# this code uses background subtraction using KNN method with shadow detect true 
bg_subtractor = cv2.createBackgroundSubtractorKNN(detectShadows= True)
erode_kernel = cv2. getStructuringElement(cv2.MORPH_ELLIPSE, (7, 3))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(17, 11))
# i am using realsense camera so will need to use 1 if you are using normal rgb camera then put 0
cap = cv2.VideoCapture(1)
# test the camera work properly if not then exit the code 
for i in range (10):
    success, frame = cap.read()
if not success:
    exit(1)

success, frame = cap.read()
while success:
    fg_mask = bg_subtractor.apply(frame)
    _, thresh = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)
    cv2.erode(thresh, erode_kernel, thresh, iterations = 2)
    cv2.dilate(thresh, dilate_kernel, thresh, iterations = 2)

    contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 
                                         cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) > 1000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h),(0, 255, 255), 3 )


    cv2.imshow('fg_mask', fg_mask)
    cv2.imshow('thresh', thresh)
    cv2.imshow('detection', frame)

    k = cv2.waitKey(30)
    if k ==27:
        break
    success, frame = cap.read()
    