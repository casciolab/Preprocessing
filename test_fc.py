import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Data set
df=pd.DataFrame.from_csv("/Users/Failla/Desktop/PIEC/RestingState/r_to_z_group_diff_t.csv")

# plot
p = sns.heatmap(df)

plt.show(p)

0   1   3.94
0   1   13.94
1   0   0
0   0   0
1   0   -4.06
1   0   -5.06
0   1   1.94
1   0   -7.06
0   1   4.94
0   0   0
0   1   6.94
0   1   9.94
0   0   0
0   1   -4.06
0   0   0
0   1   -4.06
0   0   0
0   1   12.94
1   0   -7.06
0   1   -4.06
0   1   4.94
0   1   14.94
0   1   -3.06
1   0   7.94
1   0   -9.06
1   0   29.94
0   1   -7.06
0   1   -10.06
0   1   -11.06
1   0   -4.06
0   1   -3.06
0   1   -6.06
0   1   -9.06
1   0   -10.06
1   0   -11.06
1   0   0
1   0   -3.06
0   1   -5.06
1   0   -11.06
1   0   3.94
0   1   -7.06
0   1   -3.06
1   0   -5.06
1   0   -11.06
0   1   -11.06
0   1   -3.06
1   0   -3.06
0   1   -10.06
1   0   0.940000000000001
0   1   -11.06
0   1   -2.06
1   0   0.940000000000001
1   0   0.940000000000001
1   0   -9.06
1   0   15.94
1   0   21.94
0   1   3.94
0   1   -8.06
0   1   -8.06
0   1   18.94
1   0   34.94
1   0   2.94
0   1   -11.06
1   0   5.94
1   0   -11.06
0   1   -10.06
0   1   -8.06
0   1   6.94
1   0   -9.06
0   1   14.94
0   1   9.94
0   1   13.94
0   1   2.94
0   1   13.94
0   1   8.94
1   0   4.94
0   1   4.94
0   1   12.94
0   1   13.94
1   0   -7.06
1   0   3.94
1   0   6.94
0   1   -10.06
0   1   -11.06
0   1   -9.06
0   1   5.94
0   1   4.94
0   1   11.94
0   1   11.94
0   1   5.94
0   1   5.94
0   1   2.94
0   0   0
1   0   -11.06
1   0   -6.06
1   0   -2.06
1   0   -11.06
0   1   -10.06
1   0   23.94
1   0   -5.06
1   0   4.94
1   0   -2.06
1   0   7.94

1   0   21.90709984
1   0   11.5027381
0   1   -21.03183824
1   0   -4.88238513
0   1   3.26044118
0   1   -28.25916667
0   1   -7.96714387
0   1   -33.84969173
0   1   17.63573887
0   1   17.65119748
1   0   -36.47873779
0   1   21.62178571
0   1   14.64444933
0   1   10.26223112
1   0   -29.42761826
1   0   -9.90365054999999
1   0   1.98276882
0   1   5.89635712
0   1   5.20574560999999
0   1   -22.04388889
1   0   3.35294254
1   0   -15.85941729
1   0   -1.70335406
0   1   -29.90091639
0   1   21.32213017
1   0   11.28712963
1   0   14.46165861
0   1   1.23344603
1   0   19.59797619
1   0   -34.40030781
0   1   -0.226947460000005
0   1   14.78681034
1   0   -41.57900472
1   0   0.0673760699999946
1   0   2.00598485
1   0   -3.56813873999999
0   1   -12.29325758
0   1   -16.47125268
0   1   -10.20055861
1   0   7.15569625000001
1   0   12.98662458
0   1   -17.39382764
0   1   -30.75916667
0   1   16.81708606
1   0   -16.24312624
0   1   10.33181562
0   1   5.86165011999999
0   1   17.1575
0   1   18.52534512
0   1   -11.82437053
0   1   4.7585101
1   0   8.26708486
0   1   18.07321835
0   1   -8.64230843
0   1   10.32506272
1   0   5.60285325
1   0   22.33223118
1   0   21.44501804
0   1   10.8867038
0   1   9.51861110999999
0   1   17.35761796
0   1   19.91817323
0   1   -12.09385501


21.90709984
11.5027381
-21.03183824
-4.88238513
3.26044118
-28.25916667
-7.96714387
-33.84969173
17.63573887
17.65119748
-36.47873779
21.62178571
14.64444933
10.26223112
-29.42761826
-9.90365055
1.98276882
5.89635712
5.20574561
-22.04388889
3.35294254
-15.85941729
-1.70335406
-29.90091639
21.32213017
11.28712963
14.46165861
1.23344603
19.59797619
-34.40030781
-0.22694746
14.78681034
-41.57900472
0.06737607
2.00598485
-3.56813874
-12.29325758
-16.47125268
-10.20055861
7.15569625
12.98662458
-17.39382764
-30.75916667
16.81708606
-16.24312624
10.33181562
5.86165012
17.1575
18.52534512
-11.82437053
4.7585101
8.26708486
18.07321835
-8.64230843
10.32506272
5.60285325
22.33223118
21.44501804
10.8867038
9.51861111
17.35761796
19.91817323
-12.09385501