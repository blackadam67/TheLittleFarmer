import os
import requests
from cryptography.fernet import Fernet
from PIL import Image
import base64
import json
import secrets

# Generate a Fernet key
key = Fernet.generate_key()
fernet = Fernet(key)

# Encrypt a message
def encrypt_message(message):
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

# Decrypt a message
def decrypt_message(encrypted_message):
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message

# Send an encrypted message to a GitHub repository
def send_message(repository, encrypted_message):
    url = f"https://api.github.com/repos/{repository}/contents/message.txt"
    data = {
        "message": encrypted_message.decode(),
        "committer": {
            "name": "Anonymous",
            "email": "anonymous@example.com"
        }
    }
    response = requests.put(url, json=data)
    return response.status_code == 201

# Receive an encrypted message from a GitHub repository
def receive_message(repository):
    url = f"https://api.github.com/repos/{repository}/contents/message.txt"
    response = requests.get(url)
    if response.status_code == 200:
        encrypted_message = response.json()["content"].encode()
        decrypted_message = decrypt_message(encrypted_message)
        return decrypted_message
    else:
        return None

# Send a photo to a GitHub repository
def send_photo(repository, photo_path):
    url = f"https://api.github.com/repos/{repository}/contents/photo.jpg"
    with open(photo_path, "rb") as photo_file:
        photo_data = photo_file.read()
    data = {
        "message": "Photo uploaded",
        "content": base64.b64encode(photo_data).decode(),
        "committer": {
            "name": "Anonymous",
            "email": "anonymous@example.com"
        }
    }
    response = requests.put(url, json=data)
    return response.status_code == 201

# Receive a photo from a GitHub repository
def receive_photo(repository):
    url = f"https://api.github.com/repos/{repository}/contents/photo.jpg"
    response = requests.get(url)
    if response.status_code == 200:
        photo_data = response.json()["content"].encode()
        photo_path = "received_photo.jpg"
        with open(photo_path, "wb") as photo_file:
            photo_file.write(base64.b64decode(photo_data))
        return photo_path
    else:
        return None

# Convert an image to black and white
def convert_to_bw(image_path):
    image = Image.open(image_path)
    bw_image = image.convert("L")
    bw_image.save("bw_" + image_path)
    return "bw_" + image_path

# Send a video to a GitHub repository
def send_video(repository, video_path):
    url = f"https://api.github.com/repos/{repository}/contents/video.mp4"
    with open(video_path, "rb") as video_file:
        video_data = video_file.read()
    data = {
        "message": "Video uploaded",
        "content": base64.b64encode(video_data).decode(),
        "committer": {
            "name": "Anonymous",
            "email": "anonymous@example.com"
        }
    }
    response = requests.put(url, json=data)
    return response.status_code == 201

# Receive a video from a GitHub repository
def receive_video(repository):
    url = f"https://api.github.com/repos/{repository}/contents/video.mp4"
    response = requests.get(url)
    if response.status_code == 200:
        video_data = response.json()["content"].encode()
        video_path = "received_video.mp4"
        with open(video_path, "wb") as video_file:
            video_file.write(base64.b64decode(video_data))
        return video_path
    else:
        return None

# User registration
def register_user(username, password):
    # Generate a unique ID for the user
    user_id = generate_user_id()
    # Store the user information securely
    store_user_info(username, password, user_id)
    return user_id

# User authentication
def authenticate_user(username, password):
    # Retrieve the user information
    stored_username, stored_password, user_id = retrieve_user_info(username)
    if stored_username == username and stored_password == password:
        return user_id
    else:
        return None

# Password reset
def reset_password(username, new_password):
    # Retrieve the user information
    stored_username, stored_password, user_id = retrieve_user_info(username)
    # Update the password
    store_user_info(username, new_password, user_id)

# Helper functions
def generate_user_id():
    # Generate a unique ID for the user
    return secrets.token_hex(16)

def store_user_info(username, password, user_id):
    # Store the user information securely
    user_info = {
        "username": username,
        "password": password,
        "user_id": user_id
    }
    with open("users.json", "a") as users_file:
        json.dump(user_info, users_file)
        users_file.write("\n")

def retrieve_user_info(username):
    # Retrieve the user information
    with open("users.json", "r") as users_file:
        for line in users_file:
            user_info = json.loads(line.strip())
            if user_info["username"] == username:
                return user_info["username"], user_info["password"], user_info["user_id"]
    return None, None, None

# Example usage
repository = "blackadam67/TheLittleFarmer"
message = "Hello, this is an anonymous message!"
encrypted_message = encrypt_message(message)
send_message(repository, encrypted_message)

received_message = receive_message(repository)
decrypted_message = decrypt_message(received_message.encode())
print(decrypted_message)

photo_path = "photo.jpg"
send_photo(repository, photo_path)

received_photo_path = receive_photo(repository)
bw_photo_path = convert_to_bw(received_photo_path)

video_path = "video.mp4"
send_video(repository, video_path)

received_video_path = receive_video(repository)

username = "anonymous"
password = "password"
user_id = register_user(username, password)

authenticated_user_id = authenticate_user(username, password)
print(authenticated_user_id)

reset_password(username, "new_password")
