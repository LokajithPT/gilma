from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this for security
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

if __name__ == '__main__':
    app.run(debug=True)
