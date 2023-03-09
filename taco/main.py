import string 
import pandas as pd
import numpy as np

try:
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import CountVectorizer
except ImportError as e:
    print(e)

def fill_null(csv):
    """ fill null values with average values from similar rows """
    pass

def dataset_cleanup(dataframe: pd.DataFrame) -> pd.DataFrame:
    """ dataset cleanup if dataset has null values """

    if dataframe[dataframe.isna().any(axis=1)].empty:
        print("Dataset has no null values")
    else:
        print("Datafram has null values!")
        dataframe = dataframe.dropna()

    return dataframe

def text_process(txt):
    return "".join([char for char in txt if char not in string.punctuation or char != "–"]).split()


def main():

    # read csv file as pandas dataframe
    df = pd.read_csv("dataset.csv")
    # remove rows from dataset with null values
    df = dataset_cleanup(df)
    
    feature = df.iloc[:, 1]
    bow_transformer = CountVectorizer(analyzer=text_process).fit(feature)
    friend_bow = bow_transformer.transform(feature).toarray()
    employe = df.iloc[:, 0].to_numpy()

    model = DecisionTreeClassifier()
    model.fit(friend_bow, employe)

    search = input("->")
    c_word = bow_transformer.transform([search]) 
    y_pred = model.predict(c_word)
    print(y_pred)

    # y_pred = model.predict(x_test)
    # print(f"accuracy: {accuracy_score(y_test, y_pred)}")
    # print(f"f1-score: {f1_score(y_test, y_pred, average='macro')}")




if __name__ == "__main__":
    main()