from scipy.spatial import distance
from imutils import face_utils
from pygame import mixer
import imutils
import dlib
import cv2
from twilio.rest import Client
import yagmail
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import json  # To load the JSON file with profiles
import pyttsx3  # For Voice message (Text-to-Speech)

# Initialize Pygame mixer for alert sound
mixer.init()
mixer.music.load("music.wav")

# Twilio Credentials
TWILIO_PHONE_NUMBER = '+13343264158'
TO_PHONE_NUMBER = '+918097830842'
TWILIO_ACCOUNT_SID = 'AC8a858a6ae375cf24ecc0dfd8836eb3ed'
TWILIO_AUTH_TOKEN = '7e6b149341d8db9c3e3d4a7c3dc5d5a5'

# Email Credentials
EMAIL_ADDRESS = "zeel.shah2021@vitstudent.ac.in"  # Sender email address
EMAIL_PASSWORD = "tzjv fvzr raha jbae"  # App-specific password
TO_EMAIL = "ananyag1905@gmail.com"  # Emergency contact email address

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Initialize Yagmail client
yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD)

# Initialize Text-to-Speech engine (pyttsx3) for voice message alert
engine = pyttsx3.init()


# Load driver profiles from JSON file
def load_driver_profiles():
    with open("driver_profiles.json", "r") as f:
        profiles = json.load(f)
    return profiles["profiles"]


# Function to send an SMS alert
def send_sms_alert():
    message = client.messages.create(
        to=TO_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        body="ALERT: Driver showing signs of drowsiness. Please check on them immediately!"
    )
    print(f"SMS alert sent: {message.sid}")


# Function to send an Email alert
def send_email_alert():
    try:
        yag.send(
            to=TO_EMAIL,
            subject="Drowsiness Alert: Immediate Attention Needed!",
            contents="ALERT: Driver is showing signs of drowsiness. Please check on them immediately!"
        )
        print("Email alert sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Function for voice message alert (Text-to-Speech)
def send_voice_message_alert():
    message = "ALERT: Driver showing signs of drowsiness. Please check on them immediately!"
    engine.say(message)
    engine.runAndWait()


# Function to send all preferred alerts
def send_alerts(preferred_alerts):
    # Convert preferred alerts to lowercase and split by comma
    alerts = [alert.strip().lower() for alert in preferred_alerts.split(",")]

    # Send alerts based on preferences
    if "sms" in alerts:
        send_sms_alert()
    if "email" in alerts:
        send_email_alert()
    if "voice" in alerts:
        send_voice_message_alert()


# Eye Aspect Ratio function
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


# Parameters
thresh = 0.25
frame_check = 20
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
cap = cv2.VideoCapture(0)
flag = 0


# Function for profile selection dialog from JSON
def select_profile(profiles):
    # Get profile names from the JSON
    profile_names = [profile["name"] for profile in profiles]

    # Prompt for profile selection
    profile = simpledialog.askstring("Profile Selection", "Select Driver Profile:\n" + "\n".join(profile_names))

    # Validate profile selection
    profile_match = None
    for p in profiles:
        if p["name"].lower() == profile.lower():  # Case insensitive match
            profile_match = p
            break

    if profile_match is None:
        messagebox.showerror("Error", "Invalid profile selected. Defaulting to 'zeel'.")
        profile_match = profiles[0]  # Default to first profile if invalid selection
    return profile_match


# Set up the dashboard using Tkinter
root = tk.Tk()
root.title("Driver Drowsiness Detection Dashboard")
root.geometry("600x400")  # Larger window size
root.resizable(False, False)  # Disable resizing

# Create labels for dashboard data
alert_label = tk.Label(root, text="ALERTS: 0", font=("Arial", 16), fg="red")
alert_label.pack(pady=20)

driver_info_label = tk.Label(root, text="Driver: Unknown", font=("Arial", 14))
driver_info_label.pack(pady=10)

ear_label = tk.Label(root, text="Average EAR: 0.00", font=("Arial", 14))
ear_label.pack(pady=10)

manual_alert_button = tk.Button(root, text="Trigger Manual Alert", font=("Arial", 14), command=lambda: send_alerts(driver_profile_data["preferred_alert"]))
manual_alert_button.pack(pady=10)

alert_history_label = tk.Label(root, text="Alert History: ", font=("Arial", 10))
alert_history_label.pack(pady=5)

alert_history_listbox = tk.Listbox(root, width=50, height=5)
alert_history_listbox.pack(pady=10)


# Update function to display data
def update_dashboard(alert_count, ear_value, driver_name="Unknown", alert_history=None):
    alert_label.config(text=f"ALERTS: {alert_count}")
    ear_label.config(text=f"Average EAR: {ear_value:.2f}")
    driver_info_label.config(text=f"Driver: {driver_name}")

    # Update alert history
    if alert_history:
        alert_history_listbox.delete(0, tk.END)
        for item in alert_history:
            alert_history_listbox.insert(tk.END, item)


# Load profiles from JSON
profiles = load_driver_profiles()

# Run the profile selection first
driver_profile_data = select_profile(profiles)

# Set the alert threshold based on the selected profile
thresh = driver_profile_data["ear_threshold"]

# Initialize alert history list
alert_history = []

# Loop to display video and update dashboard
alert_count = 0
while True:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    subjects = detect(gray, 0)

    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        if ear < thresh:
            flag += 1
            print(flag)
            if flag >= frame_check:
                cv2.putText(frame, "*ALERT!*", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "*ALERT!*", (10, 325),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                mixer.music.play()

                # Send all preferred alerts for the selected profile
                send_alerts(driver_profile_data["preferred_alert"])

                alert_count += 1
                alert_history.append(f"Alert {alert_count} triggered at EAR: {ear:.2f}")
                update_dashboard(alert_count, ear, driver_name=driver_profile_data["name"], alert_history=alert_history)
        else:
            flag = 0

    # Show video frame
    cv2.imshow("Frame", frame)

    # Update Tkinter dashboard window
    root.update()

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Cleanup
cv2.destroyAllWindows()
cap.release()
root.quit()