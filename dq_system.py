import numpy as np
import json
import pandas as pd


def main():
    df = pd.read_excel('default_of_credit_card_clients.xls', header=1)
    df['Accuracy'] = 1
    X = df.drop(columns=['default payment next month',"ID", "Accuracy"])
    y = df['default payment next month']
    # Article Rules (Accuracy/Consistency)
    good_education_quality_index = X[X['EDUCATION']<=4.0].index
    bad_education_quality_index = X[X['EDUCATION']>4.0].index
    X = X.iloc[good_education_quality_index]
    y = y.iloc[good_education_quality_index]
    X.reset_index(drop=True, inplace=True)
    y.reset_index(drop=True, inplace=True)

    bad_marriage_quality_index = X[X['MARRIAGE']==0].index
    good_marriage_quality_index = X[X['MARRIAGE']>0].index
    X = X.iloc[good_marriage_quality_index]
    y = y.iloc[good_marriage_quality_index]
    X.reset_index(drop=True, inplace=True)
    y.reset_index(drop=True, inplace=True)

    df['Accuracy'].iloc[bad_education_quality_index] = 0
    df['Accuracy'].iloc[bad_marriage_quality_index] = 0
    df.to_json("credit_card.json", orient='records')

if __name__ == "main":
    main()