import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração inicial
st.title("Analysis of Alcohol Consumption and Liver Health")
st.write("""
This work explores the relationship between alcohol consumption and liver function, 
focusing on how drinking habits influence key biomarkers like Gamma-Glutamyl Transpeptidase (GGT). 
By analyzing these patterns, the study aims to provide insights into the potential impact of alcohol on liver function.
""")

# Carregar dados
@st.cache_data
def load_data():
    # Carrega apenas as primeiras 6 colunas
    df = pd.read_csv('bupa.data', header=None, usecols=[0, 1, 2, 3, 4, 5])
    df.columns = ['MCV', 'FA', 'TGP', 'TGO', 'GGT', 'Drinks']
    return df

data = load_data()

# Mostrar os dados brutos (opcional)
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.write(data)

# Estatísticas descritivas para Drinks
st.subheader("Summary Statistics")
with st.expander("Show Table 1: Daily Alcohol Consumption (Drinks)"):
    st.write("""
    This table provides descriptive statistics for daily alcohol consumption, measured in half-pint equivalents.
    """)
    drinks_summary = data['Drinks'].describe().to_frame().transpose()
    st.write(drinks_summary)

with st.expander("Show Table 2: Gamma-Glutamyl Transpeptidase (GGT)"):
    st.write("""
    This table summarizes the GGT levels in the sample. The average GGT level is 38.28, 
    with a standard deviation of 39.25.
    """)
    ggt_summary = data['GGT'].describe().to_frame().transpose()
    st.write(ggt_summary)

# Gráfico 1: Distribuição do consumo de álcool
with st.expander("Show Histogram and Density Curve of Drinks"):
    st.write("""
    This figure presents a histogram and density curve illustrating the distribution of daily alcohol consumption.
    """)
    fig1, ax1 = plt.subplots()
    sns.histplot(data=data, x='Drinks', stat="density", kde=True, color='skyblue', ax=ax1)
    plt.title("Density Curve and Histogram of Drinks")
    st.pyplot(fig1)

# Gráfico 2: Distribuição dos níveis de GGT
with st.expander("Show Histogram and Density Curve of GGT Levels"):
    st.write("""
    This figure depicts a histogram and density curve for GGT levels.
    """)
    fig2, ax2 = plt.subplots()
    sns.histplot(data=data, x='GGT', stat="density", kde=True, color='salmon', ax=ax2)
    plt.title("Density Curve and Histogram of GGT Levels")
    st.pyplot(fig2)

# Gráfico 3: Relação entre Drinks e GGT (exibido diretamente)
st.subheader("Relationship Between Alcohol Consumption and Mean GGT Levels")
st.write("""
This scatter plot with a fitted linear regression line shows the relationship between daily alcohol consumption 
and average GGT levels. The plot indicates a positive correlation, suggesting that higher alcohol consumption 
is associated with increased mean GGT levels.
""")
data_mean = data.groupby('Drinks')['GGT'].mean().reset_index()
fig3, ax3 = plt.subplots()
sns.regplot(x='Drinks', y='GGT', data=data_mean, scatter_kws={'alpha':0.5}, ax=ax3)
plt.title("Relationship Between Alcohol Consumption and Mean GGT Levels")
st.pyplot(fig3)

# Gráfico 4: Associação entre Drinks e GGT (exibido diretamente)
st.subheader("Density and Association Between Alcohol Consumption and GGT Levels")
st.write("""
This joint plot illustrates the association between daily alcohol consumption and GGT levels 
using density contours and marginal density plots.
""")
fig4 = sns.jointplot(x='Drinks', y='GGT', data=data, kind='kde', fill=True, cmap='Blues')
fig4.fig.suptitle("Density and Association Between Drinks and GGT", y=1.02)
st.pyplot(fig4.fig)

# Conclusão
st.subheader("Conclusion")
st.write("""
The analysis reveals a clear positive correlation between alcohol consumption and GGT levels, 
a key biomarker for liver function. Individuals with higher daily alcohol intake tend to have elevated GGT levels, 
suggesting potential liver stress or early signs of dysfunction.

These findings emphasize the importance of monitoring liver health in individuals with increased alcohol consumption 
to enable timely intervention and prevent long-term complications.
""")
