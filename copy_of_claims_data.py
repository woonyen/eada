# -*- coding: utf-8 -*-
"""Copy of Claims Data

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uw8TS-BdyNkp4Mx_-yImyu7aO1lSJdjl
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_excel('Sample Data.xlsx')
print(df.shape)
df.head()

df.info()

"""# Drop Duplicate Values"""

df.shape

df.drop_duplicates().shape

df = df.drop_duplicates()

df.isnull().sum()

df[['ClaimType','RecPartParticulars', 'PriceSource', 'SalvageInd','RecPartsDisc',
       'RecPartsRepAmount', 'RecPartsRepFPInd',
       'RecPartsAdjAmount', 'RecPartsAdjFPInd']].info()

df.info()

"""# Drop Unnecessary column"""

drop_column = ['Merimen CaseID','Claim No','RepCoName','RepCoName','RecPartQty','RecPartNo','PartNo','SourceFile']
df = df.drop(drop_column,axis=1)

df.describe()

"""# Drop betterment as all zero"""

df = df.drop('RecPartsBetterment',axis=1)

"""# Categorical Data"""

df.describe(include = 'object')

"""## Drop RecCondition as too many unique"""

df = df.drop('RecCondition',axis=1)

"""# Clustering"""

df.columns

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df_copy = df.fillna(0)

X = df_copy[['RecPartsRepAmount', 'RecPartsAdjAmount','RecPartsInsAmount']]

cluster = KMeans(n_clusters = 2)
cluster_labels = cluster.fit_predict(X)

cluster.fit(X)
cluster.cluster_centers_

np.unique(cluster_labels, return_counts=True)

silhouette_avg = silhouette_score(X, cluster_labels)

silhouette_avg

from matplotlib.colors import ListedColormap
customcmap = ListedColormap(["yellow", "mediumblue"])

fig = plt.figure(figsize=(20, 10))
ax1 = fig.add_subplot(111, projection='3d')
ax1.scatter(df_copy['RecPartsRepAmount'], df_copy['RecPartsAdjAmount'], df_copy['RecPartsInsAmount'], 
            c=cluster_labels, s=40, cmap=customcmap)

"""# Get y """

y = df['RecPartsInsAmount'].tolist()

"""# Exploration of Continuous Variable"""

for c in df.columns:
  if df[c].dtype!='O':
    
    plt.hist(df[c])
    plt.title(c)
    plt.show()

plt.figure(figsize=(10,6))
plt.hist(df['RecPartsDisc'], bins=30)
plt.xlabel('Discount Rate (%)')
plt.ylabel('Number of cases')
plt.title('Histogram of Discount Rate Given by Repairer', pad=10);

plt.figure(figsize=(10,6))
plt.hist(df['RecPartsRepAmount'], color='blue', label='Repairer Amount', alpha=1, bins=50)
plt.hist(df['RecPartsAdjAmount'], color='yellow', label='Adjuster Amount', alpha=1, bins=50)
plt.hist(df['RecPartsInsAmount'], color='red', label='Insurer Amount', alpha=0.5, bins=50)
plt.legend(loc=(0.75,0.8))
plt.xlabel('Amount (RM)')
plt.ylabel('Number of cases')
plt.title('Histogram of Repairer Amount, Adjuster Amount and Insurer Amount', pad=10);



df.isnull().sum()



"""# Boxplot"""

df.info()

for i in df.columns:
  if df[i].dtype!='O':
    plt.figure()
    plt.tight_layout()
    sns.set(rc={"figure.figsize":(8, 5)})
    f, ax_box = plt.subplots(1, sharex=True)
    plt.gca().set(xlabel= i,ylabel='Frequency')
    sns.boxplot(df[i], ax=ax_box , linewidth= 1.0);

"""# Remove outlier - skip"""

