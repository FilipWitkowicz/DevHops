from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Importujemy CORS
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Pobiera ścieżkę katalogu projektu
DB_PATH = os.path.join(BASE_DIR, 'database.db')  # Tworzy pełną ścieżkę do pliku bazy danych
DIST_DIR = os.path.join(BASE_DIR, 'frontend', 'dist')  # Nowa ścieżka do plików statycznych Reacta


app = Flask(__name__, static_folder=DIST_DIR, static_url_path='')
CORS(app)  # Dodajemy obsługę CORS dla całej aplikacji

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'  # Lokalna baza danych w projekcie
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Przykładowa tabela (model)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Serwowanie plików Reacta
@app.route('/')
def serve_react():
    return send_from_directory(DIST_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(DIST_DIR, path)

# API do dodawania użytkownika
@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.get_json()  # Pobiera dane JSON z żądania
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400

    # Tworzymy nowego użytkownika
    new_user = User(username=username, email=email)

    try:
        db.session.add(new_user)
        db.session.commit()  # Zapisuje użytkownika do bazy
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        db.session.rollback()  # W razie błędu cofa transakcję
        return jsonify({"error": str(e)}), 500

# API do pobierania listy wszystkich użytkowników
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()  # Pobiera wszystkich użytkowników z bazy danych
    users_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    
    return jsonify(users_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tworzy bazę danych w folderze projektu, jeśli nie istnieje
    app.run(host='0.0.0.0', port=31628)
