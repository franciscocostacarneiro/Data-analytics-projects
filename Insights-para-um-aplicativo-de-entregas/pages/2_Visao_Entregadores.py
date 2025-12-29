#####################################################################
#Aula 47 - Projeto Cury de entregas - Streamlit Visão Entregadores
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
#Config layout expandido
st.set_page_config(page_title='Visão_Entregadores', page_icon='')

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
    #(Linha 1)
    with st.container():# CONTAINER 1 (o container é o quadrado onde será apresentado o conteúdo - LINHA 1)
        # st.markdown('### Métricas')
        col1, col2, col3, col4 = st.columns( 4, gap='large' ) #são as colunas, ou seja, temos como se fosse uma coordenada entre container, coluna e linha. Large é a distância entre as colunas
        with col1:
            maior_idade = df1['Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)    
        
        with col2:
            menor_idade = df1['Delivery_person_Age'].min()
            col2.metric('Menor idade', menor_idade)    
            
        with col3:
            melhor_condicao_veiculo = df1['Vehicle_condition'].max()    
            col3.metric('Melhor cond veículo', melhor_condicao_veiculo)
        
        with col4:
            pior_condicao_veiculo = df1['Vehicle_condition'].min()
            col4.metric('Pior cond veículo', pior_condicao_veiculo)
            
    st.markdown("""___""")#linha de separação na sidebar            
            
    #Linha 2
    with st.container():# CONTAINER 2 (o container é o quadrado onde será apresentado o conteúdo - LINHA 2)
        st.markdown('### Avaliações médias')
        st.markdown("""___""")#linha de separação na sidebar
        col1, col2 = st.columns( 2 , gap='large' ) #são as colunas, ou seja, temos como se fosse uma coordenada entre container, coluna e linha. Large é a distância entre as colunas
        with col1:
            st.write('###### Avaliação média por entregador')
            st.markdown("""___""")#linha de separação na sidebar
            
            avaliacao_media_entregador = pd.DataFrame(df1.groupby('Delivery_person_ID')['Delivery_person_Ratings'].mean().sort_values(ascending=False).reset_index())
            st.dataframe(avaliacao_media_entregador)
            
        with col2:
            st.write('###### Avaliação média por trânsito')
            
            # st.markdown("""___""")#linha de separação na sidebar            
            df_mean = pd.DataFrame(df1.groupby('Road_traffic_density')['Delivery_person_Ratings'].mean())
            df_std = pd.DataFrame(df1.groupby('Road_traffic_density')['Delivery_person_Ratings'].std())

            df_inner = pd.merge(df_mean, df_std, on='Road_traffic_density', how='inner')
            df_inner.columns = ['Rating médio', 'Desvio padrão']
            st.dataframe(df_inner)
            
            
            # st.markdown("""___""")#linha de separação na sidebar
            
            
            st.write('###### Avaliação média por clima')
            # st.markdown("""___""")#linha de separação na sidebar
         
            df_mean = pd.DataFrame(df1.groupby('Weatherconditions')['Delivery_person_Ratings'].mean())
            df_std = pd.DataFrame(df1.groupby('Weatherconditions')['Delivery_person_Ratings'].std())

            df_inner = pd.merge(df_mean, df_std, on='Weatherconditions', how='inner')
            df_inner.columns = ['Rating médio', 'Desvio padrão']
            st.dataframe(df_inner)
                
            
    st.markdown("""___""")#linha de separação na sidebar         
     
    #Linha 3       
    with st.container():# CONTAINER 3 (o container é o quadrado onde será apresentado o conteúdo - lINHA 3)
        st.markdown('### Top entregadores')
        st.markdown("""___""")#linha de separação na sidebar
        col1, col2 = st.columns( 2, gap='large' ) #são as colunas, ou seja, temos como se fosse uma coordenada entre container, coluna e linha. Large é a distância entre as colunas
        
        with col1:
            st.write('###### 10 entregadores mais rápidos - por cidade')
            st.markdown("""___""")#linha de separação na sidebar
            
            df_aux = pd.DataFrame(df1.groupby(['City', 'Delivery_person_ID'])['Time_taken(min)'].min()).reset_index()

            metropoli = df_aux.loc[df_aux['City'] == 'Metropolitian', :].sort_values('Time_taken(min)', ascending=True).reset_index().head(10)

            urba = df_aux.loc[df_aux['City'] == 'Urban', :].sort_values('Time_taken(min)', ascending=True).reset_index().head(10)

            semi_ur = df_aux.loc[df_aux['City'] == 'Semi-Urban', :].sort_values('Time_taken(min)', ascending=True).reset_index().head(10)

            city_concat = pd.concat([metropoli, urba, semi_ur], axis=0).reset_index(drop=True)
            city_concat2 = city_concat.drop('index', axis=1)
            st.dataframe(city_concat2)
            
            
        with col2:
            st.write('###### 10 entregadores mais lentos - por cidade')
            st.markdown("""___""")#linha de separação na sidebar    

            df_aux = pd.DataFrame(df1.groupby(['City', 'Delivery_person_ID'])['Time_taken(min)'].max()).reset_index()

            metropoli = df_aux.loc[df_aux['City'] == 'Metropolitian', :].sort_values('Time_taken(min)', ascending=False).reset_index().head(10)

            urba = df_aux.loc[df_aux['City'] == 'Urban', :].sort_values('Time_taken(min)', ascending=False).reset_index().head(10)

            semi_ur = df_aux.loc[df_aux['City'] == 'Semi-Urban', :].sort_values('Time_taken(min)', ascending=False).reset_index().head(10)

            city_concat = pd.concat([metropoli, urba, semi_ur], axis=0)
            city_concat2 = city_concat.drop('index', axis=1)
            st.dataframe(city_concat2)
                
                
#         st.markdown("""___""")#linha de separação