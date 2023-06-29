# importing libraries mentioned in requirement.txt
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
from hugchat.login import Login

# initializing streamlit; setting page title
st.set_page_config(page_title="SERPy")

# session_state variables declaration
if 'disable' not in st.session_state:
    st.session_state.disable = True
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None

# initializing login page; includes login form and sidebar; initializing chatbot
if st.session_state.disable :
    with st.form(key="Login_form"):
        st.markdown('''## SERPy🐍''')
        colored_header(label='', description='', color_name='red-70')
        hf_email = st.text_input("Email: ",placeholder="Email ID", label_visibility="collapsed")
        hf_pass = st.text_input("Password: ",type='password', placeholder='Password', label_visibility="collapsed")
        submitted = st.form_submit_button("Login")
        if submitted:
            with st.spinner(text="Logging in..."):
                sign = Login(hf_email, hf_pass)
                cookies = sign.login()
                sign.saveCookies()
                chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
                st.session_state.chatbot = chatbot
                st.session_state.disable = False
                st.write(st.session_state.disable)
# rerunning app after successful login                
                st.experimental_rerun()
        st.markdown('''_Don't have Hugging Face account? [Sign up!](https://huggingface.co/join)_''')
    with st.sidebar:
        st.markdown('''
            _Enter your Hugging Face account details to login_ 
            ## About
            **SERPy** tries to parse user queries from natural language to **S**QL, **E**xcel, **R** and **Py**thon.
            This app is based upon a LLM-powered chatbot, and is built using:
            - [Streamlit](https://streamlit.io/) UI
            - [HugChat](https://github.com/Soulter/hugging-chat-api) API
            - [OpenAssistant/oasst-sft-6-llama-30b-xor](https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor) LLM model

            **When you use this app, it means that you have agreed to the following two requirements of the HuggingChat:**

            1. AI is an area of active research with known problems such as biased generation and misinformation. Do not use this application for high-stakes decisions or advice.
            2. Your conversations will be shared with model authors.

            ''')
        add_vertical_space(5) 
        st.write('Made with ♥️  by [ravishe8](https://github.com/ravishe8?tab=repositories)')

# initializing query resolution page; setting prompt; displaying response
else :
    with st.container():
# removing input text after hitting enter
        if 'query' not in st.session_state:
            st.session_state.query = ''
        def submit():
            st.session_state.query = st.session_state.input
            st.session_state.input = ''          
        display_text = st.text_input("Query: ", "", placeholder="Enter your query", label_visibility="collapsed", key="input", on_change=submit)        
        user_input = st.session_state.query
        if user_input :
            colored_header(label='', description='', color_name='red-70')
            st.write("*"+user_input+"*")
# setting prompt; integrating user input in prompt
            prompt = f"""You are an expert on data analytics.
                         You are quite proficient in spreadsheet skills and in using Excel.
                         You are also well versed in Python, R and SQL programming languages.
                         You will be provided with a query text delimited by triple backticks.
                         You have to resolve this query in SQL, R, Python and Excel in the following format:
                         SQL - ...
                         R - ...
                         Python - ...
                         Excel - ...
                         Do not explain the codes. Do not ask any follow up questions.
                         ```{user_input}```
                         """
            response = st.session_state.chatbot.chat(prompt)
            if response :
                st.write(response)
# end 86
