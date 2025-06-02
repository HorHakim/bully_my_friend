import streamlit as st
from dotenv import load_dotenv
import base64
import os
from mistralai import Mistral

# Chargement des variables d'environnement
load_dotenv()

# ========== Fonctions Backend ==========

def encode_image(image_path):
    """Encode une image en base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        st.error(f"Erreur lors de l'encodage de l'image : {e}")
        return None

def load_context():
    with open("context.txt", "r") as file:
        return file.read()

def load_prompt():
    with open("prompt.txt", "r") as file:
        return file.read()

def get_joke(image_path):
    base64_image = encode_image(image_path)
    if not base64_image:
        return "Erreur : impossible d'encoder l'image."

    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        return "Erreur : clé API Mistral manquante."

    client = Mistral(api_key=api_key)

    messages = [
        {"role": "system", "content": load_context()},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": load_prompt()},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
            ]
        }
    ]

    response = client.chat.complete(model="pixtral-12b-2409", messages=messages)
    return response.choices[0].message.content

# ========== Interface Streamlit ==========

st.set_page_config(page_title="RoastBot 🤖🔥", layout="centered")
st.title("RoastBot 🤖🔥")
st.markdown("**Upload une photo de ton pote et laisse l'IA le clasher gentiment !**")

uploaded_file = st.file_uploader("📸 Choisis une photo de ton pote :", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Afficher l'image
    st.image(uploaded_file, caption="Voici la victime 👀", use_column_width=True)

    # Sauvegarder temporairement le fichier
    temp_path = "temp_image.jpg"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    if st.button("🔥 Génère des blagues !"):
        with st.spinner("Génération des blagues en cours..."):
            joke = get_joke(temp_path)
            st.markdown("### 😂 Blagues générées :")
            st.write(joke)
