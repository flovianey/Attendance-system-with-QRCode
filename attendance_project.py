import pymysql
import cv2


# --------------------------------------------DB-----------------------------------------------------------

def mysqlconnection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='1234567890',
        db='student_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            query = "INSERT INTO attendancetable SELECT * FROM registered_student WHERE Student_ID=%s"
            cursor.execute(query, ('data'))
            connection.commit()

        with connection.cursor() as cursor:
            query = "SELECT * FROM attendancetable"
            cursor.execute(query)
            result = cursor.fetchall()
            for rows in result:
                print(rows)


mysqlconnection()


# -----------------------------------------------QRCODE----------------------------------------------

def QRCode_Reader():
    # read the QRCODE image
    img = cv2.imread("QRCodeImage/studentcode.jpg")

    # initialize the cv2 QRCode detector
    detector = cv2.QRCodeDetector()

    # detect and decode
    data, myqrcode, straight_qrcode = detector.detectAndDecode(img)

    # if there is a QR code
    if myqrcode is not None:
        print("Attendance marked for the student ID: {}".format(data))

        mysqlconnection(str(data))
        Attendance()


def Image_capture():
    while True:
        # Activate Camera/webcam
        camera = cv2.VideoCapture(0)

        ret, frame = camera.read()
        cv2.imshow('Attendance system', frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(filename='QRCodeImage/studentcode.jpg', img=frame)
            camera.release()
            print("Image in process")
            # read the QRCODE image
            QRCode_Reader()


def Attendance():
    print("""
    ----------------------------------------
          welcome to attendance system

      A-Maths                     B-English

      C-Computer Science          D-Lab

    ----------------------------------------
    """)
    key = input("Select your course: ")

    if key == "A":
        print("Place your ID Card for Maths attendance")
        Image_capture()

    elif key == "B":
        print("Place your ID Card for English attendance")
        Image_capture()
    elif key == "C":
        print("Place your ID Card for Computer Science attendance")
        Image_capture()
    elif key == "D":
        print("Place your ID Card for Lab attendance")
        Image_capture()


if __name__ == '__main__':
    Attendance()
