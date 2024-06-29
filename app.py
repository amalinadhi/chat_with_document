import pandas as pd 
import streamlit as st 
from src.llm.base import LLM


# GLOBAL VARIABLES
START_CHATTING = False
START_INPUT = False

# Page config
st.set_page_config(page_title = "ChatBot", page_icon = "📄")

# Title
st.title("📄 Chat with the Documents")


# Initialize store session
if 'document' not in st.session_state:
    st.session_state.docs = None

if 'model' not in st.session_state:
    st.session_state.model = None 

if "messages" not in st.session_state:
    st.session_state.messages = []



# Side bar
with st.sidebar:
    st.write("## Selamat datang!")
    st.write("Berikut adalah cara menggunakan:")
    st.write("---")

    # 1
    st.write("**1. Masukkan file project yang ingin diolah**")
    uploaded_file = st.file_uploader("Pilih file project, dalam format .xlsx")
    if uploaded_file is not None:
        # Ekstrak filename
        filename = uploaded_file.name
        filename_without_extention = filename.split(".")[0]

        # Read data
        df = pd.read_excel(uploaded_file)
        df.to_csv(f'data/raw/{filename_without_extention}.csv', index=False)
        st.session_state.docs = filename_without_extention + '.csv'

        # Write data
        st.info(f"File '{uploaded_file.name}' sukses dibuka!")
        st.write(df)

    # 2
    st.write("**2. Hubungkan dengan AI Personal Assistant**")
    if st.session_state.docs is not None:        
        if st.button("Click to connect!"):
            try:
                # Koneksi dengan model
                model = LLM()
                model.connect(filepath = st.session_state.docs)
                st.session_state.model = model
                st.info("Sukses terhubung!")
            except Exception as e:
                st.error("Gagal terhubung!", e)
    else:
        st.error("Upload dahulu file project")


# Prompt
if st.session_state.model is not None:
    st.write("Diskusi dengan dokumen disini")
    messages_container = st.container(height=600)
    for i, message in enumerate(st.session_state.messages):
        messages_container.chat_message(message["role"]).markdown(message["content"])
    

    if prompt := st.chat_input("Tulis pertanyaan Anda disini"):
        messages_container.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get responses
        response = st.session_state.model.ask(questions = prompt)
        # response = "ansert + " + prompt

        # Display responses
        messages_container.chat_message("assistant").markdown(response)

        # Append answer to session state
        st.session_state.messages.append({"role": "assistant", "content": response})
