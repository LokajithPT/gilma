import requests

SERVER_URL = "http://100.104.132.24"

def list_files():
    """Fetch and display files from the server."""
    response = requests.get(f"{SERVER_URL}/list-files")
    
    if response.status_code != 200:
        print("Error fetching file list:", response.json().get("error"))
        return None

    data = response.json()
    files = data.get("files", [])
    
    if not files:
        print("No files found on the server.")
        return None

    print("\nAvailable Files:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file}")

    return files

def d():
    """List files, ask user for input, and send delete request."""
    files = list_files()
    if not files:
        return

    try:
        choice = int(input("\nEnter the number of the file to delete: ")) - 1
        if 0 <= choice < len(files):
            filename = files[choice]
            response = requests.post(f"{SERVER_URL}/delete-file", json={"filename": filename})

            if response.status_code == 200:
                print(response.json().get("message"))
            else:
                print("Error:", response.json().get("error"))
        else:
            print("Invalid choice!")
    except ValueError:
        print("Enter a valid number!")


