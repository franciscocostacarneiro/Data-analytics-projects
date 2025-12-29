import streamlit as st

# Configurando a página do Streamlit
def main():
    # st.title('Modelo de Predição e Visualização - IPEA')

    st.markdown("""
    ## Modelo de Predição e Visualização - IPEA
    
    A aplicação conta com o seguinte fluxo:
    """)

    st.image("https://github.com/nodesource/distributions/assets/43751101/05c8550a-b6e6-478c-81a8-4c5f869f77c7")

    st.markdown("""
    Primeiro é realizado o carregamento dos dados via WebScraping, em seguida os dados são armazenados em um dataframe
    Pandas possibilitando a aplicação dos modelos de Time Series. 
    
    A aplicação oferece a capacidade de aplicar dois modelos distintos: LTSM ou Prophet. Ao escolher um modelo, os dados 
    são registrados em um dataframe de saída, que posteriormente será utilizado para criar as visualizações dos dados.
    
    ### Instruções de Execução
    
    Primeiro é necessário executar toda a pagina "Model", nela será carregado o Dataframe e em seguida será aplicado o modelo
    de Machine Learning escolhido pelo usuário.
    Para executar a pagina basta clicar nos seguintes botoes:
    - Busca dos dados;
    - Seleção e Configuração do modelo;
    - Execução do modelo;
    - Analise dos Dados e Metricas Retornadas.
    
    Após completar o fluxo de coleta dos dados, a pagina "Data Visualization" ficará disponivel para execução. 
    Basta clicar no botão "Carregar Graficos" e todas as visualizações serão carregadas com base nos dados coletados.
    """)

# Executando a aplicação
if __name__ == "__main__":
    main()