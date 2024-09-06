from flask import Flask, request, jsonify
from googletrans import Translator
import time

app = Flask(__name__)
translator = Translator()

def convert_numbers(text):
    number_map = {
        '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
        '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
    }
    return ''.join([number_map.get(char, char) for char in text])


@app.route('/')
def index():
    return "Hello translation api this side", 200

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()

    pincode = data.get('pincode', "")
    state = data.get('state', "")

    if not pincode or not state:
        return jsonify({'error': 'Please provide both pincode and state for translation.'}), 400

    pincode_converted = convert_numbers(pincode)

    start_time_state = time.time()
    translated_state = translator.translate(state, dest='en').text
    end_time_state = time.time()

    result = {
        "pincode": pincode_converted,
        "state": translated_state,
        # "translation_time": f"{end_time_state - start_time_state:.4f} seconds"
    }

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
