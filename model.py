import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from tqdm import tqdm

# Pandas terminal settings
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)

# Load your dataset
# data = pd.read_json('raw_data/squad_data/Regular Season - Overall.json')

# Explore your data
# print(data)

# Load your data into a pandas DataFrame
data = {
    'Rk': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    'Squad': ['Liverpool', 'Arsenal', 'Aston Villa', 'Manchester City', 'Tottenham', 'Manchester Utd', 'Newcastle Utd', 'Brighton', 'West Ham', 'Fulham', 'Brentford', 'Chelsea', 'Wolves', 'Bournemouth', 'Crystal Palace', 'Nott\'ham Forest', 'Everton', 'Luton Town', 'Burnley', 'Sheffield Utd'],
    'W': [11, 11, 11, 10, 9, 9, 8, 7, 7, 6, 5, 5, 5, 5, 4, 3, 7, 2, 2, 2],
    'D': [4, 3, 2, 3, 3, 0, 2, 5, 3, 3, 4, 4, 4, 4, 4, 5, 2, 3, 2, 2],
    'L': [1, 2, 3, 3, 4, 7, 6, 4, 6, 7, 7, 7, 7, 7, 8, 8, 7, 11, 12, 12],
    'GF': [36, 33, 35, 38, 33, 18, 33, 33, 26, 26, 23, 26, 21, 21, 15, 17, 20, 17, 16, 12],
    'GA': [15, 15, 20, 18, 23, 21, 21, 28, 30, 26, 22, 26, 26, 30, 23, 28, 20, 32, 34, 41],
}

df = pd.DataFrame(data)

# Feature selection
features = ['W', 'D', 'L', 'GF', 'GA']
X = df[features]
y = df['W']  # You can replace 'W' with another target variable if needed

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a logistic regression model with increased max_iter
model = LogisticRegression(max_iter=10000000000000)  # You can adjust the value as needed

# Train the model with progress bar
with tqdm(total=100, desc="Training Model") as pbar:
    model.fit(X_train, y_train)
    pbar.update(50)

    # Make predictions on the test set with progress bar
    y_pred = model.predict(X_test)
    pbar.update(50)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')