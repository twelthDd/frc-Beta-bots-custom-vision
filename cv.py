import cv2

cap = cv2.VideoCapture(0)

width  = cap.get(3)  # float `width`
height = cap.get(4)  # float `height`

print(f"{width}\n{height}")

cap.release()