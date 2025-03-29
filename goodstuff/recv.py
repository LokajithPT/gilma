import os
import requests

SERVER_URL = "http://100.104.132.24"

def list_available_uploads():
    response = requests.get(f"{SERVER_URL}/list_uploads")
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching uploads.")
        return []

def download_files(folder_name, destination):
    response = requests.get(f"{SERVER_URL}/download/{folder_name}")
    
    if response.status_code != 200:
        print("Error downloading files.")
        return

    files_data = response.json()

    if destination:
        os.makedirs(destination, exist_ok=True)
    else:
        destination = os.getcwd()  # Replace current files

    # Clear the directory if replacing
    if not destination:
        for item in os.listdir(os.getcwd()):
            item_path = os.path.join(os.getcwd(), item)
            if os.path.isfile(item_path) or os.path.isdir(item_path):
                os.remove(item_path) if os.path.isfile(item_path) else shutil.rmtree(item_path)

    # Download each file
    for file_path in files_data:
        file_url = f"{SERVER_URL}/file/{folder_name}/{file_path}"
        file_response = requests.get(file_url)

        save_path = os.path.join(destination, file_path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(file_response.content)

    print(f"Download complete. Files saved to: {destination}")

def recv():
    uploads = list_available_uploads()
    
    if not uploads:
        print("No uploads found.")
        exit()

    print(colored("before any thing " , "magenta"))
    lol = input(colored(" give me ur pass:","magenta"))

    if (lol == "lowkeychillin"):
        print(colored("u got it ... " , "green"))

    else:
        print(colored("u gave me the wrong pass... " , "red"))
        exit()
    print("Available uploads:")
    for idx, name in enumerate(uploads):
        print(f"{idx + 1}. {name}")

    choice = int(input("Select a folder to download: ")) - 1
    if choice < 0 or choice >= len(uploads):
        print("Invalid choice.")
        exit()
    
    selected_folder = uploads[choice]
    destination = input("Enter folder name to save (leave empty to replace current directory): ").strip()

    download_files(selected_folder, destination if destination else None)


