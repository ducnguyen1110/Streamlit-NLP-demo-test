import streamlit as st

st.title("Demo")
st.write("xin chao cac ban")
st.text("hehehe")
st.header("phan tích văn bản")
st.markdown("**cc** haha *ha*")
with st.echo():
    text = "NLP Demo".lower()
    st.write("Result: ", text)
st.logo("photo.png")
st.image("photo.png")

option = st.selectbox(
    "Chọn tác vụ của NLP",
    ["Tóm tắt", "Dịch máy", "Hỏi đáp"],
    )
st.write("You selected:", option)
status = st.checkbox("Hiển thị văn bản")
if status:
    st.write(status)

st.slider("Nguong gia tri", min_value=1.0, max_value=5.0, step=0.5)
name = st.text_input("Your name:")
st.write(name)
age = st.number_input("Your age:")
st.write(age)
if st.button("Run"):
    st.write(name, age)
uploaded_file = st.file_uploader("Tai file len", type=["txt", "csv", "pdf"])
if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    st.write(content[:10])
if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input("Nhập câu hỏi vào đây")
if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    response = "Đây là NLP Model"
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
if "count" not in st.session_state:

    st.session_state.count = 0

 

if st.button("Increment"):

    st.session_state.count += 1

 

st.write("Count: ", st.session_state.count)