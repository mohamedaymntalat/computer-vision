import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import pandas as pd


# Function to log attendance to an Excel file
def log_attendance(name):
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {'Name': [name], 'Time': [time_now]}
    df = pd.DataFrame(data)
    attenadance_path = r"C:\Users\moham\Desktop\computer vision\attendance_log.xlsx"

    # Append data to the Excel file (create if doesn't exist)
    with pd.ExcelWriter(attenadance_path, mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, index=False, header=False)


# Function to read QR code from the camera feed
def read_qr_code():
    cap = cv2.VideoCapture(0)  # Open default camera

    while True:
        ret, frame = cap.read()  # Capture frame from the camera
        if ret:
            qr_codes = decode(frame)  # Decode the QR codes in the frame

            for qr in qr_codes:
                qr_data = qr.data.decode('utf-8')  # Extract the QR code data (user name)
                print(f"QR Code Detected: {qr_data}")

                # Log attendance
                log_attendance(qr_data)
                print(f"Attendance logged for {qr_data}")

            # Display the frame
            cv2.imshow('QR Code Reader', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    read_qr_code()
