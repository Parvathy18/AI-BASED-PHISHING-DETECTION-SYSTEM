from flask import Flask, request, jsonify
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import traceback

app = Flask(__name__)

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Load model and vectorizer
def load_model_and_vectorizer():
    try:
        model_path = os.path.join(MODEL_DIR, "svm_model.pkl")
        vectorizer_path = os.path.join(MODEL_DIR, "vectorizer.pkl")

        if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
            raise FileNotFoundError("Model or vectorizer not found. Train the model first.")

        with open(model_path, "rb") as model_file:
            model = pickle.load(model_file)

        with open(vectorizer_path, "rb") as vec_file:
            vectorizer = pickle.load(vec_file)

        return model, vectorizer
    except Exception as e:
        print(f"Error loading model or vectorizer: {e}")
        traceback.print_exc()
        return None, None

model, vectorizer = load_model_and_vectorizer()

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict whether the input text is phishing or legitimate.
    """
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request."}), 400

        # Get the text input
        input_text = data['text']

        # Transform the text using the vectorizer
        input_vector = vectorizer.transform([input_text])

        # Predict using the trained model
        prediction = model.predict(input_vector)[0]
        confidence = model.predict_proba(input_vector).max() * 100

        return jsonify({
            "prediction": "Phishing" if prediction == 1 else "Legitimate",
            "confidence": round(confidence, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


if __name__ == '__main__':
    app.run(debug=True)