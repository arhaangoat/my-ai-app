import streamlit as st
from google import genai

st.set_page_config(page_title="Aro AI", page_icon="⚡", layout="centered")

st.markdown(
    """
    <style>
    /* App base background styling */
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1 { color: #00f2fe; text-align: center; font-family: 'Helvetica Neue', sans-serif; }
    
    /* CHAT INPUT BAR: Full pitch black background, crisp white text */
    [data-testid="stChatInput"] textarea {
        background-color: #000000 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    
    /* CHAT MESSAGES TEXT: Force every single letter inside response blocks to be bright readable white */
    .stChatMessage p, .stChatMessage span, .stChatMessage div {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    
    /* USER MESSAGE CONTAINER: Distinct dark blue tint box */
    [data-testid="stChatMessageUser"] {
        background-color: #1e293b !important;
        border-radius: 12px;
    }
    
    /* AI ASSISTANT MESSAGE CONTAINER: Distinct dark gray box */
    [data-testid="stChatMessageAssistant"] {
        background-color: #262730 !important;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("⚡ Aro AI Agent")
st.write("Welcome! This AI app was built solo with Python and Gemini.")


@st.cache_resource
def get_ai_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


client = get_ai_client()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_question := st.chat_input("Ask me anything..."):
    with st.chat_message("user"):
        st.markdown(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response_stream = client.models.generate_content_stream(
                model="models/gemini-3.6-flash", contents=user_question
            )
            for chunk in response_stream:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Configuration Error: {str(e)}"
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
