import streamlit as st

def main():
    st.title("Ứng dụng quét mã QR")
    
    # Người dùng nhập số lượng
    num_boxes = st.number_input("Nhập số lượng mã QR cần quét:", min_value=1, value=1, step=1)
    
    # Hiển thị các ô nhập liệu tương ứng
    qr_codes = []
    for i in range(int(num_boxes)):
        st.write(f"Mã QR {i+1}:")
        qr_code = st.empty()
        qr_codes.append(qr_code)
    
    # Thêm mã JavaScript để quét mã QR bằng camera
    scanner_script = """
    <script src="https://rawgit.com/schmich/instascan-builds/master/instascan.min.js"></script>
    <script>
        var scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
        scanner.addListener('scan', function (content) {
            alert("Mã QR đã quét: " + content);
            var index = window.location.search.split("index=")[1];
            var qrCodeElement = window.parent.document.querySelectorAll('.element-container')[index].querySelector('.stTextInput input');
            qrCodeElement.value = content;
        });
        Instascan.Camera.getCameras().then(function (cameras) {
            if (cameras.length > 0) {
                scanner.start(cameras[0]);
            } else {
                console.error('Không tìm thấy camera.');
            }
        }).catch(function (e) {
            console.error(e);
        });
    </script>
    """
    
    # Hiển thị khung preview camera
    for i in range(int(num_boxes)):
        st.write(f'<iframe src="/?index={i}" width="400" height="300" frameborder="0"></iframe>', unsafe_allow_html=True)
        st.write(scanner_script, unsafe_allow_html=True)
    
    # Xử lý khi người dùng nhấn nút Submit
    if st.button("Submit"):
        st.write("Các mã QR đã nhập:")
        for i, qr_code in enumerate(qr_codes):
            st.write(f"{i+1}. {qr_code.text_input('')}")

if __name__ == "__main__":
    main()