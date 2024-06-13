import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import numpy as np
from pyzbar import pyzbar

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
        barcodes = pyzbar.decode(img)
        
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            
            for i, qr_code in enumerate(qr_codes):
                if qr_code.text_input("", value=barcode_data, key=f"qr_code_{i}"):
                    break
        
        return img
    
    # Hiển thị camera và quét mã QR
    webrtc_streamer(key="qr_scanner", video_frame_callback=video_frame_callback)
    
    # Xử lý khi người dùng nhấn nút Submit
    if st.button("Submit"):
        st.write("Các mã QR đã nhập:")
        for i, qr_code in enumerate(qr_codes):
            st.write(f"{i+1}. {qr_code.text_input('', key=f'qr_code_{i}')}")

if __name__ == "__main__":
    main()
