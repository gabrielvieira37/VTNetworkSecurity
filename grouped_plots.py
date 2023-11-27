import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


def boxplot():
    md5 = pd.read_json(f'received_times_MD5.json', typ='series')
    sha1 = pd.read_json(f'received_times_SHA1.json', typ='series')
    sha256 = pd.read_json(f'received_times_SHA256.json', typ='series')
    sha512 = pd.read_json(f'received_times_SHA512.json', typ='series')

    labels = ['MD5', 'SHA1', 'SHA256', 'SHA512']

    fig, ax = plt.subplots(1, figsize=(12,9))
    plt.title('Boxplot of request times of all hahes')
    plt.xlabel('Hashes')
    plt.ylabel('Request time of requests(ms)')
    bplot = ax.boxplot([md5, sha1, sha256, sha512], vert=True, patch_artist=True, labels=labels)
    # plt.show()
    plt.savefig(f'boxplot_all_hashes.png')
    plt.close()

def line_graph():
    md5 = pd.read_json(f'cum_sum_plot_MD5.json', typ='series')
    sha1 = pd.read_json(f'cum_sum_plot_SHA1.json', typ='series')
    sha256 = pd.read_json(f'cum_sum_plot_SHA256.json', typ='series')
    sha512 = pd.read_json(f'cum_sum_plot_SHA512.json', typ='series')
    x = 20*np.arange(md5.size)
    fig = plt.Figure(figsize=(12,9))
    plt.plot(x, md5, label='md5')
    plt.plot(x, sha1, label='sha1')
    plt.plot(x, sha256, label='sha256')
    plt.plot(x, sha512, label='sha512')
    plt.title('Cumulative request time after multiple requests')
    plt.ylabel('Cumulative request time(ms)')
    plt.xlabel('Number of requests')
    plt.legend()
    plt.grid()
    # plt.show()
    plt.savefig(f'line_graph_all_hashes.png')

if __name__=='__main__':
    boxplot()
    line_graph()