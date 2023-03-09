import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

with open("dataset.csv", "r") as file:
    dataset = pd.read_csv(file)

x = dataset.iloc[:, 1:]
y = dataset.iloc[:, 0]

print(x_train)

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
