import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import requests
import base64


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Radebot",
    page_icon=":sparkles:",  # Favicon emoji
    layout="centered",  # Page layout option
)

image_url = "https://raw.githubusercontent.com/CRNOHD/radebot/main/hat2.gif"
response = requests.get(image_url)
image_data = response.content

# Convert the image data to a data_url
data_url = base64.b64encode(image_data).decode("utf-8")

# Display the image in Streamlit
st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="Radebot">',
    unsafe_allow_html=True,
)

GOOGLE_API_KEY = os.getenv("AIzaSyDhKHiVyXhINaIL6NYHLtASgoaj3NvSBqg")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("🤖 Radebot")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Rade...")
if user_prompt:
    if user_prompt in ("Rade", "About"):
        st.chat_message("assistant").markdown("✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨\nHello there! 👋 My name is Ramdane Bouroga, 😊 and I'm the proud developer of this chatbot. 😁 Feel free to contact me at crnohd@gmail.com if you have any questions or feedback. 😉\n✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨")
    else:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
