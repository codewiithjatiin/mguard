from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this for production security

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Hardcoded login credentials
USERNAME = "mguard24scse"
PASSWORD = "jatiin135"
VIRUSTOTAL_API_KEY = "7b4d5ed055159706c8fbbba152a1825250c14ada32753fcd1e969065d40d4015"

# Store scan history
db_history = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid Credentials", "error")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if 'username' not in session:
        return redirect(url_for('login'))

    result = None
    filename = None

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # --- VirusTotal API Call ---
            with open(filepath, 'rb') as f:
                files = {'file': (filename, f)}
                headers = {"x-apikey": VT_API_KEY}
                response = requests.post("https://www.virustotal.com/api/v3/files", files=files, headers=headers)

            if response.status_code == 200:
                analysis_id = response.json()['data']['id']
                analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
                analysis_response = requests.get(analysis_url, headers=headers)

                if analysis_response.status_code == 200:
                    analysis_data = analysis_response.json()
                    stats = analysis_data['data']['attributes']['stats']
                    malicious = stats['malicious']

                    # --- Result Logic ---
                    if malicious > 0:
                        result = "Malware Found!"
                    else:
                        result = "No Malware Found."

                    # --- Save to History DB ---
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    conn = sqlite3.connect(DATABASE)
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO history (filename, result, timestamp) VALUES (?, ?, ?)",
                                   (filename, result, timestamp))
                    conn.commit()
                    conn.close()
                else:
                    result = "Error fetching analysis results."
            else:
                result = "Error uploading file to VirusTotal."

    return render_template("scan.html", result=result, filename=filename)

@app.route('/history')
def history():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('history.html', history=db_history)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
