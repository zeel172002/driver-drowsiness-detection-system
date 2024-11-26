import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import json
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # This generates a 24-byte random key

# Helper function to load driver profiles from the JSON file
def load_driver_profiles_from_json():
    try:
        with open('driver_profiles.json', 'r') as file:
            data = json.load(file)
            return data.get('profiles', [])
    except FileNotFoundError:
        print("The file 'driver_profiles.json' was not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from the file.")
        return []

def get_user_by_id(user_id):
    # Example of fetching user from a list of profiles (can be adapted to your data storage method)
    for profile in profiles:
        if profile['id'] == user_id:
            return profile
    return None

# Helper function to save updated driver profiles back to the JSON file
def save_driver_profiles_to_json(profiles):
    with open('driver_profiles.json', 'w') as file:
        json.dump({"profiles": profiles}, file, indent=4)

# Route to load and display profiles (Home Page)
@app.route('/')
def home():
    profiles = load_driver_profiles_from_json()  # Get all profiles from the JSON file
    print(profiles)  # Add this line to check if profiles are being loaded
    return render_template('index.html', profiles=profiles)

# Route to add a new user profile
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        age = int(request.form['age'])
        contact_number = request.form['contact_number']
        email_id = request.form['email_id']
        preferred_alert = request.form['preferred_alert']
        ear_threshold = float(request.form['ear_threshold'])

        # Load existing profiles
        profiles = load_driver_profiles_from_json()

        # Check if the user already exists
        existing_user = next((p for p in profiles if p['name'] == name), None)
        if existing_user:
            flash('User already exists!', 'danger')
            return redirect(url_for('add_user'))

        # Create a new user profile
        new_user = {
            "name": name,
            "age": age,
            "contact_number": contact_number,
            "email_id": email_id,
            "preferred_alert": preferred_alert,
            "ear_threshold": ear_threshold,
            "alert_status": "Active",  # Add default values if needed
            "last_detected": str(datetime.utcnow())
        }

        # Add the new user profile to the list and save to JSON
        profiles.append(new_user)
        save_driver_profiles_to_json(profiles)

        flash('User added successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('add_user.html')

@app.route('/dashboard/<string:name>', methods=['GET', 'POST'])
def select_driver(name):
    profiles = load_driver_profiles_from_json()
    user = next((p for p in profiles if p['name'] == name), None)

    if user is None:
        flash('User not found!', 'danger')
        return redirect(url_for('home'))

    return render_template('dashboard.html', user=user)


# Route to edit an existing user profile
@app.route('/edit_user/<string:name>', methods=['GET', 'POST'])
def edit_user(name):
    profiles = load_driver_profiles_from_json()
    user = next((p for p in profiles if p['name'] == name), None)

    if user is None:
        flash('User not found!', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Update the user profile fields
        user['name'] = request.form['name']
        user['age'] = int(request.form['age'])
        user['contact_number'] = request.form['contact_number']
        user['email_id'] = request.form['email_id']
        user['preferred_alert'] = request.form['preferred_alert']
        user['ear_threshold'] = float(request.form['ear_threshold'])

        # Save the updated profiles back to the JSON file
        save_driver_profiles_to_json(profiles)

        flash('User updated successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_user.html', user=user)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        user_id = request.form.get('user_id')  # Get user_id from the form

        # Load profiles from the JSON file
        with open('driver_profiles.json', 'r') as file:
            data = json.load(file)

        profiles = data.get("profiles", [])  # Safely access the "profiles" list

        # Convert user_id to an integer if it's provided as a numeric string
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return "Invalid user ID format", 400

        # Ensure user_id corresponds to the list index of profiles
        if 0 <= user_id < len(profiles):
            user = profiles[user_id]  # Get the user by index
        else:
            return "User not found", 404

        # Render the dashboard template with the selected user's data
        return render_template('dashboard.html', user=user)

    return "Invalid method", 405


# Route to delete a user profile

@app.route('/delete_user/<string:name>', methods=['POST'])
def delete_user(name):
    profiles = load_driver_profiles_from_json()
    user = next((p for p in profiles if p['name'] == name), None)

    if user is None:
        flash('User not found!', 'danger')
        return redirect(url_for('home'))

    # Remove the user profile and save the updated profiles back to JSON
    profiles = [p for p in profiles if p['name'] != name]
    save_driver_profiles_to_json(profiles)

    flash('User deleted successfully!', 'success')
    return redirect(url_for('home'))

# Initialize the app
if __name__ == '__main__':
    app.run(debug=True)
