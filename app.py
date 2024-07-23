from flask import Flask, request, jsonify, send_from_directory
import openai
import requests

app = Flask(__name__)

# Hardcoded API keys
OPENAI_API_KEY = 'sk-proj-'  # Your actual OpenAI API key
ELEVENLABS_API_KEY = 'sk_'  # Your actual ElevenLabs API key
VOICE_ID = 'NIFHM4Vq7RGiZjrapWMb'  # This is my TARS voice ID Key :)

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

def text_to_speech(text, voice_id):
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
    headers = {
        'xi-api-key': ELEVENLABS_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'voice_settings': {
            'stability': 0.75,
            'similarity_boost': 0.75
        }
    }
    print("Headers:", headers)  # Print headers for debugging
    response = requests.post(url, json=data, headers=headers)
    print("Response Status Code:", response.status_code)  # Print response status code
    print("Response Text:", response.text)  # Print response text
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    user_input = data.get('text')
    if not user_input:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        # Generate AI response
        ai_response = generate_response(user_input)
        # Convert AI response to speech
        audio = text_to_speech(ai_response, VOICE_ID)
        return audio, 200, {'Content-Type': 'audio/wav'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
