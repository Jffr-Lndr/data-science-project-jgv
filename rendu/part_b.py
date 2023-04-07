import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sn

DATABASE_URL = "postgresql+psycopg2://project_dat_5623:STdvleCgo7H9jXH7osWL@project-dat-5623.postgresql.a.osc-fr1.scalingo-dbs.com:32019/project_dat_5623?sslmode=prefer"
engine = create_engine(DATABASE_URL, connect_args={'sslmode': "allow"})

data_frame = pd.read_sql('data_cleaned', engine).dropna()

# Récupère chaque variable quantitative autre que le prix et les représentes dans un scatter plot
def graph_1():
    Y = data_frame['price']
    fig = plt.figure()
    a = fig.add_subplot(221)
    b = fig.add_subplot(222)
    c = fig.add_subplot(223)
    d = fig.add_subplot(224)

    a.scatter(data_frame[['total_sqft']], Y)
    a.set_title('Surface')
    a.set_ylabel('Prix')

    b.scatter(data_frame[['size']], Y)
    b.set_title('Pieces')
    b.set_ylabel('Prix')

    c.scatter(data_frame[['bath']], Y)
    c.set_title('Salle de Bain')
    c.set_ylabel('Prix')

    d.scatter(data_frame[['balcony']], Y)
    d.set_title('Balcon')
    d.set_ylabel('Prix')
    plt.show()

# Permet de représenter un graphique qui détermine pour quel nombre de balcons les biens ont le prix moyen le plus élevé.
def graph_2():

    def avg_price_balc(balcony_number):
        return data_frame[data_frame['balcony'] == balcony_number].mean(axis=0,numeric_only=True)['price']


    Y = data_frame['price']
    plt.scatter(data_frame[['balcony']], Y)
    plt.plot([avg_price_balc(x) for x in range(int(data_frame.max(axis=0)['balcony'])+1)])
    plt.xlabel('Balcon')
    plt.ylabel('Prix')
    plt.show()

# Représente un graphique qui permet de déterminer pour quel nombre de salles de bains les biens ont le prix moyen le plus élevé.
def graph_3():

    def avg_price_bath(bath_number):
        return [bath_number,data_frame[data_frame['bath'] == bath_number].mean(axis=0,numeric_only=True)['price']]


    Y = data_frame['price']
    plt.scatter(data_frame[['bath']], Y)
    to_plot = [avg_price_bath(x) for x in data_frame.drop_duplicates(['bath'])['bath']]
    to_plot.sort(key=lambda x: x[0])
    plt.plot([x[0] for x in to_plot],[x[1] for x in to_plot])
    plt.xlabel('Salle de Bain')
    plt.ylabel('Prix')
    plt.show()

#Créer une DataFrame avec les colonnes availability, count, count_cum, price_mean et les stocks dans une DataFrame nommée data_availability.
def reframe_4():
    data_availability = data_frame.drop_duplicates(['availability'])
    data_availability['count'] = [data_frame[data_frame['availability'] == x].count(axis=0)[0] for x in data_availability['availability']]
    data_availability = data_availability[['availability','count']]
    data_availability['count_cum'] = [data_frame[data_frame['availability'] <= x].count(axis=0)[0] for x in data_availability['availability']]
    data_availability['price_mean'] = [data_frame[data_frame['availability'] == x].mean(axis=0,numeric_only=True)['price'] for x in data_availability['availability']]
    data_availability.to_sql('data_availability',engine,if_exists='replace')

# Représente la matrice des corrélations des variables quantitatives
def corr_5():
    cols = ['size','total_sqft','bath','balcony','price']
    matrix = data_frame[cols].corr()
    correlation_matrix_values = pd.DataFrame(columns=['variable_1','variable_2','coefficient_correlation'])

    for i in range(4):
        x = cols[i]
        for y in cols[i+1:]:
            new_row = pd.DataFrame({'variable_1':x,'variable_2':y,'coefficient_correlation':matrix[x][y]},index=[0])
            correlation_matrix_values = pd.concat([new_row,correlation_matrix_values.loc[:]]).reset_index(drop=True)
    sn.heatmap(matrix, annot=True)
    plt.show()
    correlation_matrix_values.to_sql('correlation_matrix_values',engine,if_exists='replace')

#graph_1()
#graph_2()
#graph_3()
#reframe_4()
corr_5()