# df_copy = df.copy()
# for c in df.columns:
#   if df[c].dtype!='O':
#     if c=='RecPartsInsAmount':
#       continue
#     q1 = df[c].quantile(0.25)
#     q3 = df[c].quantile(0.75)
#     iqr = q3-q1
#     lower_limit = q1-(1.5*iqr)
#     upper_limit = q3+(1.5*iqr)
#     print("{} Upper:{} Lower:{}".format(c,upper_limit,lower_limit))
#     df_copy = df_copy[
#         (df_copy[c]>lower_limit)&
#         (df_copy[c]<upper_limit)&
#         (~df_copy[c].isnull())
#     ]

"""# Remove Null Values of RecPartsInsAmount"""

df_copy = df.copy()

df_copy = df_copy[
    ~df_copy['RecPartsInsAmount'].isnull()
]

df_copy.shape

"""# Correlation"""

df_copy.corr()

sns.heatmap(df_copy.corr(), cmap="YlGnBu", annot=True)

# correlation matrix for cases above 10k and below 10k
sns.heatmap(df_copy[df_copy['RecPartsInsAmount']<=10000].corr(), cmap="YlGnBu", annot=True)

sns.heatmap(df_copy[df_copy['RecPartsInsAmount']>10000].corr(), cmap="YlGnBu", annot=True)

X_cols = ['RecPartsDisc','RecPartsRepAmount', 'RecPartsAdjAmount']

for col in X_cols:
  figure = plt.figure
  ax = plt.gca()
  ax.scatter(df_copy[col], df_copy['RecPartsInsAmount'])
  ax.set_xlabel(col)
  ax.set_ylabel('Insurer Amount')
  ax.set_title("{} vs {}".format(col, 'Insurer Amount'))

  plt.legend()
  plt.show()



"""# Train Test Split"""

df_slr = df_copy[['RecPartsAdjAmount','RecPartsInsAmount']].dropna()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df_slr['RecPartsAdjAmount'], df_slr['RecPartsInsAmount'], test_size=0.33, random_state=42)

"""# Simple Linear Regression"""

import numpy as np
X_train = np.expand_dims(X_train,1)
X_test = np.expand_dims(X_test,1)

from sklearn.linear_model import LinearRegression

reg = LinearRegression().fit(X_train, y_train)
reg.score(X_train, y_train)

from sklearn.metrics import mean_squared_error

y_pred = reg.predict(X_test)
mean_squared_error(y_test, y_pred, squared=False)

from sklearn.metrics import r2_score

X_all = np.expand_dims(df_slr['RecPartsAdjAmount'],1)
y_all = df_slr['RecPartsInsAmount']
y_pred_all = reg.predict(X_all)
r2_score(y_train,y_pred)



r2_score(y_all,y_pred_all)

reg.coef_

reg.intercept_

plt.scatter(X_test, y_test, label='Actual')
plt.plot(X_test, y_pred, color='red', label='Predicted')
plt.title('Adjuster Amount vs Insurer Amount', pad=10)
plt.xlabel('RecPartsAdjAmount')
plt.ylabel('RecPartsInsAmount')
plt.legend(loc=(1.1,0.8))

"""# Multiple Linear Regression"""

df_copy.columns

df_copy = df_copy.dropna()

X = df_copy[['ClaimType','RecPartParticulars', 'PriceSource', 'SalvageInd','RecPartsDisc',
       'RecPartsRepAmount', 'RecPartsRepFPInd',
       'RecPartsAdjAmount', 'RecPartsAdjFPInd']]


y = df_copy['RecPartsInsAmount']

X = pd.get_dummies(X, drop_first=True)

mlr_X_train, mlr_X_test, mlr_y_train, mlr_y_test = train_test_split(X, y, test_size=0.33, random_state=42)

mlr = LinearRegression().fit(mlr_X_train, mlr_y_train)

mlr_y_pred = mlr.predict(mlr_X_test)

r2_score(mlr_y_test,mlr_y_pred)

r2_score(mlr_y_test,mlr_y_pred)

pd.DataFrame(zip(X.columns, mlr.coef_))

mean_squared_error(mlr_y_test, mlr_y_pred,squared=False)

