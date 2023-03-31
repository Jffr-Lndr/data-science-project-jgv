import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import datetime
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

DATABASE_URL = "postgresql+psycopg2://project_dat_5623:STdvleCgo7H9jXH7osWL@project-dat-5623.postgresql.a.osc-fr1.scalingo-dbs.com:32019/project_dat_5623?sslmode=prefer"
engine = create_engine(DATABASE_URL, connect_args={'sslmode': "allow"})

data_frame = pd.read_sql('data_cleaned', engine)
data_frame = data_frame.dropna()

data_frame.to_sql('data_cleaned_3', engine, if_exists='replace')


# Prediction Surface
def pred_1():
    data_frame_train,data_frame_test = train_test_split(data_frame,train_size = 0.7,test_size=0.3,random_state=42)

    data_frame_train.to_sql('train', engine, if_exists='replace')
    data_frame_test.to_sql('test', engine, if_exists='replace')


    Y = data_frame_train['price']
    X = data_frame_train[['total_sqft']]

    linear_model = LinearRegression(
        fit_intercept=False
    )
    linear_model.fit(X, Y)

    plt.scatter(X, Y)
    plt.xlabel('Surface')
    plt.ylabel('Prix')

    X = data_frame_test[['total_sqft']]

    y_predictions_test = linear_model.predict(X)
    plt.plot(X, y_predictions_test, color='red')
    plt.show()

    model_1_predictions = data_frame_test[['index','total_sqft','price']]
    model_1_predictions['price_pred'] = y_predictions_test
    model_1_predictions.to_sql('model_1_predictions',engine,if_exists='replace')



# Prediction Disponibilité
def pred_2():
    def days_before_calc(availability):
        today = datetime.now()
        return max(0,math.floor((availability-today).total_seconds()/86400))

    data_frame['days_before'] = [days_before_calc(x) for x in data_frame['availability']]

    data_frame.to_sql('data_cleaned_4', engine, if_exists='replace')

    data_frame_train,data_frame_test = train_test_split(data_frame,train_size = 0.7,test_size=0.3,random_state=42)

    data_frame_train.to_sql('train_2', engine, if_exists='replace')
    data_frame_test.to_sql('test_2', engine, if_exists='replace')


    Y = data_frame_train['price']
    X = data_frame_train[['days_before']]

    linear_model = LinearRegression(
        fit_intercept=False
    )
    linear_model.fit(X, Y)

    plt.scatter(X, Y)
    plt.xlabel('Disponibilité')
    plt.ylabel('Prix')

    X = data_frame_test[['days_before']]

    y_predictions_test = linear_model.predict(X)
    plt.plot(X, y_predictions_test, color='red')
    plt.show()

    model_1_predictions = data_frame_test[['index','days_before','price']]
    model_1_predictions['price_pred'] = y_predictions_test
    model_1_predictions.to_sql('model_1_predictions_days_before',engine,if_exists='replace')



#Prediction Multiple
def pred_3():
    def days_before_calc(availability):
        today = datetime.now()
        return max(0,math.floor((availability-today).total_seconds()/86400))

    data_frame['days_before'] = [days_before_calc(x) for x in data_frame['availability']]

    data_frame.to_sql('data_cleaned_4', engine, if_exists='replace')

    data_frame_train,data_frame_test = train_test_split(data_frame,train_size = 0.7,test_size=0.3,random_state=42)

    data_frame_train.to_sql('train_2', engine, if_exists='replace')
    data_frame_test.to_sql('test_2', engine, if_exists='replace')


    Y = data_frame_train['price']
    X = data_frame_train[['size','days_before','total_sqft','bath','balcony']]

    linear_model = LinearRegression(
        fit_intercept=False
    )
    linear_model.fit(X.values, Y)

    X = data_frame_test[['size','days_before','total_sqft','bath','balcony']]

    y_predictions_test = linear_model.predict(X.values)

    model_2_predictions = data_frame_test[['index','total_sqft','price']]
    model_2_predictions['price_pred'] = y_predictions_test
    model_2_predictions.to_sql('model_2_predictions',engine,if_exists='replace')
    print(model_2_predictions)

#Prediction Multiple avec Categorie
def pred_4():
    def days_before_calc(availability):
        today = datetime.now()
        return max(0,math.floor((availability-today).total_seconds()/86400))

    data_frame['days_before'] = [days_before_calc(x) for x in data_frame['availability']]
    data_frame['area_type'] = [x.replace(' ','').lower() for x in data_frame['area_type']]

    data_frame.to_sql('data_cleaned_4', engine, if_exists='replace')

    data_frame_d = pd.get_dummies(data_frame['area_type'],prefix='area')
    data_frame_with_d = pd.concat([data_frame, data_frame_d], axis=1)

    data_frame_train,data_frame_test = train_test_split(data_frame_with_d,train_size = 0.7,test_size=0.3,random_state=42)

    data_frame_train.to_sql('train_2', engine, if_exists='replace')
    data_frame_test.to_sql('test_2', engine, if_exists='replace')


    Y = data_frame_train['price']
    X = data_frame_train.drop(['price','availability','area_type','location'],axis=1)

    linear_model = LinearRegression(
        fit_intercept=False
    )
    linear_model.fit(X.values, Y)

    X = data_frame_test.drop(['price','availability','area_type','location'],axis=1)
    y_predictions_test = linear_model.predict(X.values)

    model_3_predictions = data_frame_test[['index','total_sqft','price']]
    model_3_predictions['price_pred'] = y_predictions_test
    #model_3_predictions['price_pred_error'] = [x[2] - x[3] for x in model_3_predictions.values]
    model_3_predictions.to_sql('model_3_predictions',engine,if_exists='replace')
    print(model_3_predictions)

#pred_1()
#pred_2()
#pred_3()
pred_4()