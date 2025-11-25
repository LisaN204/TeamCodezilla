import openai
import os
import json
from flask import Blueprint, request, jsonify, session
from dotenv import load_dotenv
from app.database import SessionLocal
from app.models import User

# Charger variables d'environnement
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/", methods=["POST"])
def chat():

    # 1️⃣ Vérifier que l’utilisateur est connecté
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"msg": "Vous devez être connecté pour discuter avec l'IA"}), 401

    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"msg": "Message requis"}), 400

    # 2️⃣ Charger l’historique de cet utilisateur
    db = SessionLocal()
    user = db.query(User).filter_by(id=user_id).first()

    # Convertir JSON → Python
    history = json.loads(user.chat_history)

    # 3️⃣ Ajouter le message utilisateur
    history.append({"role": "user", "content": user_message})

    try:
        # 4️⃣ Envoyer tout l'historique au modèle OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=history,
            max_tokens=200
        )

        ai_message = response.choices[0].message.content

        # 5️⃣ Ajouter réponse IA
        history.append({"role": "assistant", "content": ai_message})

        # 6️⃣ Sauvegarder l’historique mis à jour en base
        user.chat_history = json.dumps(history)
        db.commit()
        db.close()

        return jsonify({"response": ai_message}), 200

    except Exception as e:
        return jsonify({"msg": "Erreur lors de l'appel à l'IA", "error": str(e)}), 500
