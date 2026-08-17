import streamlit as st
import requests
import time
from groq import Groq

# ========== PAGE CONFIGURATION==========
st.set_page_config(
    page_title="mumu AI chatbot",
    page_icon="🤖",
    layout="centered"
)

# ========== API ===========
API_KEY = st.secrets["API_KEY"]
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"

#========== CHAT HISTORY ===========
if "messages" not in st.session_state:
    st. session_state. messages = []

if "dark_mode" not in st.session_state:
     st.session_state.dark_mode = True

 #========== chatgpt style ui ==========
 
if st.session_state.dark_mode:
     bg_color = "#0d1117"
     text_color = "#e6edf3"
else:
     bg_color = "#ffffff"
     text_color = "#000000"

if st.session_state.dark_mode:
     assistant_bg = "#161b22"
     assistant_text = "#e6edf3"
     assistant_border = "#30363d" 
else:
     assistant_bg = "#f1f3f5"
     assistant_text = "#1f2937"
     assistant_border = "#d1d5db"

st.markdown(f"""
<style>
body {{
     transition: none;
}}

/* background */
[data-testid="stAppViewContainer"] {{
    background-color: {bg_color};
    color: {text_color};
}}

/* center chat width */
.block-container {{
max-width: 750px;
padding_top: 2rem;
}}

/* user bubble */
.user-bubble {{
background-color: #1f6feb;
color: white;
padding: 12px 15px;
border-radius: 18px 18px 4px 18px;
margin: 10px 0 10px auto;
max-width: 75%;
width: fit-content;
text-align: left;
line-height: 1.5;
word-wrap: break-word;
}}

/* assistant bubble */
.assistant-bubble {{
background: {assistant_bg};
color: {assistant_text};
padding: 12px 15px;
border : 1px solid {assistant_border};
border-radius: 18px 18px 18px 4px;
margin: 10px auto 10px 0;
max-width: 80%;
width: fit-content;
line-height: 1.5;
word-wrap: break-word;
}}

/* input box */
.input-box {{
background-color: #161b22 !important;
color: #e6edf3 !important;
border: 1px solid #30363d !important;
}}

/*Chat input text*/
.stChatInput textarea {{
     color: #000000 !important;
     caret-color: #000000 !important;
}}

/*chat input placeholder*/
.stChatInput textarea::placeholder{{
    color: #777777 !important;
}}
/*==========MOBILE RESPONSIVE DESIGN==========*/
@media (max-width: 768px) {{

    /* Main chat area* /
    .block-container{{
        max-width:100% !important;
        padding: 1rem !important;
    }}
    
    /* Make the title smaller on phones */
    h1 {{
         font-size: 2rem !important;
    }}
    
    /* Smaller subtitle */
    p {{
        font-size: 0.9rem;
    }}
    
    /* User messages */
    .user-bubble {{
         max-width: 90%;
         padding: 10px 12px;
         font-size: 0.95rem;
    }}
    
    /*AI messages */
    .assistant-bubble {{
         max-width: 95%;
         padding: 10px 12px;
         font-size:0.95rem;
    }}
    
    /* Chat input */
    .stChatInput {{
         width: 100% !important;
    }}
    
    .stChatInput textarea {{
         font-size: 16px !important;
    }}
}}

</style>
""", unsafe_allow_html=True)

 #========== SIDEBAR ==========
with st.sidebar:
        st.title(" ⚙️ Controls")

        if st.button ("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

        st.toggle("🌙 Dark Mode", key="dark_mode")
        
        st.markdown ("---")
        st.write ( "mumu AI chatbot , CHATGPT clone")
        st.write ( " streaming UI")
        st.write ("memory enabled")

  # ========= TITLE ==========
st.title ("mumu AI chatbot 🤖")
st.caption ("A simple AI chatbot, a clone of the chatgpt interface built with streamlit")

#========= FUNCTIONS ==========
def get_response(prompt):
    try:
        client = Groq(api_key=API_KEY)

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant.Give clear, short, direct ,concise answers unless the user asks for more detail. "
            },
            *st.session_state.messages,
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"API Error: {e}"

#========== DISPLAY CHAT ==========
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">{message[ "content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-bubble">{message["content"]}</div>', unsafe_allow_html= True)

  #========== INPUT ==========
user_input = st.chat_input("message mumu bot here...")

if user_input:
     #show user message
     st.session_state.messages.append({"role":"user","content": user_input})

     st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html= True)
     #place holder for streaming effect
     placeholder= st.empty()
     reply = get_response(user_input)

     # ========== STREAMING EFFECT ==========
     streamed_text= ""
     for char in reply:
          streamed_text += char
          placeholder.markdown(f'<div class=" assistant-bubble">{streamed_text}</div>', unsafe_allow_html=True)
          time.sleep(0.02)

     #save final message 
     st.session_state.messages.append({"role":"assistant","content": reply}) 
