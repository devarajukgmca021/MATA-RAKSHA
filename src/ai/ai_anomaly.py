# src/utils/ai/ai_anomaly.py
import numpy as np
from sklearn.ensemble import IsolationForest

class VoteAnomalyDetector:
    def __init__(self):
        # A pretrained model would be ideal, but this lightweight rule works.
        self.model = IsolationForest(contamination=0.10)

        # Fake historical voting behavior dataset
        # Each row = [time_of_day, vote_gap_seconds]
        normal_data = np.array([
            [9, 120], [10, 240], [11, 180],
            [12, 300], [13, 200], [14, 150],
            [15, 320], [16, 280]
        ])

        self.model.fit(normal_data)

    def check_vote(self, time_of_day, sec_since_last_vote):
        """
        Returns:
        - "Normal"
        - "Suspicious"
        """
        X = np.array([[time_of_day, sec_since_last_vote]])
        result = self.model.predict(X)[0]

        return "Normal" if result == 1 else "Suspicious"
