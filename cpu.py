# Shapiro-Wilk Test
import json
from numpy.random import seed
from numpy.random import randn
from scipy.stats import shapiro, wilcoxon, norm, kstest, ttest_rel, normaltest
import matplotlib.pyplot as plt

path = "./debugadd1/cpu-t-add-"

def plot2(data1, data2):
    colors = ['red', 'lime']
    plt.hist([data1,data2], histtype='bar', color=colors, label=["zap", "logrus"])
    plt.legend(prop={'size': 10})
    plt.xlabel("cpu usage")
    plt.ylabel("occurance")
    # plt.set_title('bars with legend')
    plt.show()

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

# print(zdata)
print("zap")
zmean = 0
z_user_arr = []
z_sys_arr = []
for i in range(len(zdata)):
    z_user_arr.append(zdata[i][1])
    z_sys_arr.append(zdata[i][2])
    zmean += zdata[i][1]
zfile.close()
zmean /= len(zdata)

# load logrus mem data
lrfile = open(f'{path}logrus.json')
lres = json.load(lrfile)
ldata = lres["data"]
print("logrus")

lmean = 0
l_user_arr = []
l_sys_arr = []

for i in range(len(ldata)):
    l_user_arr.append(ldata[i][1])
    l_sys_arr.append(ldata[i][2])
    lmean += ldata[i][1]

lmean /= len(ldata)

print("logrus")
print("logrus mean:", lmean)
normality_test(l_user_arr)

print("zap:")
print("zap mean:", zmean)
normality_test(z_user_arr)

plot2(z_user_arr, l_user_arr)

res = wilcoxon(l_user_arr, z_user_arr, alternative='greater')
print(res)
tres = ttest_rel( l_user_arr, z_user_arr)
print(tres)
# from matplotlib import pyplot
# pyplot.hist(zarr)
# pyplot.show()