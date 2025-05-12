import os
from flask import Flask, request, jsonify
import easyocr
import serial
import time
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SIM800L_PORT = os.getenv("SIM800L_PORT")  # Example: '/dev/ttyUSB0'
SIM800L_BAUDRATE = os.getenv("SIM800L_BAUDRATE")  # Example: 9600
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize EasyOCR
reader = easyocr.Reader(['en'])

# Setup serial connection for SIM800L
gsm = serial.Serial(SIM800L_PORT, SIM800L_BAUDRATE, timeout=1)

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Get the uploaded image
        file = request.files['file']
        
        # Read the image with EasyOCR
        result = reader.readtext(file.read())

        # Extract the license plate text from the OCR result
        plate_text = ""
        for detection in result:
            plate_text += detection[1] + " "

        plate_text = plate_text.strip()

        if plate_text:
            # Search for the license plate in Supabase DB
            response = supabase.table('vehicles').select('*').eq('license_plate', plate_text).execute()

            if response.data:
                phone_number = response.data[0]['phone_number']
                message = f"Your car with plate {plate_text} is parked in slot 1."  # Example message
                # Send SMS using SIM800L
                send_sms(phone_number, message)

                return jsonify({"message": "SMS sent successfully!", "license_plate": plate_text}), 200
            else:
                return jsonify({"message": "License plate not found in database."}), 404
        else:
            return jsonify({"message": "No license plate detected."}), 400
    except Exception as e:
        return jsonify({"message": f"Error processing image: {str(e)}"}), 500

def send_sms(phone_number, message):
    try:
        # Initialize SIM800L GSM module
        send_at_command('AT')  # Check if the module is responding
        send_at_command('AT+CMGF=1')  # Set SMS mode to text
        send_at_command(f'AT+CMGS="{phone_number}"')  # Set the recipient phone number
        send_at_command(message + chr(26))  # Send the message followed by CTRL+Z to send the SMS

        print(f"SMS sent to {phone_number}: {message}")
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")

def send_at_command(command):
    gsm.write((command + '\r').encode())
    time.sleep(1)
    response = gsm.read_all()
    print(response.decode())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
