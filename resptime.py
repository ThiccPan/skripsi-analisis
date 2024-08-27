import json
import matplotlib.figure
import numpy as np
from numpy.random import seed
from numpy.random import randn
from numpy import hstack, repeat
from scipy.stats import shapiro, wilcoxon, kstest, norm, normaltest, ttest_rel
from pandas import read_csv, DataFrame, Series
import matplotlib.pyplot as plt

def read_resp_csv(path: str) -> DataFrame:
    df = read_csv(path)
    duration_filter = df["metric_name"] == "http_req_duration"
    df = df[duration_filter]
    duration_filter = df["url"] == "http://localhost:8080/items"
    df = df[duration_filter]
    return df

def normality_test(data: Series):
    print(data)
    loc, scale = norm.fit(data)
    # create a normal distribution with loc and scale
    n = norm(loc=loc, scale=scale)
    ks_res = kstest(data, n.cdf)
    print(ks_res)

    shapiro_res = shapiro(data)
    print(shapiro_res)

    stat, p = normaltest(data)
    print(p)
    return n

def plot(data, n):
    plt.hist(data, bins=np.arange(data.min(), data.max()+0.2, 2), rwidth=0.5)
    x = np.arange(data.min(), data.max()+0.2, 0.2)
    plt.plot(x, 350*n.pdf(x))
    plt.show()

def plot2(data1, data2):
    colors = ['red', 'lime']
    plt.hist([data1,data2], histtype='bar', color=colors, label=["zap", "logrus"])
    plt.legend(prop={'size': 10})
    plt.xlabel("time")
    plt.ylabel("occurance")
    # plt.set_title('bars with legend')
    plt.show()

def main():
    # path = "./debuggetall2/test-getall-"
    path = "./infogetall1/test-getall-"  
    zap_df = read_resp_csv(f'{path}zap.csv')
    zap_val = zap_df["metric_value"]
    print("zap:")
    print("mean: ", zap_val.mean())
    print("min: ", zap_val.min())
    print("max: ", zap_val.max())
    # zap_df.to_json("./infogetall1/zap-resp.json")
    normality_test(zap_val)
    print()

    lr_df = read_resp_csv(f'{path}logrus.csv')
    lr_val = lr_df["metric_value"]
    print("logrus:")
    print("mean:", lr_val.mean())
    print("min: ", lr_val.min())
    print("max: ", lr_val.max())
    # lr_df.to_json("./infogetall1/logrus-resp.json")
    normality_test(lr_val)

    diff = wilcoxon(zap_val, lr_val)
    diff_ttest = ttest_rel(zap_val, lr_val)
    print(diff)
    plot2(zap_val.array, lr_val.array)

main()