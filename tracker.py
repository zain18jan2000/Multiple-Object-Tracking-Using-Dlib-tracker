import cv2
import dlib

cap = cv2.VideoCapture('video.mp4')

trackers = []

while True:
    success,frame = cap.read()

    if frame is None:
        break

    frame = cv2.resize(frame,(900,580))
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    for tracker in trackers:
        tracker.update(rgb_frame)
        position = tracker.get_position()
        x1 = int(position.left())
        y1 = int(position.top())
        x2 = int(position.right())
        y2 = int(position.bottom())

        cv2.rectangle(frame,(x1,y1),(x2,y2),(255,255,255),2)

    cv2.imshow('video',frame)
    k = cv2.waitKey(30)

    if k == ord('s'):
        rois = cv2.selectROIs('video',frame)

        for roi in rois:
            x1,y1,w,h = roi
            x2,y2 = x1+w, y1+h

            tkr = dlib.correlation_tracker()
            rect = dlib.rectangle(x1,y1,x2,y2)
            tkr.start_track(rgb_frame,rect)
            trackers.append(tkr)


cap.release()
cv2.destroyAllWindows()