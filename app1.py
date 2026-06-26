import streamlit as st

st.title("Chatbot KHÔNG CÓ session_state (Mất trí nhớ)")

# Tạo một biến danh sách thông thường để lưu tin nhắn
# CỨ MỖI LẦN BẠN NHẤN ENTER GỬI TIN NHẮN, DÒNG NÀY SẼ CHẠY LẠI
# VÀ NÓ SẼ RESET CÁI MẢNG NÀY THÀNH RỖNG [ ] TỪ ĐẦU!
messages = []

prompt = st.chat_input("Nhập câu hỏi vào đây")

if prompt:
    # Thêm câu hỏi của bạn vào danh sách
    messages.append({"role": "user", "content": prompt})
    
    # Giả lập câu trả lời của AI
    response = "Tôi là AI mất trí nhớ..."
    messages.append({"role": "assistant", "content": response})

# Vòng lặp in tin nhắn ra màn hình
for message in messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])