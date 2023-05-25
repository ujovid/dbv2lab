import time
import cv2

cap = cv2.VideoCapture('sample.mp4')
counter_left = 0
counter_right = 0

flag = None

x_tmp = 0
y_tmp = 0
counter = 0
while True:
    ret, img = cap.read()
    if not ret:
        break

    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grey = cv2.GaussianBlur(grey, (21, 21), 0)
    ret, thresh = cv2.threshold(grey, 100, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        X, Y, W, H = cv2.boundingRect(c)
        counter += 1
        x_tmp += X
        y_tmp += Y
        if X + W // 2 > 320:

            counter_right += bool(not flag)
            color = (255, 0, 0)
            flag = True
        else:
            counter_left += 1 if flag else 0
            color = (0, 0, 255)
            flag = False

        cv2.circle(img, (X + W // 2, Y + H // 2), W // 2, color, 2)
        cv2.line(img, (0, Y + H // 2), (640, Y + H // 2), color, 1)
        cv2.line(img, (X + W // 2, 0), (X + W // 2, 480), color, 1)
        cv2.putText(img, "x: " + str(X) + " y: " + str(Y) + " w: " + str(W) + " h: " + str(H),
                    (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0))
        cv2.putText(img, "left: " + str(counter_left) + " right: " + str(counter_right), (0, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0))
        cv2.putText(img, "Distance: " + str(((X + W // 2 - 320) ** 2 + (Y + H // 2 - 240) ** 2) ** 0.5),
                    (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0))
        cv2.putText(img, "Area percentage: " + str(100 * H * W / 640 / 480) + " %", (0, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 0, 0))

        cv2.rectangle(img, (220, 140), (420, 340), (0, 0, 0), 2)

    cv2.imshow('Frame', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.05)

print("x:", x_tmp / counter, "y:", y_tmp / counter)

cap.release()
cv2.destroyAllWindows()
