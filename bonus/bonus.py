import pandas as pd
from sklearn.linear_model import LogisticRegression

data_frame_train = pd.read_csv('./ensae_competition_train.txt', header=[0,1], sep="\t", index_col=0)
data_frame_test = pd.read_csv('./ensae_competition_test_X.txt', header=[0,1], sep="\t", index_col=0)

def edu_parse(edu_val):
    if edu_val == 1:
        return 'GRADUATE_SCHOOL'
    if edu_val == 2:
        return 'UNIVERSITY'
    if edu_val == 3:
        return 'HIGH_SCHOOL'
    if edu_val == 4: 
        return 'OTHERS'

def mar_parse(mar_val):
    if mar_val == 1:
        return 'MARRIED'
    if mar_val == 2:
        return 'SINGLE'
    if mar_val == 3: 
        return 'OTHERS'

def pay_parse(pay_val):
    return str(pay_val)

data_frame_train.columns = data_frame_train.columns.droplevel()
data_frame_test.columns = data_frame_test.columns.droplevel()

data_frame_train['SEX'] = [ x-1 for x in data_frame_train['SEX']]
data_frame_train['EDUCATION'] = [ edu_parse(x) for x in data_frame_train['EDUCATION']]
data_frame_train['MARRIAGE'] = [ mar_parse(x) for x in data_frame_train['MARRIAGE']]
data_frame_train['PAY_0'] = [ pay_parse(x) for x in data_frame_train['PAY_0']]
data_frame_train['PAY_2'] = [ pay_parse(x) for x in data_frame_train['PAY_2']]
data_frame_train['PAY_3'] = [ pay_parse(x) for x in data_frame_train['PAY_3']]
data_frame_train['PAY_4'] = [ pay_parse(x) for x in data_frame_train['PAY_4']]
data_frame_train['PAY_5'] = [ pay_parse(x) for x in data_frame_train['PAY_5']]
data_frame_train['PAY_6'] = [ pay_parse(x) for x in data_frame_train['PAY_6']]
data_frame_train = data_frame_train.rename({"default payment next month":"Y"},axis=1)

cat_var =  list(data_frame_train.columns[2:4]) + list(data_frame_train.columns[5:11]) + list(data_frame_train.columns[-1:])
num_var = [v for v in data_frame_train.columns if v not in cat_var]

dummies = pd.get_dummies(data_frame_train[cat_var],drop_first=True)

data_frame_train = pd.concat([data_frame_train[num_var], dummies], axis=1)


data_frame_test['SEX'] = [ x-1 for x in data_frame_test['SEX']]
data_frame_test['EDUCATION'] = [ edu_parse(x) for x in data_frame_test['EDUCATION']]
data_frame_test['MARRIAGE'] = [ mar_parse(x) for x in data_frame_test['MARRIAGE']]
data_frame_test['PAY_0'] = [ pay_parse(x) for x in data_frame_test['PAY_0']]
data_frame_test['PAY_2'] = [ pay_parse(x) for x in data_frame_test['PAY_2']]
data_frame_test['PAY_3'] = [ pay_parse(x) for x in data_frame_test['PAY_3']]
data_frame_test['PAY_4'] = [ pay_parse(x) for x in data_frame_test['PAY_4']]
data_frame_test['PAY_5'] = [ pay_parse(x) for x in data_frame_test['PAY_5']]
data_frame_test['PAY_6'] = [ pay_parse(x) for x in data_frame_test['PAY_6']]

cat_var =  list(data_frame_test.columns[2:4]) + list(data_frame_test.columns[5:11])
num_var = [v for v in data_frame_test.columns if v not in cat_var]

dummies = pd.get_dummies(data_frame_test[cat_var],drop_first=True)

data_frame_test = pd.concat([data_frame_test[num_var], dummies], axis=1)

col_train = data_frame_train.columns.values
col_test = data_frame_test.columns.values

col_train_set = set(col_train)
col_test_set = set(col_test)
missing_in_col_train_set = [x for x in col_test_set if x not in col_train_set]
missing_in_col_test_set = [x for x in col_train_set if x not in col_test_set]

# Does Not Work Yet
for col in missing_in_col_train_set:
    data_frame_train[col] = [0 for x in data_frame_train]

for col in missing_in_col_test_set:
    data_frame_test[col] = [0 for x in data_frame_test]

Y = data_frame_train['Y']
X = data_frame_train.drop(['Y'],axis=1)

model = LogisticRegression(
        fit_intercept=False
    )
model.fit(X.values, Y)


X = data_frame_train.drop(['Y'],axis=1)
y_predictions_test = model.predict(X.values)


print(y_predictions_test)