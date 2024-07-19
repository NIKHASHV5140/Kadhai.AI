import streamlit as st
import streamlit_scrollable_textbox as stx
from gtts import gTTS
from fpdf import FPDF
import requests
import random
import openai   
import os 
import base64
import tempfile
from streamlit_player import st_player



openai.api_key = "sk-proj-fePlCq2Vh56F1KglJDXbT3BlbkFJTdLnvyq7Y9mrinJFs1u3"

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }
    .title {
        background-color: blue;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
    }
    .subtitle {
        font-size: 18px;
        margin-bottom: 20px;
    }
    .text-input {
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: blue;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: blue;
    }
    .download-link {
        text-decoration: none;
        color: black;
        font-weight: bold;
    }
    .video-container {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Set the title of the app
st.title("Kathai.AI")

#user_text=""
lang="ta"

# Initialize session state variables
if 'text1' not in st.session_state:
    st.session_state.text1 = ""
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Function to handle submit action
def submit():
    st.session_state.text1 = st.session_state.user_input
    st.session_state.submitted = True

# Function to handle clear action
def clear(): 
    st.session_state.text1 = ""   
    #st.session_state.user_input = ""
    st.session_state.submitted = False

# Set the title of the app
# st.title("Enter the Prompt")
# Add a text area widget to get user input
user_input = st.text_area("Enter your text here:", key='user_input', height=200)

option = st.selectbox("Select the Output Language ?", ("Tamil", "English"))
# dropdown = st.selectbox("Select one of the following default stories: ", ("The Tortoise and the Hare", "Thirukural 411: செல்வத்துட் செல்வம்"))

# Add Submit and Clear buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Generate"):
        submit()
with col2:
    if st.button("Clear"):
        clear()

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download Audio</a>'    
    return href


# Display the input text if submitted
if st.session_state.submitted:  
    st.write(" Hold on a sec, Retrieving Content. ")
    #st.write(lang.upper())    
    user_input+="," 
    user_input+="\n Get the meaning only in "+option+" language"
    #st.write(user_input)

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
            {"role": "system", "content": "About Tamil"},
            {"role": "user", "content": user_input}
            ]
    
    )

    output=response['choices'][0]['message']['content']
    #print(output)
    myobj = gTTS(text=output, lang='ta', slow=False)
    myobj.save("tamil.mp3")
    #st.audio("open tamil.mp3")
    #st.write(st.session_state.text1)
    #st.write(output)
    stx.scrollableTextbox(output, height=250)  
    # Auto Playing Audio
    st.write("# Auto-playing Audio!")
    autoplay_audio("tamil.mp3")

    #Download Audi Link
    st.markdown(get_binary_file_downloader_html('tamil.mp3', 'Audio'), unsafe_allow_html=True)

    # Define the video URL or local path
    video_url = 'https://www.youtube.com/watch?v=jPwe1s__9fs&t=139s'  # Replace with your video URL

    # Create a button
    if st.button('Play Video'):
        st_player(video_url) 


#Quiz
# Function to make API call to ChatGPT and generate multiple-choice questions
def generate_mcq(prompt):
    api_key = 'YOUR_API_KEY'
    api_url = 'https://api.openai.com/v1/engines/davinci-codex/completions'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        'prompt': prompt,
        'max_tokens': 1000  # Adjust max tokens based on your prompt length
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        choices = []
        # Generate multiple plausible choices
        for _ in range(3):  # Generate 3 choices (A, B, C)
            choice = response.json()['choices'][0]['text'].strip()
            choices.append(choice)

        # Shuffle choices and add correct answer
        correct_answer = random.choice(choices)
        choices.append(correct_answer)
        random.shuffle(choices)

        return choices
    else:
        return ["Error generating question."]

# Streamlit app
def main():
    st.title('Quiz Time!')

    if st.button('Generate MCQ'):
        if response:
            choices = generate_mcq(response)
            if len(choices) >= 4:
                st.write("Choose the correct answer:")
                st.write(f"A) {choices[0]}")
                st.write(f"B) {choices[1]}")
                st.write(f"C) {choices[2]}")
                st.write(f"D) {choices[3]}")
            else:
                st.error("Error generating choices.")
        else:
            st.warning('Please enter a prompt.')

if __name__ == '__main__':
    main()
