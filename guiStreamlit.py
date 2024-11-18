import streamlit as st
import numpy as np
import random
import time
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch



# print(torch.cuda.is_available())

# Load the model and tokenizer from local storage
tokenizer = AutoTokenizer.from_pretrained("./hf_cache/models--nvidia--Minitron-4B-Base/snapshots/d6321f64412982046a32d761701167e752fedc02")
model = AutoModelForCausalLM.from_pretrained("./hf_cache/models--nvidia--Minitron-4B-Base/snapshots/d6321f64412982046a32d761701167e752fedc02",
                                             torch_dtype=torch.bfloat16,
                                             device_map="auto",
                                             offload_folder="./offload_dir"
                                             )

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)



# Function to generate a response using the model
def generate_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")  # Encode the user's input
    outputs = model.generate(inputs, max_length=200, num_return_sequences=1)  # Generate a response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)  # Decode the response
    return response



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
    yield ""

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

     # Generate response from the model
    with st.spinner("Thinking..."):
        response = generate_response(prompt)

    # Stream the assistant's response word by word
    with st.chat_message("assistant"):
        st.write_stream(response_generator(response))
    

    # response = f"Echo: {prompt}"

    # Display assistant response in chat message container
    # with st.chat_message("assistant"):
    #     response = st.write_stream(response_generator(response))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


