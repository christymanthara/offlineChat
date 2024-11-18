import streamlit as st
import numpy as np
import random
import time

def response_generator(custom_response=None):
    response = (custom_response
        if custom_response is not None
        else random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Hi Boss,Do you need help?",
        ]
        )
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("NVIDIA Minitron offline model")

st.subheader("Chat with the Model")



with st.chat_message("assistant"):
    st.write_stream(response_generator) #random message input
    # st.bar_chart(np.random.randn(30, 3)) #barchart output

# prompt = st.chat_input("Say something")
# if prompt:
#     st.write(f"User has sent the following prompt: {prompt}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What's up. Ask me a question?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    

    response = f"Echo: {prompt}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(response))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})