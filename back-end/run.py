from flask import Flask, render_template
from app.database import Base, engine
from app.models import User
from app.users import users_bp
from app.chat import chat_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "une_Secret_Key_Très_Longue_et_Sécurisée"
    app.register_blueprint(users_bp)
    app.register_blueprint(chat_bp)
    return app

app = create_app()

# Route pour servir la page d'accueil
@app.route("/")
def home():
    return render_template("index.html")  # Flask cherche automatiquement dans templates/

# Création des tables dans PostgreSQL
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app.run(debug=True)

