import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

def main():
    print("hello world")
    df = pd.read_json("credit_card.json", orient="records")# Change it to receive message from socket
    X = df.drop(columns=['default payment next month',"ID", "Accuracy"])
    y = df['default payment next month']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test
    clf = DecisionTreeClassifier(random_state=1234, max_depth=3)
    model = clf.fit(X_train,y_train)
    #Predict the response for test dataset
    y_pred = clf.predict(X_test)
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    fig = plt.figure(figsize=(25,20))
    tree.plot_tree(clf,
                    feature_names=list(X.columns),
                    class_names=["denied", "approved"],
                    filled=True)
    plt.savefig('foo.png')

    importance = model.feature_importances_
    new_importance = [x for x in importance if x!=0 ]
    fig = plt.figure(figsize=(25,20))
    # summarize feature importance
    for i,v in enumerate(importance):
        if v!=0:
            print(f'Feature: {X.columns[i]}, Score: {v:.4f}')
    # plot feature importance
    plt.bar([x for x in range(len(new_importance))], new_importance)
    plt.savefig('foo2.png')
    # plt.show()

if __name__ == "__main__":
    main()