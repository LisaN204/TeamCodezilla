from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import SessionLocal
from app.models import User
import json

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "email et mot de passe requis"}), 400

    hashed_password = generate_password_hash(password)

    session_db = SessionLocal()

    existing_user = session_db.query(User).filter_by(email=email).first()
    if existing_user:
        session_db.close()
        return jsonify({"msg": "email déjà utilisé"}), 400

    new_user = User(email=email, password=hashed_password, chat_history="[]")
    session_db.add(new_user)
    session_db.commit()
    session_db.close()

    return jsonify({"msg": "Utilisateur enregistré avec succès !"}), 201


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "email et mot de passe requis"}), 400

    session_db = SessionLocal()

    user = session_db.query(User).filter_by(email=email).first()
    session_db.close()

    if not user:
        return jsonify({"msg": "Utilisateur non trouvé"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"msg": "Mot de passe incorrect"}), 401

    # 🔥 Stocker automatiquement l'utilisateur connecté
    session["user_id"] = user.id

    return jsonify({
        "msg": "Connexion réussie !"
    }), 200

