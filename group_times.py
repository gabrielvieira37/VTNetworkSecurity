import matplotlib.pyplot as plt
import pandas as pd
import argparse

def group(hash_name):
    time_series = pd.read_json(f'received_times_{hash_name.upper()}.json', typ='series')
    cum_sum_plot = []
    x = []
    size = time_series.size
    if size == 1000:
        final_range = 50
        steps = 20
    else:
        final_range = size
        steps=1
    for i in range(final_range):
        x.append(i*steps)
        curr_cum_sum = time_series.iloc[0:i*steps].sum()
        cum_sum_plot.append(curr_cum_sum)
    cum_sum_plot_series = pd.Series(cum_sum_plot)
    cum_sum_plot_series.to_json(f'cum_sum_plot_{hash_name.upper()}.json')

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-n", "--name", help="hash name")
    args = argParser.parse_args()
    group(args.name)