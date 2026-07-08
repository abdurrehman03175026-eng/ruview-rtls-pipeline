import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

class AblationModelTestbed:
    def __init__(self, n_neighbors=3):
        self.n_neighbors = n_neighbors

    def evaluate_feature_subset(self, X_train, y_train, X_test, y_test, column_indices):
        """
        Isolates specific statistical features and returns classification performance metrics.
        """
        # Filter the dataset matrices to only include the requested columns
        X_tr_sub = X_train[:, column_indices]
        X_te_sub = X_test[:, column_indices]
        
        # Train the K-Nearest Neighbors Classifier
        clf = KNeighborsClassifier(n_neighbors=self.n_neighbors)
        clf.fit(X_tr_sub, y_train)
        
        # Predict the scene locations (Desk vs. Doorway)
        predictions = clf.predict(X_te_sub)
        
        # Compute official performance metrics
        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, average='macro'),
            "recall": recall_score(y_test, predictions, average='macro')
        }
        return metrics