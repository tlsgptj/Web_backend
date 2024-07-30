from flask import Flask, render_template
from flask_socketio import SocketIO
import firebase_admin
from firebase_admin import credentials, db, auth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

cred = credentials.Certificate('path/to/your-firebase-adminsdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-name.firebaseio.com'
})


def listen_for_firebase_changes(path, event_name):
    ref = db.reference(path)

    def listener(event):
        if event.data:
            socketio.emit(event_name, event.data)
    ref.listen(listener)


listen_for_firebase_changes('/path/for/main', 'data_main')
listen_for_firebase_changes('/path/for/user_report', 'data_user_report')
listen_for_firebase_changes('/path/for/user', 'data_user')
listen_for_firebase_changes('/path/for/heart', 'data_heart')
listen_for_firebase_changes('/path/for/realtime', 'data_realtime')
listen_for_firebase_changes('/path/for/management', 'data_management')


@app.route("/")
def main():
    return render_template('admin_main.html')


@app.route("/user_report")
def user_report():
    return render_template('admin_report.html')


@app.route("/user")
def user():
    return render_template('admin_user.html')


@app.route("/heart")
def heart():
    return render_template('heart_rate.html')


@app.route("/realtime")
def realtime():
    return render_template('realtime_data.html')


@app.route("/management")
def management():
    return render_template('work_management.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/report")
def report():
    return render_template("report.html")


def listen_for_firebase_changes():
    ref = db.reference('/your/data/path')

    def listener(event):
        if event.data:
            socketio.emit('new_data', event.data)
    ref.listen(listener)


@app.route("/api/register", methods=['POST'])
def register_user():
    data = request.json
    email = data['email']
    password = data['password']
    gender = data['gender']
    

    try:
        user = auth.create_user(email=email, password=password)
        return jsonify({'status': 'success', 'uid': user.uid}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route("/api/login", methods=['POST'])
def login_user():
    data = request.json
    id_token = data.get('idToken')

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return jsonify({'status': 'success', 'uid': uid}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
