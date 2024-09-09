import requests
from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()


def convert_numbers(text):
    number_map = {
        '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
        '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
    }
    return ''.join([number_map.get(char, char) for char in text])


def is_english(text):
    return all(ord(char) < 128 for char in text)


@app.route('/')
def index():
    return "Hello translation API this side", 200


@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()

    pincode = data.get('pincode', "")
    state = data.get('state', "")

    if not pincode or not state:
        return jsonify({'error': 'Please provide both pincode and state for translation.'}), 400

    # Check if pincode is in English, otherwise convert
    if is_english(pincode):
        print('Pincode already in English')
        pincode_converted = pincode
    else:
        pincode_converted = convert_numbers(pincode)

    # Verify if the pincode exists using the external API
    service_pincode_url = "http://35.154.99.208:3000/api/user/servicepincode"
    payload = {"pincode": pincode_converted, "state": state}
    print(payload)

    try:
        response = requests.post(service_pincode_url, json=payload)
        response_data = response.json()

        if response.status_code != 200 or "Pincode is not available" in response_data.get("message", ""):
            return jsonify({'error': 'Pincode not found'}), 400

    except Exception as e:
        return jsonify({'error': f'Failed to verify pincode: {str(e)}'}), 500

    # Continue with translation if the pincode is found
    if is_english(state):
        print('State already in English')
        translated_state = state
    else:
        translated_state = translator.translate(state, dest='en').text

    result = {
        "pincode": pincode_converted,
        "state": translated_state,
    }

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
