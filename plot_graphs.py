import matplotlib.pyplot as plt
import pandas as pd
import argparse

def plot(hash_name):
    time_series = pd.read_json('received_times.json', typ='series')
    cum_sum_plot = []
    x = []
    for i in range(50):
        x.append(i*20)
        curr_cum_sum = time_series.iloc[0:i*20].sum()
        cum_sum_plot.append(curr_cum_sum)
    cum_sum_plot_series = pd.Series(cum_sum_plot)
    cum_sum_plot_series.to_json(f'cum_sum_plot_{hash_name}.json')

    fig = plt.figure(figsize=(25,20))
    plt.title("Cumulative request time after multiple requests", fontsize=40)
    plt.ylabel("Time of requests(ms)", fontsize=25)
    plt.xlabel("Number of requests", fontsize=25)
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    plt.scatter(x, cum_sum_plot, label='Cumulative time')
    plt.savefig(f'cum_req_plot_{hash_name}.png')
    plt.close(fig)

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-n", "--name", help="hash name")
    args = argParser.parse_args()
    plot(args.name)