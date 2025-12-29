#####################################################################
#Aula 47 - Projeto Cury de entregas - Streamlit Visão Empresa
#####################################################################

#Problema de negócio
#############################################
# A Cury Company é uma empresa de tecnologia que criou um aplicativo que conecta
# restaurantes, entregadores e pessoas.<br><br>
# Através desse aplicativo, é possível realizar o pedido de uma refeição, em qualquer
# restaurante cadastrado, e recebê-lo no conforto da sua casa por um entregador
# também cadastrado no aplicativo da Cury Company.<br><br>
# A empresa realiza negócios entre restaurantes, entregadores e pessoas, e gera
# muitos dados sobre entregas, tipos de pedidos, condições climáticas, avaliação dos
# entregadores e etc. Apesar da entrega estar crescento, em termos de entregas, o
# CEO não tem visibilidade completa dos KPIs de crescimento da empresa.<br><br>
# Você foi contratado como um Cientista de Dados para criar soluções de dados para
# entrega, mas antes de treinar algoritmos, a necessidade da empresa é ter um os
# principais KPIs estratégicos organizados em uma única ferramenta, para que o CEO
# possa consultar e conseguir tomar decisões simples, porém importantes.<br><br>
# A Cury Company possui um modelo de negócio chamado Marketplace, que fazer o
# intermédio do negócio entre três clientes principais:<br> Restaurantes;<br> entregadores;<br> e
# pessoas compradoras.


#O DATASET UTILIZADO NESTA SOLUÇÃO FOI TRATADA ANTERIORMENTE EM UM NOTEBOOK ESPECÍFICO PARA O CASE CURY

##############################################
#Requerimentos
##############################################

import pandas as pd
import numpy as np
from datetime import datetime
import re
import plotly.express as px
from matplotlib import pyplot as plt
import folium
from streamlit_folium import folium_static
from haversine import haversine
import streamlit as st
from PIL import Image#para a logo utilizada - biblioteca de m anipulação de imagens

############################################
#Helper functions
############################################
#Config do layout expandido
st.set_page_config(page_title='Visão_Empresa', page_icon='', layout='wide')

#Transformação de casas decimais das notações científicas 
pd.set_option('display.float_format', lambda x: '%.2f' % x)

#Dimensionamento do dataset
def dimensionamento(dataframe):
    print(f"O dataset tem {dataframe.shape[0]} linhas.")
    print(f"O dataset tem {dataframe.shape[1]} colunas.")
    return None

#Tratamento do espaçamento no dados do tipo string - sem loop for
def space_clean(dataframe, coluna):
    dataframe.loc[:, coluna] = dataframe.loc[:, coluna].str.strip()
    return dataframe[coluna]



#################################################
# BACK-END DO PROJETO - DATA LOADER AND DATA PERFORMER
#################################################

# Data load - vamos utilizar o dataset já tratado nos exercícios anteriores
###############################################
data = pd.read_csv("Datasets/train_tratado.csv")

#Aqui vamos alterar o tipo da variável 'Order_Date'

data["Order_Date"] = pd.to_datetime(data["Order_Date"], format="%Y-%m-%d")


#################################################
#FRONT-END - LAYOUT NO STREAMLIT
#################################################
#Todos os widgets criados neste projeto streamlit foram pesquisados na documentação dos Streamlit
#no seguinte endereço: https://docs.streamlit.io/library/api-reference
#Criando um sidebar - aquela barra lateral onde ficarão os filtros que escolheremos
#como parâmetross de visualização de dados
st.header('Marketplace - Visão Empresa')

# 1. BARRA LATERAL - SIDEBAR
###############################################

    #Logotipo
# image_path = 'Delivery_food.png'
image = Image.open('Delivery_food.png')
st.sidebar.image(image, width=300)
st.markdown("""___""")#linha de separação na sidebar

    #Cabeçalho
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")#linha de separação na sidebar
    
    #Filtro de data com slider
st.sidebar.markdown('### Selecione uma data limite')
date_slider = st.sidebar.slider(
                                'Até qual data?',
                                value=pd.datetime(2022, 4, 13),
                                min_value=data['Order_Date'].min()  ,#pd.datetime(2022, 11, 2),
                                max_value=data['Order_Date'].max(),#pd.datetime(2022, 6, 4),
                                format='DD-MM-YYYY')

st.sidebar.markdown("""___""")#linha de separação na sidebar

    #Filtro de tipos de trânsito com multiselect
st.sidebar.markdown('### Selecione o(s) tipo(s) de trânsito')
traffic_options = st.sidebar.multiselect(
                                        'Quais as condicões do trânsito?',
                                        data['Road_traffic_density'].unique(),
                                        default=['Low', 'Medium', 'High', 'Jam'])

