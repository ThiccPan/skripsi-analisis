# Shapiro-Wilk Test
import json
import numpy as np
from numpy.random import seed
from numpy.random import randn
from scipy.stats import shapiro, wilcoxon, norm, kstest
import matplotlib.pyplot as plt
# from resptime import plot2

path = "./debugadd1/mem-t-add-"

def normality_test(data):
    loc, scale = norm.fit(data)
    # create a normal distribution with loc and scale
    n = norm(loc=loc, scale=scale)
    ks_res = kstest(data, n.cdf)
    print(ks_res)

    shapiro_res = shapiro(data)
    print(shapiro_res)

    return n

# load zap mem data
zfile = open(f'{path}zap.json')

zres = json.load(zfile)
zdata = zres["data"]
print("zap:")
zarr = []
zmean = 0
for i in range(len(zdata)):
    zarr.append(zdata[i][1])
    print(zdata[i][1])
    zmean += zdata[i][1]
zmean /= len(zdata)

# print(zarr)
zfile.close()

normality_test(zarr)

# load logrus mem data
lrfile = open(f'{path}logrus.json')
lres = json.load(lrfile)
ldata = lres["data"]
print("logrus:")
larr = []
lmean = 0
for i in range(len(ldata)):
    larr.append(ldata[i][1])
    print(ldata[i][1])
    lmean += ldata[i][1]
lmean /= len(ldata)

res = wilcoxon(larr, zarr, alternative='greater')
print(res)

def plot2(data1, data2):
    colors = ['red', 'lime']
    plt.hist([data1,data2], histtype='bar', color=colors, label=["zap", "logrus"])
    plt.legend(prop={'size': 10})
    plt.xlabel("memory usage")
    plt.ylabel("occurance")
    # plt.set_title('bars with legend')
    plt.show()

print("logrus")
print("lmean:", lmean)
normality_test(larr)

print("zap")
print("zmean:", zmean)
normality_test(zarr)
plot2(zarr, larr)

# plt.hist(zarr)
# plt.xlabel("value")
# plt.ylabel("occurance")
# plt.ylim([0,70])
# plt.show()

# from matplotlib import pyplot
# pyplot.hist(zarr)
# pyplot.show()