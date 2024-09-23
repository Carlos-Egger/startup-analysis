import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static

# Carregar o dataset
df = pd.read_csv(r'C:\Users\chase\OneDrive\Desktop\lapes\startup data.csv')

# Tratamentos de dados
# Renomear colunas
df.columns = ['Unnamed', 'state_code', 'latitude', 'longitude', 'zip_code', 'id', 'city', 'Unnamed_6', 
              'name', 'labels', 'founded_at', 'closed_at', 'first_funding_at', 'last_funding_at', 
              'age_first_funding_year', 'age_last_funding_year', 'age_first_milestone_year', 
              'age_last_milestone_year', 'relationships', 'funding_rounds', 'funding_total_usd', 
              'milestones', 'state_code_1', 'is_CA', 'is_NY', 'is_MA', 'is_TX', 'is_otherstate', 
              'category_code', 'is_software', 'is_web', 'is_mobile', 'is_enterprise', 
              'is_advertising', 'is_gamesvideo', 'is_ecommerce', 'is_biotech', 'is_consulting', 
              'is_othercategory', 'object_id', 'has_VC', 'has_angel', 'has_roundA', 
              'has_roundB', 'has_roundC', 'has_roundD', 'avg_participants', 'is_top500', 'status']

# Tratar valores ausentes
df.dropna(subset=['name', 'city'], inplace=True)  # Excluir linhas sem nome ou cidade
df.fillna(0, inplace=True)  # Preencher outros NaN com 0, se apropriado

# Converter tipos de dados
df['founded_at'] = pd.to_datetime(df['founded_at'], errors='coerce')  # Converter para datetime
df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'], errors='coerce')  # Converter para numérico

# Remover colunas desnecessárias
df.drop(columns=['Unnamed', 'Unnamed_6', 'state_code_1'], inplace=True)

# Título do app
st.title('Análise de Startups nos EUA')

# Mostrar a tabela de dados (opcional)
st.write("Visualização inicial dos dados:")
st.write(df.head())

# 1. Distribuição Geográfica das Empresas
st.subheader('Distribuição Geográfica das Empresas')

# Criar um mapa centrado nos EUA
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Adicionar pontos para cada empresa com base em sua latitude e longitude
for index, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)

# Renderizar o mapa no Streamlit
folium_static(m)

# 2. Idade das Empresas até o Primeiro Financiamento
st.subheader('Idade das Empresas até o Primeiro Financiamento')
df_age_first_funding = df[['age_first_funding_year']].dropna()
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df_age_first_funding['age_first_funding_year'], bins=20, kde=True, ax=ax)
plt.title('Distribuição da Idade das Empresas até o Primeiro Financiamento')
plt.xlabel('Anos até o Primeiro Financiamento')
plt.ylabel('Número de Empresas')
st.pyplot(fig)

# 3. Status das Empresas
st.subheader('Status das Empresas')
df_status_distribution = df['status'].value_counts().reset_index()
df_status_distribution.columns = ['status', 'count']
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='status', y='count', data=df_status_distribution, ax=ax)
plt.title('Status das Empresas (Ativa ou Fechada)')
plt.xlabel('Status')
plt.ylabel('Número de Empresas')
st.pyplot(fig)

# 4. Total de Financiamento Arrecadado
st.subheader('Distribuição do Total de Financiamento Arrecadado')
df_funding_total = df[['funding_total_usd']].dropna()
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df_funding_total['funding_total_usd'], bins=20, kde=True, ax=ax)
plt.title('Distribuição do Total de Financiamento Arrecadado')
plt.xlabel('Financiamento Total (USD)')
plt.ylabel('Número de Empresas')
st.pyplot(fig)

# 5. Distribuição por Categorias
st.subheader('Distribuição por Categorias de Empresas')
df_categories = df['category_code'].value_counts().reset_index()
df_categories.columns = ['category_code', 'count']
total_count = df_categories['count'].sum()
df_categories['percentage'] = df_categories['count'] / total_count * 100
df_categories.loc[df_categories['percentage'] < 2, 'category_code'] = 'Outros'
df_categories = df_categories.groupby('category_code').sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 8))
plt.pie(df_categories['count'], labels=df_categories['category_code'], autopct='%1.1f%%', startangle=140)
plt.title('Distribuição por Categorias de Empresas')
st.pyplot(fig)

# 6. Relacionamentos de Parcerias
st.subheader('Distribuição de Relacionamentos de Parcerias')
df_relationships = df[['relationships']].dropna()
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df_relationships['relationships'], bins=20, kde=True, ax=ax)
plt.title('Distribuição de Relacionamentos de Parcerias')
plt.xlabel('Número de Relacionamentos')
plt.ylabel('Número de Empresas')
st.pyplot(fig)

# 7. Participação em Financiamentos
st.subheader('Distribuição da Participação Média nas Rodadas de Financiamento')
df_avg_participants = df[['avg_participants']].dropna()
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(df_avg_participants['avg_participants'], bins=20, kde=True, ax=ax)
plt.title('Distribuição da Participação Média nas Rodadas de Financiamento')
plt.xlabel('Participantes Médios')
plt.ylabel('Número de Empresas')
st.pyplot(fig)

# 8. Distribuição por Estados Específicos
st.subheader('Distribuição por Estados Específicos')
states_columns = ['is_CA', 'is_NY', 'is_MA', 'is_TX', 'is_otherstate']
state_names = ['CA', 'NY', 'MA', 'TX', 'Other']
df_states_distribution = pd.DataFrame({'state': state_names, 'count': df[states_columns].sum()})

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='state', y='count', data=df_states_distribution, ax=ax)
plt.title('Distribuição de Empresas por Estados Específicos')
plt.xlabel('Estado')
plt.ylabel('Número de Empresas')
st.pyplot(fig)
