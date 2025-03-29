from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.secret_key = "nigganigga"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
######################################
        #gui code
######################################


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'loki' and password == 'lokihehe':
            session['user'] = username
            return redirect(url_for('dashboard', path=''))
        return "Invalid credentials! Try again."
    return render_template('login.html')

@app.route('/dashboard/', defaults={'path': ''})
@app.route('/dashboard/<path:path>')
def dashboard(path):
    if 'user' not in session:
        return redirect(url_for('login'))
    full_path = os.path.join(UPLOAD_FOLDER, path)
    if not os.path.exists(full_path):
        return "Directory not found", 404
    
    if os.path.isfile(full_path):
        return view_file(full_path, path)
    
    items = [{'name': f, 'is_dir': os.path.isdir(os.path.join(full_path, f)), 'path': os.path.join(path, f)} for f in os.listdir(full_path)]
    return render_template('dashboard.html', files=items, current_path=path)

@app.route('/download/<path:path>')
def download_file(path):
    full_path = os.path.join(UPLOAD_FOLDER, path)
    if os.path.exists(full_path):
        return send_from_directory(UPLOAD_FOLDER, path, as_attachment=True)
    return "File not found", 404

@app.route('/view/<path:path>')
def view_file(path, current_path=None):
    full_path = os.path.join(UPLOAD_FOLDER, path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        with open(full_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        return render_template('view_file.html', filename=os.path.basename(path), content=content, current_path=current_path)
    return "File not found", 404

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

 

@app.route("/list-files", methods=["GET"])
def list_files():
    """Lists all files in the uploads directory."""
    if not os.path.exists(UPLOAD_FOLDER):
        return jsonify({"error": "Uploads folder not found"}), 404

    files = os.listdir(UPLOAD_FOLDER)
    if not files:
        return jsonify({"message": "No files found"}), 200

    return jsonify({"files": files})

@app.route("/delete-file", methods=["POST"])
def delete_file():
    """Deletes a file from the uploads directory."""
    data = request.json
    filename = data.get("filename")

    if not filename:
        return jsonify({"error": "Filename not provided"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    shutil.rmtree(file_path)
    return jsonify({"message": f"Deleted {filename} successfully"})



# Upload endpoint
@app.route("/upload", methods=["POST"])
def upload():
    if "folder_name" not in request.form:
        return "Missing folder name", 400

    folder_name = request.form["folder_name"]
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)

    # Remove old files
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    os.makedirs(folder_path)

    for file_key in request.files.getlist("files"):
        file_path = os.path.join(folder_path, file_key.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file_key.save(file_path)

    return "Upload successful", 200

# List available uploads
@app.route("/list_uploads", methods=["GET"])
def list_uploads():
    return jsonify(os.listdir(UPLOAD_FOLDER))

# List all files in a selected upload folder
@app.route("/download/<folder_name>", methods=["GET"])
def list(folder_name):
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)

    if not os.path.exists(folder_path):
        return "Folder not found", 404

    all_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), folder_path)
            all_files.append(file_path)

    return jsonify(all_files)

# Send individual files
@app.route("/file/<folder_name>/<path:file_path>", methods=["GET"])
def send_file_from_server(folder_name, file_path):
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name, file_path)
    
    if not os.path.exists(folder_path):
        return "File not found", 404

    return send_file(folder_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)

