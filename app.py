from flask import Flask, render_template, request, send_file, redirect, url_for
from gtts import gTTS
import openai
import os
import base64

app = Flask(__name__)
openai.api_key = "sk-proj-fePlCq2Vh56F1KglJDXbT3BlbkFJTdLnvyq7Y9mrinJFs1u3"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['user_input']
    option = request.form['option']

    user_input += ",\n Get the meaning only in " + option + " language"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "About Tamil"},
            {"role": "user", "content": user_input}
        ]
    )

    output = response['choices'][0]['message']['content']
    myobj = gTTS(text=output, lang='ta', slow=False)
    myobj.save("static/tamil.mp3")

    return render_template('index.html', output=output, audio_file="tamil.mp3")

@app.route('/download_audio')
def download_audio():
    return send_file("static/tamil.mp3", as_attachment=True)

@app.route('/clear')
def clear():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
