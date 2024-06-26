import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import cv2
import numpy as np

def main():
    st.title("QR Code and Barcode Scanner App")

    # User input for the number of codes to scan
    num_boxes = st.number_input("Enter the number of codes to scan:", min_value=1, value=1, step=1)

    # Initialize a list to store the scanned codes
    scanned_codes = []

    # Callback function to process frames from the camera
    def video_frame_callback(frame):
        img = frame.to_ndarray(format="bgr24")

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect and decode QR codes and barcodes
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(gray)

        if data and len(scanned_codes) < num_boxes:
            if data not in scanned_codes:
                scanned_codes.append(data)
                st.write(f"Scanned Code: {data}")

        return img

    # Display the camera and scan codes
    webrtc_streamer(
        key="code_scanner",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}),
        video_frame_callback=video_frame_callback
    )

    # Display the scanned codes
    if len(scanned_codes) > 0:
        st.write("Scanned Codes:")
        for code in scanned_codes:
            st.write(code)

if __name__ == "__main__":
    main()
