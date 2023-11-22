import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import json
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

def decision_maker(recieved_json):
    df = pd.read_json(recieved_json, orient="records")# Change it to receive message from socket
    X = df.drop(columns=['default payment next month',"ID", "Accuracy"])
    y = df['default payment next month']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test
    clf = DecisionTreeClassifier(random_state=1234, max_depth=3)
    model = clf.fit(X_train,y_train)
    #Predict the response for test dataset
    y_pred = clf.predict(X_test)
    print("Recall:",metrics.recall_score(y_test, y_pred))
    fig, ax = plt.subplots(1, figsize=(25,20))
    _ = tree.plot_tree(clf,
                    feature_names=list(X.columns),
                    class_names=["denied", "approved"],
                    filled=True,
                    ax=ax)
    plt.title("Decision Tree Process", fontsize=40)
    plt.savefig('decision_tree.png', bbox_inches='tight')
    plt.close(fig)

    importance = model.feature_importances_


    new_importance, new_importance_lables = [], []
    for i, v in enumerate(importance):
        if v!=0:
            new_importance.append(v)
            new_importance_lables.append(X.columns[i])

    fig = plt.figure(figsize=(25,20))
    # summarize feature importance
    # for i,v in enumerate(importance):
    #     if v!=0:
    #         print(f'Feature: {X.columns[i]}, Score: {v:.4f}')
    # plot feature importance
    plt.title("Feature Importance", fontsize=40)
    plt.ylabel("Importance", fontsize=25)
    plt.xlabel("Feature", fontsize=25)
    plt.xticks([x for x in range(len(new_importance))] ,(new_importance_lables), fontsize=30)
    plt.bar([x for x in range(len(new_importance))], new_importance)
    plt.savefig('feature_importance.png')
    plt.close(fig)
    print("End decision maker")
    # plt.show()

if __name__ == "__main__":
    raw_file = open('credit_card.json')
    df = pd.read_json(raw_file, orient="records")
    masked_df = df[df['Accuracy']==1].reset_index(drop=True)
    # import pdb; pdb.set_trace()
    decision_maker(masked_df.to_json(orient="records"))
    # decision_maker(raw_file)