import requests
import os
import json

SERVER_URL = "http://100.104.132.24:5000"

def list_files():
    response = requests.get(f"{SERVER_URL}/list-files")
    if response.status_code == 200:
        files = response.json().get("files", [])
        if files:
            print("Files in the uploads directory:")
            for file in files:
                print(file)
        else:
            print("No files found.")
    else:
        print("Error:", response.json().get("error"))

def delete_file(filename):
    data = {"filename": filename}
    response = requests.post(f"{SERVER_URL}/delete-file", json=data)
    if response.status_code == 200:
        print(f"Deleted {filename} successfully.")
    else:
        print("Error:", response.json().get("error"))

def upload_files(folder_name, file_paths):
    files = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            files.append(("files", open(file_path, "rb")))
        else:
            print(f"File not found: {file_path}")
            return

    data = {"folder_name": folder_name}
    response = requests.post(f"{SERVER_URL}/upload", files=files, data=data)
    if response.status_code == 200:
        print("Upload successful.")
    else:
        print("Error:", response.text)

def list_uploads():
    response = requests.get(f"{SERVER_URL}/list_uploads")
    if response.status_code == 200:
        uploads = response.json()
        if uploads:
            print("Available uploads:")
            for upload in uploads:
                print(upload)
        else:
            print("No uploads found.")
    else:
        print("Error:", response.json().get("error"))

def list_files_in_folder(folder_name):
    response = requests.get(f"{SERVER_URL}/download/{folder_name}")
    if response.status_code == 200:
        files = response.json()
        if files:
            print(f"Files in {folder_name}:")
            for file in files:
                print(file)
        else:
            print("No files found in the folder.")
    else:
        print("Error:", response.text)

def download_file(folder_name, file_path):
    response = requests.get(f"{SERVER_URL}/file/{folder_name}/{file_path}")
    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {file_path} successfully.")
    else:
        print("Error:", response.text)

def main():
    while True:
        print("\nOptions:")
        print("1. List files in the uploads directory")
        print("2. Delete a file")
        print("3. Upload files")
        print("4. List available uploads")
        print("5. List files in a specific upload folder")
        print("6. Download a file")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            list_files()
        elif choice == "2":
            filename = input("Enter the filename to delete: ")
            delete_file(filename)
        elif choice == "3":
            folder_name = input("Enter the folder name: ")
            file_paths = input("Enter the file paths (comma-separated): ").split(",")
            upload_files(folder_name, file_paths)
        elif choice == "4":
            list_uploads()
        elif choice == "5":
            folder_name = input("Enter the folder name: ")
            list_files_in_folder(folder_name)
        elif choice == "6":
            folder_name = input("Enter the folder name: ")
            file_path = input("Enter the file path: ")
            download_file(folder_name, file_path)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()