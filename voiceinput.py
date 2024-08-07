import streamlit as st
import streamlit_scrollable_textbox as stx
from gtts import gTTS
from fpdf import FPDF
import openai   
import os 
import base64
import tempfile
from streamlit_player import st_player
#for audio to text
import speech_recognition as sr
import pyaudio
from pydub import AudioSegment
import os





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
        color: black;
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
# Create a container for the title and button
title_container = st.container()
button_container = st.container()

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
# Function to input audio
def audio():
    # Upload audio file
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])
    # If an audio file is uploaded, display the audio player
    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/mp3')  # Change format as needed
    else:
        audio_file = uploaded_file
# Function to convert audio to wav format
def convert_to_wav(audio_file):
    sound = AudioSegment.from_file(audio_file)
    wav_file = "converted.wav"
    sound.export(wav_file, format="wav")
    return wav_file

 #Language selection
language = st.selectbox("Select language for transcription", 
                        ("en-US", "es-ES", "fr-FR", "de-DE", "hi-IN", "zh-CN", "ta-IN"))

# Function to perform speech recognition
def recognize_speech(language):
    recognizer = sr.Recognizer()

    # Capture audio from the microphone
    with sr.Microphone() as source:
        st.write("Speak something...")
        audio = recognizer.listen(source)

        # Attempt to recognize speech
        try:
            text = recognizer.recognize_google(audio, language=language)
            return text

        except sr.UnknownValueError:
            st.error("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")

# Function to transcribe audio file
def recognize_speech2(audio_file, language):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        text = "Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        text = f"Could not request results from Google Speech Recognition service; {e}"
    return text
    





# Main function for the Streamlit app
def main():
    if one:
        #Button to start voice input
        transcribed_text = recognize_speech(language)
        if transcribed_text:
            Transcribed_input = st.text_area("Transcription Area:", value = transcribed_text, height=200)
    if two:
        #Button to start voice input
        transcribed_text = recognize_speech2(language)
        if transcribed_text:
            Transcribed_input = st.text_area("Transcription Area:", value = transcribed_text, height=200)


           

# Set the title of the app
# st.title("Enter the Prompt")
# Add a text area widget to get user input
user_input = st.text_area("Enter your text here:", key = 'user_input', height=200)





option = st.selectbox("Select the Output Language ?", ("Tamil", "English"))
# dropdown = st.selectbox("Select one of the following default stories: ", ("The Tortoise and the Hare", "Thirukural 411: செல்வத்துட் செல்வம்"))

# Add Submit and Clear buttons
col1, col2,col3,col4, col5= st.columns(5)
with col1:
    if st.button("Generate"):
        submit()
with col5:
    if st.button("Clear"):
        clear()
with button_container:
    if st.button('Audio Input'):
       audio()
       two = True
       
       
with button_container:
    if st.button("Start Speech Recognition"):
        one = True
        main()
        

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


