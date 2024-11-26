from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Initialize the database
db = SQLAlchemy()

# Define the User table
class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}  # Ensure that the table is extended if already defined

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    preferred_alert = db.Column(db.String(100), nullable=False)
    ear_threshold = db.Column(db.Float, nullable=False)
    blink_count = db.Column(db.Integer, default=0)
    drowsy_count = db.Column(db.Integer, default=0)
    ear_changes = db.Column(db.Integer, default=0)
    days_active = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

# Helper function to load driver profiles from JSON file
def load_driver_profiles():
    try:
        with open("driver_profiles.json", "r") as f:
            profiles = json.load(f)
        return profiles["profiles"]
    except FileNotFoundError:
        print("driver_profiles.json file not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from driver_profiles.json.")
        return []

# Function to load driver profiles into the database
def load_driver_profiles_to_db():
    profiles = load_driver_profiles()  # Ensure this is defined
    for profile in profiles:
        existing_user = User.query.filter_by(name=profile["name"]).first()
        if existing_user:
            print(f"Profile for {profile['name']} already exists in the database.")
        else:
            new_user = User(
                name=profile["name"],
                age=profile["age"],
                experience=profile["experience"],
                preferred_alert=profile["preferred_alert"],
                ear_threshold=profile["ear_threshold"]
            )
            db.session.add(new_user)
            db.session.commit()
            print(f"Added profile for {profile['name']}")


# Function to create a new user (optional, for manual user creation)
def create_user(name, age, experience, preferred_alert, ear_threshold):
    new_user = User(
        name=name,
        age=age,
        experience=experience,
        preferred_alert=preferred_alert,
        ear_threshold=ear_threshold
    )
    db.session.add(new_user)
    db.session.commit()
    print(f"Created new user: {name}")

# Function to update user statistics (optional)
def update_user_stats(user_name, blink_count, drowsy_alert, ear_change):
    user = User.query.filter_by(name=user_name).first()
    if user:
        user.blink_count = blink_count
        user.drowsy_count += 1 if drowsy_alert else 0
        user.ear_changes = ear_change
        user.days_active += 1
        user.last_updated = datetime.utcnow()
        db.session.commit()
        print(f"Updated statistics for {user_name}")
    else:
        print(f"User {user_name} not found")

# Function to get user statistics (optional)
def get_user_stats(user_name):
    user = User.query.filter_by(name=user_name).first()
    if user:
        stats = {
            "name": user.name,
            "blink_count": user.blink_count,
            "drowsy_count": user.drowsy_count,
            "ear_changes": user.ear_changes,
            "days_active": user.days_active,
            "last_updated": user.last_updated
        }
        return stats
    else:
        return {"error": f"User {user_name} not found"}