st.sidebar.markdown("""___""")#linha de separação na sidebar

st.sidebar.markdown('### Powered by Francisco Costa Carneiro')



##############################################################################################
# Agora vamos fazer a conexão dos filtros com os gráficos expostos no corpo do nosso dashboard
##############################################################################################
#Filtro de Data Limite e Traffic Density
#########################################

#Criando as filtragens e a conexão
#Filtrando
linhas_selecionadas = (data['Order_Date'] < date_slider) & (data['Road_traffic_density'].isin( traffic_options ))
df1 = data.loc[linhas_selecionadas, :]
st.markdown('### Dataframe selecionado no filtro de período de data limite e Tipos de tráfego')


# 2. CORPO DO DASHBOARD
###############################################
#Lembrando que vamos criar a apresentação de acordo com o nosso planejamento realizado no Draw.io (figura: Planejamento do Dashboard no Drawio)

#Primeiramente, vamos criar ABAS dentro do nosso aplicativo(serão 3 tabs):
tab1, tab2, tab3 = st.tabs(['Visão gerencial', 'Visão tática', 'Visão geográfica'])

with tab1: #Ou seja, tudo que estiver identado dentro do with tab 1 ficará dentro da apresentação da Visão gerencial
    st.markdown('### Visão diária')
    #(Linha 1)
    with st.container():#o container é o quadrado onde será apresentada a análise que, nesse caso tem apenas 1 coluna.
        # 1. Quantidade de pedidos por dia
        ###############################################
        df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()

        #Renomeando as colunas
        df_aux.columns = ['order_date', 'qtde_entregas']

        # gráfico de barras
        st.markdown('#### Sazonalidade de entregas por data')
        fig = px.bar( df_aux, x='order_date', y='qtde_entregas' )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""___""")#linha de separação
   
    #(Linha 2)
    with st.container():
        col1, col2 = st.columns( 2 )#declarando que eu quero duas colunas nessa linha
        
         # 2.1. Distribuição de pedidos por tipo de tráfego (linha 2, coluna 1)
        ################################################
        with col1:
            st.markdown('#### Distribuição de pedidos por tipo de tráfego')
            df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
            df_aux['perc_ID'] = 100 * (df_aux['ID'] / df_aux['ID'].sum())
            figpie = px.pie( df_aux, values='perc_ID', names='Road_traffic_density')
            st.plotly_chart(figpie, use_container_width=True)
            st.markdown("""___""")#linha de separação
            
        # 2.2. Comparação de volume de pedido por cidade e tráfego (linha 2, coluna 2)
        ################################################
        with col2:
            st.markdown('#### Comparação de volume por Cidade e tipo de tráfego')
            df_aux = df1.loc[:, ["ID", "City", "Road_traffic_density"]].groupby(["City", "Road_traffic_density"]).count().reset_index()
            fig = px.scatter(df_aux, x="City", y="Road_traffic_density", size="ID", color="City")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""___""")#linha de separação
        
with tab2:
    st.markdown('### Visão semanal')
    st.markdown('#### A quantidade de pedidos por entregador por semana')
    with st.container():
        
        df_aux1 = df1.loc[:, ['ID', 'Week_of_year']].groupby( 'Week_of_year' ).count().reset_index()
        df_aux2 = df1.loc[:, ['Delivery_person_ID', 'Week_of_year']].groupby( 'Week_of_year').nunique().reset_index()
        df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
        df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
        fig = px.line( df_aux, x='Week_of_year', y='order_by_delivery' )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""___""")#linha de separação
        
        
    st.markdown('#### A quantidade de pedidos por semana')
    with st.container():
        
        fig = px.bar( df_aux1, x='Week_of_year', y='ID' )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""___""")#linha de separação
    
with tab3:
    #(Linha 3)
    with st.container():#o container é o quadrado onde será apresentada a análise que, nesse caso tem apenas 1 coluna.
        # 3. A localização central de cada cidade por tipo de tráfego.
        #################################################
        st.markdown('#### Localização central de cada cidade por tipo de tráfego')
        df_aux = df1.loc[:, ["City", "Road_traffic_density", "Delivery_location_latitude", "Delivery_location_longitude"]].groupby(["City", 'Road_traffic_density']).median().reset_index()
        _map = folium.Map()
        
        for index, location_info in df_aux.iterrows():
            folium.Marker([location_info['Delivery_location_latitude'], 
                          location_info['Delivery_location_longitude']], popup=location_info[['City', 'Road_traffic_density']]).add_to(_map)

        folium_static(_map, width=1200 , height= 600)
        
        
        st.markdown("""___""")#linha de separação