import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# Load CSV file
df = pd.read_csv('Dataset.csv')

# Specify feature columns and label column
feature_columns = ['runq-sz', 'plist-sz', 'ldavg-1', 'ldavg-5', 'ldavg-15']  # Replace with actual column names
label_column = 'Label'  

# Prepare feature matrix (X) and target vector (y)
X = df[feature_columns]
y = df[label_column]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train SVM classifier
clf = SVC(kernel='linear', C=1.0)  # Change kernel if needed
clf.fit(X_train, y_train)

# Save the trained model
joblib.dump(clf, 'svm_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:\n', classification_report(y_test, y_pred))

