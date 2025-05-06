# 1. Import Libraries
import numpy as np
import pandas as pd
import os
import pickle
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import datetime
import matplotlib.pyplot as plt

# 2. Constants
DATA_FILE = 'dataset.csv'  # Path inside Colab after clone
MODEL_DIR = 'models/'      # Models will be saved here
MODEL_FILE = os.path.join(MODEL_DIR, 'model.pkl') 
CLASSES = np.array([0,1])           # Risk classes: Safe (0), Risky (1)

# 3. Ensure model folder exists
os.makedirs(MODEL_DIR, exist_ok=True)

# 4. Functions
def load_dataset(file_path):
    """Load dataset from CSV."""
    data = pd.read_csv(file_path)
    X = data[['loc', 'complexity']].values  # feature columns
    y = data['risk'].values                 # label column
    return X, y

def initialize_or_load_model():
    """Load model from disk if exists, else initialize new."""
    if os.path.exists(MODEL_FILE):
        print("Loading existing model...")
        with open(MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
    else:
        print("Creating new model...")
        model = SGDClassifier(loss='log_loss')  # behaves like Logistic Regression
    return model

def save_model(model):
    """Save model to disk."""
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
    print("Model saved successfully.")

def train_incrementally(model, X_train, y_train):
    """Train model on new data."""
    model.partial_fit(X_train, y_train, classes=CLASSES)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model and print accuracy."""
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f" Model Accuracy: {acc*100:.2f}%")
    return acc, y_pred

def timestamped_model_save(model):
    """Optional: Save model versioned with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    versioned_file = f"model_{timestamp}.pkl"
    with open(versioned_file, 'wb') as f:
        pickle.dump(model, f)
    print(f" Model also saved as {versioned_file} for version control.")

def visualize_comparison(X, y_true, y_pred, save_path="comparison_plot.png"):
    """Compare true labels vs model predictions using scatter plots, and save as image."""
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Ground Truth (actual labels)
    axes[0].scatter(X[y_true==0][:, 0], X[y_true==0][:, 1], c='green', label='Safe', alpha=0.7, edgecolors='k')
    axes[0].scatter(X[y_true==1][:, 0], X[y_true==1][:, 1], c='red', label='Risky', alpha=0.7, edgecolors='k')
    axes[0].set_title('Ground Truth: Program Risk')
    axes[0].set_xlabel('Lines of Code (LOC)')
    axes[0].set_ylabel('Cyclomatic Complexity')
    axes[0].legend()
    axes[0].grid(True)
    
    # Plot 2: Model Predictions
    axes[1].scatter(X[y_pred==0][:, 0], X[y_pred==0][:, 1], c='green', label='Predicted Safe', alpha=0.7, edgecolors='k')
    axes[1].scatter(X[y_pred==1][:, 0], X[y_pred==1][:, 1], c='red', label='Predicted Risky', alpha=0.7, edgecolors='k')
    axes[1].set_title('Model Predictions: Program Risk')
    axes[1].set_xlabel('Lines of Code (LOC)')
    axes[1].set_ylabel('Cyclomatic Complexity')
    axes[1].legend()
    axes[1].grid(True)
    
    plt.suptitle('Comparison: Ground Truth vs Model Predictions', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Save the figure
    plt.savefig(save_path)
    plt.close()  # Close plot to avoid memory issues

# 5. Main Agent Flow
# Step 1: Load dataset
X, y = load_dataset(DATA_FILE)
print(f" Loaded dataset: {X.shape[0]} samples.")
print("Labels distribution:", np.bincount(y))

# Step 2: Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print("Train labels distribution:", np.bincount(y_train))
print("Test labels distribution:", np.bincount(y_test))

# Step 3: Initialize or Load model
model = initialize_or_load_model()

# Step 4: Incremental training
model = train_incrementally(model, X_train, y_train)

# Step 5: Evaluate
acc, y_pred = evaluate_model(model, X_test, y_test)

# Step 6: Save updated model
save_model(model)

# Step 7: Visualize the truth vs prediction comparison
visualize_comparison(X_test, y_test, y_pred)

# Optional: Save timestamped version
timestamped_model_save(model)
