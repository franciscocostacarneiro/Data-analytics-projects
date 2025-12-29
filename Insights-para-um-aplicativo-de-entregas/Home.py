import streamlit as st
from PIL import Image

st.set_page_config(page_title='Home', page_icon='', layout='wide')

image_path = 'Delivery_food.png'
image = Image.open(image_path)
st.sidebar.image(image, width=300)
st.markdown("""___""")


 #Cabeçalho
st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""___""")#linha de separação na sidebar

st.write('# Cury Company Growth Dashboard')

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos entregadores e restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - ##### Visão Empresa:
        - Visão gerencial: Métricas gerais de comportamento;
        - Visão tática: Indicadores semanais de crescimento; e
        - Visão geográfica: Insights de geolocalização.
                    
    
    - ##### Visão Entregador:
        - Acompanhamento dos indicadoores semanais de crescimento.
    
    
    - ##### Visão Restaurantes:
        - Indicadores semanais de crescimento dos restaurantes
    
    ### Ask for help
    ###### Francisco Costa Carneiro
    - Linked In: https://www.linkedin.com/in/francisco-costa-carneiro-374b7227/
""")

