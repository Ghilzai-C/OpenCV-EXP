import cv2 
# this code uses the simple base background difference method for tracking object 
blur_radius = 21 
erode_kernel = cv2. getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9, 9))

cap = cv2.VideoCapture(1)
for i in range (10):
    success, frame = cap.read()
if not success:
    exit(1)
gray_background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray_background = cv2.GaussianBlur( gray_background, 
                                   (blur_radius, blur_radius ), 0)
success, frame = cap.read()
while success:
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (blur_radius, blur_radius), 0)
    
    diff = cv2.absdiff(gray_background, gray_frame)
    _, thresh = cv2.threshold(diff, 40, 255, cv2.THRESH_BINARY)
    cv2.erode(thresh, erode_kernel, thresh, iterations = 2)
    cv2.dilate(thresh, dilate_kernel, thresh, iterations = 2)

    contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 
                                         cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) > 4000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h),(0, 255, 255), 3 )


    cv2.imshow('diff', diff)
    cv2.imshow('thresh', thresh)
    cv2.imshow('detection', frame)

    k = cv2.waitKey(1)
    if k ==27:
        break
    success, frame = cap.read()
    