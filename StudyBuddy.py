
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image

# Setting up API Key for Gen-AI
genai.configure(api_key= os.getenv('GEN_AI_API'))

def res(prompt, user_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, user_text])
    return response.text
def generate_chat_summary(chat_history):
    chat_summary = "\n".join(chat_history)
    return chat_summary
def input_setup(upload):
    if upload is not None:
        bytes_data = upload.getvalue()

        image_parts = [
            {
                "mime_type": upload.type,
                "data": bytes_data 
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")
def get_res(prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([prompt,image[0]])
    return response.text
st.set_page_config(layout='wide')
st.title("StudyBuddy")
st.header('AI assistant for studies')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
chat_history = st.session_state.chat_history
if "messages" not in st.session_state:
    st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

prompt_for_text  = """
You are an expert in maths, physics, computer science  and engineering. You have a PhD from MIT and work at Google Research.
Your job is to help the student who is entering their problem. Read the text from the user input and and then also check online for solutions and use them as referencefor your answer.
Finally generate a step - by - step solution accordingly by using these references.

"""
prompt_for_image = """
You are an expert in maths, physics, computer science  and engineering. You have a PhD from MIT and work at Google Research.
Your job is to help the student who is uploading the problem as image.
Extract the problem as text from the image and then also check online for solutions and use them as reference.
Finally solve the problem by using these references and provide the results inside a textbox.
"""

for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])    
# with st.container(height=320,border=False):
#     container = st.container(border=True)
#     st.write(" ")
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])
with st.container():    
    user_text = st.chat_input("Chat:")
    if user_text is not None:
        st.session_state.messages.append({"role": "user", "content": user_text})
        response = res(prompt_for_text, user_text)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("user"):
            st.markdown(user_text)
            # st.write(user_text)
        with st.chat_message("assistant"):
            if user_text == "":
                st.write("Please enter some text.")
            else:                                            
               with st.spinner("Thinking..."):
                
                st.markdown(response)
                # st.write(response)

                chat_history.append("You: " + user_text)
                chat_history.append("Bot: " + response)
            
                chat_summary = generate_chat_summary(chat_history)
                st.sidebar.text("Chat Summary:")
                first_user_line = user_text.split("\n")[0]  
                st.sidebar.markdown(f"[{first_user_line}](#{len(chat_history)})")
# if st.button("Upload file"):
    uploaded_file = st.file_uploader(" ", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        if st.button("submit"):  
            try:
                image = Image.open(uploaded_file)
                image_data = input_setup(uploaded_file)
                response = get_res(prompt_for_image, image_data)
                with st.chat_message("user"):
                    st.markdown("Image analysis and result")
                    
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        st.markdown(response)

            except Exception as e:
                st.error(f'Error processing image {e}')

with st.container(height=50, border=False):
    center_text_class = """
    <style>
    .center-text {
        text-align: center;
    }
    </style>
    """
    text_to_center = "Results are experimental and may not always be correct.\nPlease double-check the results"

    st.markdown(center_text_class, unsafe_allow_html=True)
    st.markdown(f"<p class='center-text'>{text_to_center}</p>", unsafe_allow_html=True)

model_response = st.empty()
if st.sidebar.button("+ New Chat"):
    st.session_state.user_text = ""   



