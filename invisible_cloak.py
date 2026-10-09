import cv2
import numpy as np
import time


# ==========================================
# 1. START CAMERA
# ==========================================

cap = cv2.VideoCapture(0)

# Camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("ERROR: Camera open nahi hua!")
    exit()

print("Camera starting...")
time.sleep(2)


# ==========================================
# 2. CAPTURE BACKGROUND
# ==========================================

print("\n===================================")
print("BACKGROUND CAPTURE")
print("===================================")
print("Camera ke saamne se completely hat jao.")
print("Koi BLACK object bhi frame mein nahi hona chahiye.")

for i in range(5, 0, -1):

    ret, frame = cap.read()

    if not ret:
        print("ERROR: Camera frame nahi mil raha!")
        cap.release()
        exit()

    frame = cv2.flip(frame, 1)

    cv2.putText(
        frame,
        f"Background in {i}",
        (400, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (255, 255, 255),
        4
    )

    cv2.imshow("Setup", frame)

    if cv2.waitKey(1000) & 0xFF == ord("q"):
        cap.release()
        cv2.destroyAllWindows()
        exit()


# Capture background
ret, background = cap.read()

if not ret:
    print("ERROR: Background capture failed!")
    cap.release()
    exit()

background = cv2.flip(background, 1)

cv2.destroyWindow("Setup")

print("\nBackground captured successfully!")
print("Ab BLACK object camera ke saamne lao.")


# ==========================================
# 3. MAIN LOOP
# ==========================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("ERROR: Frame read nahi ho raha!")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)


    # ======================================
    # 4. CONVERT BGR TO HSV
    # ======================================

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    # ======================================
    # 5. BLACK COLOR DETECTION
    # ======================================

    # Black = low brightness/value
    #
    # H = 0 - 180
    # S = 0 - 255
    # V = 0 - 60

    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 60])

    mask = cv2.inRange(
        hsv,
        lower_black,
        upper_black
    )


    # ======================================
    # 6. REMOVE SMALL NOISE
    # ======================================

    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )


    # ======================================
    # 7. FILL SMALL HOLES
    # ======================================

    kernel = np.ones((7, 7), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )


    # ======================================
    # 8. SMOOTH EDGES
    # ======================================

    mask = cv2.GaussianBlur(
        mask,
        (5, 5),
        0
    )


    # ======================================
    # 9. CREATE INVERSE MASK
    # ======================================

    inverse_mask = cv2.bitwise_not(mask)


    # ======================================
    # 10. KEEP NORMAL PART
    # ======================================

    normal_part = cv2.bitwise_and(
        frame,
        frame,
        mask=inverse_mask
    )


    # ======================================
    # 11. GET BACKGROUND
    # ======================================

    invisible_part = cv2.bitwise_and(
        background,
        background,
        mask=mask
    )


    # ======================================
    # 12. COMBINE BOTH
    # ======================================

    result = cv2.add(
        normal_part,
        invisible_part
    )


    # ======================================
    # 13. DISPLAY RESULT
    # ======================================

    cv2.imshow(
        "Invisible Cloak - BLACK",
        result
    )


    # Show mask for debugging
    cv2.imshow(
        "Black Detection",
        mask
    )


    # ======================================
    # 14. EXIT
    # ======================================

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==========================================
# 15. RELEASE CAMERA
# ==========================================

cap.release()
cv2.destroyAllWindows()

print("Program closed.")