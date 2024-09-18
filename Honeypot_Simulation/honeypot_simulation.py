import socket
import joblib
import numpy as np
import time
from utils.feature_extraction import gather_features
from utils.interaction_mode_switch import switch_to_high_interaction

# Load the pre-trained XGBoost model
model = joblib.load('../Attack_Classification/final_xgboost_model.pkl')

def low_interaction_honeypot():
    print("Starting low-interaction honeypot...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 22))  # Example: SSH on port 22
    s.listen(1)
    
    while True:
        conn, addr = s.accept()
        print(f"Connection from {addr}")
        
        # Log the connection details
        with open('logs/honeypot_log.txt', 'a') as f:
            f.write(f"Low-interaction connection from {addr}\n")
        
        # Extract features from the interaction
        features = np.array(gather_features(conn))
        print(type(features), features.shape)  # Check type and shape of the features
        
        # Reshape the features to match the expected input of the model (1 sample, 41 features)
        features = features.reshape(1, -1)  # Reshape to (1, 41)
        
        # Classify the activity (0: normal, 1: suspicious)
        result = model.predict(features)
        
        if result == 1:  # Suspicious activity detected
            print(f"Suspicious activity detected from {addr}. Escalating...")
            switch_to_high_interaction(conn)
        else:
            print(f"Normal activity from {addr}.")
            conn.close()

if __name__ == "__main__":
    low_interaction_honeypot()
