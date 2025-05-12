# Car License Plate Detection & SMS Notification System

This project allows you to capture car license plates using an **ESP32-CAM**, extract the license plate number using **OCR** (Optical Character Recognition), and then send an SMS notification with the car's parking information using a **SIM800L GSM Module**.

## 💡 Project Overview

1. **ESP32-CAM**: Captures the image of a car's license plate.
2. **OCR Processing**: The image is sent to a **Python backend** for Optical Character Recognition (OCR), which extracts the license plate number.
3. **Database Query**: The extracted license plate is then matched against records in a **Supabase database** to retrieve the corresponding phone number.
4. **SMS Notification**: Once a match is found, an SMS notification is sent to the car owner's phone number using the **SIM800L GSM module**.

---

## 📦 Requirements

### 1. **Hardware**
- **ESP32-CAM**: Camera module for capturing the car’s license plate.
- **SIM800L GSM Module**: For sending SMS notifications.
- **Ultrasonic Sensors**: To detect the presence of a car in the parking slot.
- **Servo Motor**: To rotate the camera and aim it at the parking slots.
- **Arduino (for ESP32)**: Controls the ultrasonic sensors, servo, and triggers the camera.

### 2. **Software**
- **Python 3.x**
- **Flask** (Python web framework)
- **EasyOCR** (For Optical Character Recognition)
- **supabase-py** (To interact with the Supabase database)
- **PySerial** (For communicating with the SIM800L GSM module)
- **python-dotenv** (For handling environment variables)

---

## 🛠 Installation

### 1. **Set Up the Supabase Database**
   - Go to [Supabase](https://supabase.io/) and create a new project.
   - Create a table `vehicles` with columns:
     - `license_plate` (text)
     - `phone_number` (text)
   - Get the **API URL** and **API Key** from the Supabase project settings.

### 2. **Set Up Twilio or SIM800L** (Choose One)
   - **For SIM800L GSM Module**: Ensure you have the **SIM800L** connected via serial (e.g., `/dev/ttyUSB0` on Linux or `COMx` on Windows).
   - **For Twilio**: If you decide to use Twilio instead of the SIM800L, create a [Twilio account](https://www.twilio.com/), get the **Account SID**, **Auth Token**, and a **Twilio phone number**.

### 3. **Clone the Repository**
   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Atharvaig/car-license-plate-detection.git
   cd car-license-plate-detection

