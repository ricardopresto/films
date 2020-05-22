import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report

df = pd.read_pickle('1971-1989_processed.pkl')

#scaler = StandardScaler()

cols = df.columns.to_flat_index()
cols = list(cols)
for n in range(len(cols)):
    if cols[n][1] == '':
        cols[n] = cols[n][0]
    else:
        cols[n] = cols[n][0] + '_' + cols[n][1]

df.columns = cols

df = df.drop('title', axis=1)

df = df.apply(pd.to_numeric)

imp = SimpleImputer(missing_values=np.nan, strategy='mean')

na_cols = ['budget', 'box_office', 'profit', 'time']

imputed = imp.fit_transform(df[na_cols])
imputed = pd.DataFrame(imputed)

df.budget = imputed[0]
df.box_office = imputed[1]
df.profit = imputed[2]
df.time = imputed[3]


X = df.drop(['nom'], axis=1)
y = df.nom


X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.2)

rfc = RandomForestClassifier(max_features='sqrt', n_estimators=200)
gbc = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1)

rfc = rfc.fit(X_train, y_train)
gbc = gbc.fit(X_train, y_train)

res1 = rfc.predict(X_test)
res2 = gbc.predict(X_test)


print(classification_report(y_test, res1))
print(classification_report(y_test, res2))

df.corr()
