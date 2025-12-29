#####################################################################
#Aula 47 - Projeto Cury de entregas - Streamlit Visão Restaurante
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
import plotly.graph_objects as go
from matplotlib import pyplot as plt
import folium
from streamlit_folium import folium_static
from haversine import haversine
import streamlit as st
from PIL import Image#para a logo utilizada - biblioteca de m anipulação de imagens

############################################
#Helper functions
############################################

#Config layout expandido
st.set_page_config(page_title='Visão_Restaurantes', page_icon='', layout='wide')

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
st.header('Marketplace - Visão Entregadores')

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


# 2. CORPO DO DASHBOARD
###############################################
#Lembrando que vamos criar a apresentação de acordo com o nosso planejamento realizado no Draw.io (figura: Planejamento do Dashboard - Visão Entregadores)

#Primeiramente, vamos criar ABAS dentro do nosso aplicativo(serão 3 tabs):
tab1, tab2, tab3 = st.tabs(['Visão gerencial', '-', '-'])
        
with tab1: #Ou seja, tudo que estiver identado dentro do with tab 1 ficará dentro da apresentação da Visão gerencial
    st.markdown('### Métricas')
    st.markdown("""___""")#linha de separação na sidebar
    
    #(Linha 1)#############################################################################################################################################
    with st.container():# CONTAINER 1 (o container é o quadrado onde será apresentado o conteúdo - LINHA 1)
        # st.markdown('### Métricas')
        col1, col2, col3, col4, col5, col6 = st.columns( 6 ) #são as colunas, ou seja, temos como se fosse uma coordenada entre container, coluna e linha. Large é a distância entre as colunas
        with col1:
            entregadores_unicos = np.round(data['Delivery_person_ID'].nunique(),2)
            col1.metric('Entregadores únicos', entregadores_unicos)    
        
        with col2:
            cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

            df1['Delivery_distance'] = df1.loc[:, cols].apply( lambda x: haversine(
                                                                        (x['Restaurant_latitude'], 
                                                                         x['Restaurant_longitude']),
                                                                        (x['Delivery_location_latitude'],                                                                                                                                                                    x['Delivery_location_longitude'])), axis=1)
            
            distancia_media = np.round(df1['Delivery_distance'].mean(),2)
            col2.metric('Distância média', distancia_media)    
            
        with col3:
            linhas = data.loc[data['Festival'] == 'Yes', 'Festival']
            tempo_entrega_festival = np.round(data.groupby(linhas)['Time_taken(min)'].mean(),2)
            col3.metric('Entr.c/festival', tempo_entrega_festival)
        
        with col4:
            linhas = data.loc[data['Festival'] == 'Yes', 'Festival']
            std_entrega_festival = np.round(data.groupby(linhas)['Time_taken(min)'].std(),2)
            col4.metric('Std méd festival', std_entrega_festival)
            
        with col5:
            linhas = data.loc[data['Festival'] == 'No', 'Festival']
            tempo_entrega_s_festival = np.round(data.groupby(linhas)['Time_taken(min)'].mean(),2)
            col5.metric('Entr.méd.s/festival', tempo_entrega_s_festival)
            
        with col6:
            linhas = data.loc[data['Festival'] == 'No', 'Festival']
            std_entrega_s_festival = np.round(data.groupby(linhas)['Time_taken(min)'].std(),2)
            col6.metric('Std méd s/festival', std_entrega_s_festival)
            
            
    st.markdown("""___""")#linha de separação na sidebar            
            
    #(Linha 2)#############################################################################################################################################
    with st.container():# CONTAINER 2 (o container é o quadrado onde será apresentado o conteúdo - LINHA 1)
        # st.markdown('### Métricas')
        st.markdown('##### Distribuição da distância média por cidade')
        cols = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

        df1['Delivery_distance'] = df1.loc[:, cols].apply( lambda x: haversine(
                                                                        (x['Restaurant_latitude'], 
                                                                         x['Restaurant_longitude']),
                                                                        (x['Delivery_location_latitude'],                                                                                                                                                                    x['Delivery_location_longitude'])), axis=1)
            
        distancia_media = np.round(df1.loc[:,['City','Delivery_distance']].groupby('City').mean().reset_index(),2)
        
        fig = go.Figure(data=[go.Pie(labels=distancia_media['City'], values=distancia_media['Delivery_distance'], pull=[0.05, 0.05, 0.05])])#o pull é quanto vamos puxar do gráfico para ficTempo médio por tipo de entregaizza
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""___""")#linha de separação na sidebar   
    
    #(Linha 3)#############################################################################################################################################
    with st.container():# CONTAINER 3 (o container é o quadrado onde será apresentado o conteúdo - LINHA 1)
        # st.markdown('### Métricas')
        col1, col2 = st.columns( 2, gap='large' ) #são as colunas, ou seja, temos como se fosse uma coordenada entre container, coluna e linha. Large é a distância entre as colunas
        
        with col1:
            st.markdown('##### Distribuição do tempo por cidade')
            df_aux = df1.loc[:, ['City','Time_taken(min)']].groupby('City').agg({'Time_taken(min)':['mean','std']})
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            
            fig = go.Figure()
            fig.add_trace( go.Bar( name='Control', x = df_aux['City'], y = df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time'])))
            fig.update_layout(barmode='group')
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""___""")#linha de separação na sidebar  
                
        with col2:
            st.markdown('##### Tempo médio por Cidade e Tipo de trânsito')
            df_aux = (df1.loc[:, ['City','Time_taken(min)', 'Road_traffic_density']]
                        .groupby(['City', 'Road_traffic_density'])
                        .agg({'Time_taken(min)':['mean','std']}))
            
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
                        
            fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='avg_time', 
                              color='std_time', color_continuous_scale='RdBu',
                              color_continuous_midpoint=np.average(df_aux['std_time']))
            st.plotly_chart(fig, use_container_width=True)
            
            
            st.markdown("""___""")#linha de separação na sidebar  
    #(Linha 4)#############################################################################################################################################
    with st.container():# CONTAINER 4 (o container é o quadrado onde será apresentado o conteúdo - LINHA 1)
        st.markdown('##### O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego')
        mean = pd.DataFrame(data.groupby(['City', 'Road_traffic_density'])['Time_taken(min)'].mean())
        std = pd.DataFrame(data.groupby(['City', 'Road_traffic_density'])['Time_taken(min)'].std())

        merge = pd.merge(mean, std, on=['City', 'Road_traffic_density'], how='inner')
        merge.columns=['Tempo médio', 'Desvio padrão']
        st.dataframe(merge)
        
        