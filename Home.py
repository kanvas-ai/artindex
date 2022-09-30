import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title('Kanvas.AI Art Index')

st.header('Estonian Auctions - Map of Art Market')

df = pd.read_csv('data/auctions_clean.csv')
df_hist = pd.read_csv('data/historical_avg_price.csv')
st.subheader('Is art getting more expensive? The relationship between the average price of an art work and year')
fig = px.area(df_hist, x="date", y="avg_price", color="src")
st.plotly_chart(fig, use_container_width=True)

# price inception by category
st.subheader('What is the average return of investment for art categories? Average total and annual return per category')
end_year = 2021
category_returns = []
for cat in df["category"].unique():
    df_cat = df[df["category"]==cat]
    
    start_year = df_cat["date"].min()
    start_sum = df_cat.loc[df_cat["date"] == start_year, "end_price"].mean()
    end_sum = df_cat.loc[df_cat["date"] == end_year, "end_price"].mean()
    
    total_return = round((end_sum - start_sum) / start_sum * 100, 2)
    annual_return = round(total_return / (end_year - start_year), 2)
    category_returns.append([cat, total_return, annual_return])
df_cat_returns = pd.DataFrame(category_returns, columns=["Category", "Total Return %", "Annual Return %"]) 
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df_cat_returns.columns),
                fill_color='black',
                align='left'),
    cells=dict(values=df_cat_returns.transpose().values.tolist(),
               fill_color='#262730',
               align='left'))
])
# remove space between texts
fig.update_layout(height=200, margin=dict(r=5, l=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)

st.subheader('Is the art market growing in volume? The relationship between the volume of sold art works sold and year')
fig = px.area(df_hist, x="date", y="volume", color="src")
st.plotly_chart(fig, use_container_width=True)

# price inception by category
st.subheader('What is the total volume change for art categories? Volume total and annual change per category')
end_year = 2021
category_returns = []
for cat in df["category"].unique():
    df_cat = df[df["category"]==cat]
    
    start_year = df_cat["date"].min()
    start_sum = df_cat.loc[df_cat["date"] == start_year, "end_price"].sum()
    end_sum = df_cat.loc[df_cat["date"] == end_year, "end_price"].sum()
    
    total_return = round((end_sum - start_sum) / start_sum * 100, 2)
    annual_return = round(total_return / (end_year - start_year), 2)
    category_returns.append([cat, total_return, annual_return])
df_cat_returns = pd.DataFrame(category_returns, columns=["Category", "Total Return %", "Annual Return %"]) 
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df_cat_returns.columns),
                fill_color='black',
                align='left'),
    cells=dict(values=df_cat_returns.transpose().values.tolist(),
               fill_color='#262730',
               align='left'))
])
# remove space between texts
fig.update_layout(height=200, margin=dict(r=5, l=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)

st.subheader('Who are the best selling artists? Total art auction sales by overbidding percentage')

df['overbid_%'] = (df['end_price'] - df['start_price'])/df['start_price'] * 100
df['art_work_age'] = df['date'] - df['year']
df2 = df.groupby(['author', 'technique', 'category']).agg({'end_price':['sum'], 'overbid_%':['mean']})
df2.columns = ['total_sales', 'overbid_%']
df2 = df2.reset_index()

fig = px.treemap(df2, path=['category', 'technique', 'author'], values='total_sales',
                  color='overbid_%', hover_data=['author'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df2['overbid_%'], weights=df2['total_sales']),
                  range_color = (0, df['overbid_%'].mean() + df['overbid_%'].std()))

st.plotly_chart(fig, use_container_width=True)

# price inception by author
st.subheader('What is the average return of investment for 10 highest selling authors? Average total and annual return for top 10 authors')
author_returns = []
author_sum = df.groupby(["author"], sort=False)["end_price"].sum()
top_authors = author_sum.sort_values(ascending=False)[:10]
for author in top_authors.index:
    df_aut = df[df["author"] == author]
    start_year = df_aut["date"].min()
    end_year = df_aut["date"].max()
    
    start_sum = df_aut.loc[df_aut["date"] == start_year, "end_price"].mean()
    end_sum = df_aut.loc[df_aut["date"] == end_year, "end_price"].mean()
    
    total_return = round((end_sum - start_sum) / start_sum * 100, 2)
    annual_return = round(total_return / (end_year - start_year + 1), 2)
    author_returns.append([author, total_return, annual_return])
df_author_returns = pd.DataFrame(author_returns, columns=["Category", "Total Return %", "Annual Return %"])    
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df_author_returns.columns),
                fill_color='black',
                align='left'),
    cells=dict(values=df_author_returns.transpose().values.tolist(),
               fill_color='#262730',
               align='left'))
])
# remove space between texts
fig.update_layout(height=200, margin=dict(r=5, l=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)

# price inception by author
st.subheader('What is the total volume change for 10 highest selling authors? Volume total and annual change for top 10 authors')
author_returns = []
author_sum = df.groupby(["author"], sort=False)["end_price"].sum()
top_authors = author_sum.sort_values(ascending=False)[:10]
for author in top_authors.index:
    df_aut = df[df["author"] == author]
    start_year = df_aut["date"].min()
    end_year = df_aut["date"].max()
    
    start_sum = df_aut.loc[df_aut["date"] == start_year, "end_price"].sum()
    end_sum = df_aut.loc[df_aut["date"] == end_year, "end_price"].sum()
    
    total_return = round((end_sum - start_sum) / start_sum * 100, 2)
    annual_return = round(total_return / (end_year - start_year + 1), 2)
    author_returns.append([author, total_return, annual_return])
df_author_returns = pd.DataFrame(author_returns, columns=["Category", "Total Return %", "Annual Return %"])    
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df_author_returns.columns),
                fill_color='black',
                align='left'),
    cells=dict(values=df_author_returns.transpose().values.tolist(),
               fill_color='#262730',
               align='left'))
])
# remove space between texts
fig.update_layout(height=200, margin=dict(r=5, l=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)

st.subheader('Is older art more expensive? The relationship between the age of the art work and price')

df = df.dropna(subset=["decade"])
fig = px.scatter(df, x="art_work_age", y="end_price", color="category",
                 size='decade', hover_data=['author'])

st.plotly_chart(fig, use_container_width=True)

st.subheader('Are larger art works more expensive? The relationship between the dimensions of an art work and its price')

df = df.dropna(subset=["dimension"])
fig = px.scatter(df, x="dimension", y="end_price", color="category",
                 size='dimension', hover_data=['author'])

st.plotly_chart(fig, use_container_width=True)

st.text('Copyright Kanvas.ai')
st.text('Authors: Markus Sulg, Julian Kaljuvee')
st.text('Source: Estonian auctions (2020-2022)')
