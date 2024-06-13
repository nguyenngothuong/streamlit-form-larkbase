import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import qrcode
import cv2
import numpy as np

def main():
    st.title("Ứng dụng quét mã QR")
    
    # Người dùng nhập số lượng
    num_boxes = st.number_input("Nhập số lượng mã QR cần quét:", min_value=1, value=1, step=1)
    
    # Hiển thị các ô nhập liệu tương ứng
    qr_codes = []
    for i in range(int(num_boxes)):
        qr_code = st.empty()
        qr_codes.append(qr_code)
    
    # Hàm xử lý frame từ camera
    def video_frame_callback(frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Chuyển đổi hình ảnh sang grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Tạo đối tượng QRCodeDetector
        qr_detector = cv2.QRCodeDetector()
        
        # Phát hiện và giải mã mã QR
        data, _, _ = qr_detector.detectAndDecode(gray)
        
        if data:
            for i, qr_code in enumerate(qr_codes):
                if qr_code.text_input("", value=data, key=f"qr_code_{i}"):
                    break
        
        return img
    
    # Hiển thị camera và quét mã QR
    webrtc_streamer(
        key="qr_scanner",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}),
        video_frame_callback=video_frame_callback
    )
    
    # Xử lý khi người dùng nhấn nút Submit
    if st.button("Submit"):
        st.write("Các mã QR đã nhập:")
        for i, qr_code in enumerate(qr_codes):
            st.write(f"{i+1}. {qr_code.text_input('', key=f'qr_code_{i}')}")

if __name__ == "__main__":
    main()
