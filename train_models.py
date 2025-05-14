import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

def train_models(dataset_path, save_dir="models"):
    """
    Train phishing detection models using SVM, Random Forest, and Decision Tree.

    Args:
        dataset_path (str): Path to the CSV dataset file. The dataset must contain 'text' and 'label' columns.
        save_dir (str): Directory to save the trained models and vectorizer.

    Returns:
        dict: A dictionary containing training accuracy and paths to the saved models and vectorizer.
    """
    try:
        # Ensure the save directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Load the dataset
        print(f"Loading dataset from {dataset_path}...")
        data = pd.read_csv(dataset_path)

        # Ensure the dataset has the required columns
        if 'text' not in data.columns or 'label' not in data.columns:
            raise ValueError("Dataset must contain 'text' and 'label' columns.")

        # Split the dataset into training and testing sets
        print("Splitting dataset into training and testing sets...")
        X_train, X_test, y_train, y_test = train_test_split(
            data['text'], data['label'], test_size=0.2, random_state=42
        )

        # Vectorize the text data
        print("Vectorizing text data...")
        vectorizer = TfidfVectorizer(max_features=5000)
        X_train_vec = vectorizer.fit_transform(X_train)
        X_test_vec = vectorizer.transform(X_test)

        # Save the vectorizer
        vectorizer_path = os.path.join(save_dir, "vectorizer.pkl")
        with open(vectorizer_path, 'wb') as vec_file:
            pickle.dump(vectorizer, vec_file)
        print(f"Vectorizer saved to {vectorizer_path}")

        # Initialize classifiers
        classifiers = {
            "SVM": SVC(probability=True, random_state=42),
            "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
            "Decision Tree": DecisionTreeClassifier(random_state=42)
        }

        results = {}

        # Train and evaluate each classifier
        for name, clf in classifiers.items():
            print(f"\nTraining {name} model...")
            clf.fit(X_train_vec, y_train)

            # Save the model
            model_path = os.path.join(save_dir, f"{name.replace(' ', '_').lower()}_model.pkl")
            with open(model_path, 'wb') as model_file:
                pickle.dump(clf, model_file)
            print(f"{name} model saved to {model_path}")

            # Evaluate the model
            print(f"Evaluating {name} model...")
            y_pred = clf.predict(X_test_vec)
            accuracy = accuracy_score(y_test, y_pred)
            print(f"{name} Accuracy: {accuracy * 100:.2f}%")
            print(classification_report(y_test, y_pred))

            # Store the results
            results[name] = {
                "accuracy": accuracy * 100,
                "model_path": model_path
            }

        return results

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python train_models.py <dataset_path>")
    else:
        dataset_path = sys.argv[1]
        results = train_models(dataset_path)
        print("\nTraining Results:")
        for model_name, metrics in results.items():
            print(f"{model_name}: {metrics}")