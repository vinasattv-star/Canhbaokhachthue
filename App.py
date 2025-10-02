import streamlit as st
from deepface import DeepFace
import os

# Thư mục lưu ảnh cảnh báo
DATA_DIR = "warning_faces"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

st.title("🚨 Hệ thống cảnh báo khách thuê xe")

menu = ["Thêm vào danh sách cảnh báo", "Kiểm tra khách mới"]
choice = st.sidebar.selectbox("Chọn chức năng", menu)

# Hàm lưu ảnh
def save_image(img_file, name, note):
    path = os.path.join(DATA_DIR, f"{name}.jpg")
    with open(path, "wb") as f:
        f.write(img_file.getbuffer())
    with open(os.path.join(DATA_DIR, f"{name}.txt"), "w", encoding="utf-8") as f:
        f.write(note)

# Hàm kiểm tra ảnh mới
def check_image(img_file):
    new_img_path = "temp_check.jpg"
    with open(new_img_path, "wb") as f:
        f.write(img_file.getbuffer())

    for file in os.listdir(DATA_DIR):
        if file.endswith(".jpg"):
            db_img_path = os.path.join(DATA_DIR, file)
            try:
                result = DeepFace.verify(new_img_path, db_img_path, model_name="Facenet", enforce_detection=False)
                if result["verified"]:
                    name = file.replace(".jpg", "")
                    note_file = os.path.join(DATA_DIR, f"{name}.txt")
                    note = ""
                    if os.path.exists(note_file):
                        with open(note_file, "r", encoding="utf-8") as f:
                            note = f.read()
                    return name, note
            except Exception:
                continue
    return None, None

# Giao diện
if choice == "Thêm vào danh sách cảnh báo":
    st.header("📌 Thêm khách thuê vào danh sách cảnh báo")
    name = st.text_input("Tên hoặc biệt danh")
    note = st.text_area("Ghi chú (số điện thoại, lý do cảnh báo...)")
    img_file = st.file_uploader("Tải ảnh lên", type=["jpg", "jpeg", "png"])

    if img_file and name:
        if st.button("Lưu"):
            save_image(img_file, name, note)
            st.success(f"✅ Đã lưu {name} vào danh sách cảnh báo")

elif choice == "Kiểm tra khách mới":
    st.header("🔎 Kiểm tra khách thuê mới")
    img_file = st.file_uploader("Tải ảnh khách mới", type=["jpg", "jpeg", "png"])

    if img_file:
        if st.button("Kiểm tra"):
            name, note = check_image(img_file)
            if name:
                st.error(f"⚠️ Trùng khớp với người trong danh sách cảnh báo: {name}")
                st.write(f"📋 Ghi chú: {note}")
            else:
                st.success("✅ Không tìm thấy trong danh sách cảnh báo")
