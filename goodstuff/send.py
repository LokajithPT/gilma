import os
import requests

SERVER_URL = "http://127.0.0.1:5000/upload"

def send():
    current_folder = os.path.basename(os.getcwd())  # Get current folder name
    files_to_send = []

    for root, _, files in os.walk(os.getcwd()):
        # Skip the `venv` directory
        if "venv" in root.split(os.sep):  
            continue  

        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, os.getcwd())  # Preserve structure
            files_to_send.append(("files", (relative_path, open(file_path, "rb"))))

    data = {"folder_name": current_folder}
    response = requests.post(SERVER_URL, files=files_to_send, data=data)

    print(response.text)

