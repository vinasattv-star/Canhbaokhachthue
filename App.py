import streamlit as st
import face_recognition
import numpy as np
import os
from PIL import Image

# Thư mục lưu ảnh cảnh báo
DATA_DIR = "warning_faces"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

st.title("🚨 Hệ thống cảnh báo khách thuê xe (Face Recognition)")

menu = ["Thêm vào danh sách cảnh báo", "Kiểm tra khách mới"]
choice = st.sidebar.selectbox("Chọn chức năng", menu)

def save_image(img_file, name, note):
    path = os.path.join(DATA_DIR, f"{name}.jpg")
    with open(path, "wb") as f:
        f.write(img_file.getbuffer())
    with open(os.path.join(DATA_DIR, f"{name}.txt"), "w", encoding="utf-8") as f:
        f.write(note)

def get_face_encoding(img_path):
    try:
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            return encodings[0]
        else:
            return None
    except Exception as e:
        print("Encoding error:", e)
        return None

def check_image(img_file):
    new_img_path = "temp_check.jpg"
    with open(new_img_path, "wb") as f:
        f.write(img_file.getbuffer())

    new_encoding = get_face_encoding(new_img_path)
    if new_encoding is None:
        return None, None

    for file in os.listdir(DATA_DIR):
        if file.endswith(".jpg"):
            db_img_path = os.path.join(DATA_DIR, file)
            db_encoding = get_face_encoding(db_img_path)
            if db_encoding is not None:
                result = face_recognition.compare_faces([db_encoding], new_encoding, tolerance=0.5)
                if result[0]:
                    name = file.replace(".jpg", "")
                    note_file = os.path.join(DATA_DIR, f"{name}.txt")
                    note = ""
                    if os.path.exists(note_file):
                        with open(note_file, "r", encoding="utf-8") as f:
                            note = f.read()
                    return name, note
    return None, None

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
