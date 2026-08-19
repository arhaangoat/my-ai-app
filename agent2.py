import streamlit as st
from google import genai

st.set_page_config(page_title="Custom AI Assistant", page_icon="⚡", layout="centered")

API_KEY = st.secrets["AQ.Ab8RN6LGRjaywIAEjqmLbSq6cC0cJurkFPLg_SvnEsxaW4thvw"]

st.markdown(
    """
    <style>
    /* Make the base app background dark */
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1 { color: #00f2fe; text-align: center; font-family: 'Helvetica Neue', sans-serif; }
    
    /* TARGET STREAMLIT CHAT BAR: Turn it dark gray and make typing text crisp white */
    [data-testid="stChatInput"] textarea {
        background-color: #262730 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚡ Aro AI Agent")
st.write("Welcome! This AI app was built solo with Python and Gemini.")

@st.cache_resource
def get_ai_client():
    return genai.Client(api_key=API_KEY)

client = get_ai_client()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversion log history blocks
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
                model="gemini-2.5-flash",
                contents=user_question
            )
            for chunk in response_stream:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Configuration Error: Verify API connection strings! ({str(e)})"
            message_placeholder.markdown(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
