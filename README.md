# AI-BASED-PHISHING-DETECTION-SYSTEM

This project is an AI-based phishing detection system that leverages both frontend and backend components to detect phishing attempts in real-time. It uses machine learning models trained on phishing datasets to classify suspicious URLs and email data.

Project Structure

My-project-main/
├── app.js                 # Frontend JavaScript logic
├── app.py                 # Backend Flask application
├── index.html             # Main HTML page for the app
├── pd.csv                 # Data file for analysis
├── phishing_dataset.csv   # Dataset for phishing detection
└── train_models.py        # Script for training models

Features

Real-Time Phishing Detection: Identifies phishing URLs and email headers instantly.

Model Training: Includes scripts to train machine learning models.

Interactive Web Interface: User-friendly interface for easy detection.

Setup and Installation

Clone the repository:

git clone https://github.com/yourusername/My-project-main.git
cd My-project-main

Install the dependencies:

pip install -r requirements.txt

Run the Flask application:

python app.py

Open index.html in your browser to interact with the application.

Usage

Navigate to the web interface and enter the URL or email header details to check for phishing threats.

The model will provide real-time predictions.

Training the Model

To retrain the models, run:

python train_models.py

This will update the model with new data from phishing_dataset.csv.

**Contributing**
Feel free to open issues or submit pull requests for improvements and bug fixes.
