import time
from googletrans import Translator

translator = Translator()

def convert_numbers(text):
    number_map = {
        '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
        '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
    }
    return ''.join([number_map.get(char, char) for char in text])

hindi_text = "नमस्ते दुनिया १२३"
marathi_text = "माझे नाव ४५६ आहे"

hindi_text_converted = convert_numbers(hindi_text)
print(hindi_text_converted)
marathi_text_converted = convert_numbers(marathi_text)
print(marathi_text_converted)

start_time_hindi = time.time()
translated_hindi = translator.translate(hindi_text_converted, src='hi', dest='en')
print(f"translated hindi: ${translated_hindi}")
end_time_hindi = time.time()

start_time_marathi = time.time()
translated_marathi = translator.translate(marathi_text_converted, src='mr', dest='en')
end_time_marathi = time.time()

print(f"Translated Hindi: {translated_hindi.text}")
print(f"Time taken for Hindi translation: {end_time_hindi - start_time_hindi:.4f} seconds")

print(f"Translated Marathi: {translated_marathi.text}")
print(f"Time taken for Marathi translation: {end_time_marathi - start_time_marathi:.4f} seconds")
