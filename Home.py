import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.image("https://d1muf25xaso8hp.cloudfront.net/https%3A%2F%2Fs3.amazonaws.com%2Fappforest_uf%2Ff1609072752424x654841387818197400%2Fhorisontal%2520%25E2%2580%2593%2520koopia.jpg?w=256&h=45&auto=compress&fit=crop&dpr=1.25")
st.title('Art Index (2001 - 2021)')

st.header('Estonian Auctions - Map of Art Market')

df = pd.read_csv('data/auctions_clean.csv')
df = df[df["date"] >= 2001]
df_hist = pd.read_csv('data/historical_avg_price.csv')
df_hist = df_hist[df_hist["date"] >= 2001]
df_hist = df_hist.groupby("date").sum()
st.subheader('Figure - Historical Price Performance')

fig = px.area(df_hist, x=df_hist.index, y="avg_price",
              labels={
                 "avg_price": "Average Price (€)",
                 "date": "Auction Year",
             })
st.plotly_chart(fig, use_container_width=True)

# price inception by category
st.subheader('Table - Historical Price Performance')
category_returns = []
for cat in df["category"].unique():
    df_cat = df[df["category"]==cat]
    
    start_year = df_cat["date"].min()
    end_year = df_cat["date"].max()
    start_sum = df_cat.loc[df_cat["date"] == start_year, "end_price"].mean()
    end_sum = df_cat.loc[df_cat["date"] == end_year, "end_price"].mean()
    
    total_return = round((end_sum - start_sum) / start_sum * 100, 2)
    annual_return = round(total_return / (end_year - start_year), 2)
    category_returns.append([cat, total_return, annual_return])
df_cat_returns = pd.DataFrame(category_returns, columns=["Category", "Total Return (%)", "Annual Return (%)"]) 
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df_cat_returns.columns),
                align='left'),
    cells=dict(values=df_cat_returns.transpose().values.tolist(),
               align='left'))
])
# remove space between texts
fig.update_layout(height=150, margin=dict(r=5, l=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)

st.subheader('Figure - Historical Volume Growth')
fig = px.area(df_hist, x=df_hist.index, y="volume", 
             labels={
                 "volume": "Volume (€)",
                 "date": "Auction Year",
             })
st.plotly_chart(fig, use_container_width=True)

# price inception by category
st.subheader('Table - Historical Volume Growth')
category_returns = []
for cat in df["category"].unique():
    df_cat = df[df["category"]==cat]
    
    start_year = df_cat["date"].min()  
    end_year = df_cat["date"].max()
    start_sum = df_cat.loc[df_cat["date"] == start_year, "end_price"].sum()
    end_sum = df_cat.loc[df_cat["date"] == end_year, "end_price"].sum()
    
    total_return = round((end_sum - start_sum) / start_sum * 100, 2)
    annual_return = round(total_return / (end_year - start_year), 2)
    category_returns.append([cat, total_return, annual_return])
df_cat_returns = pd.DataFrame(category_returns, columns=["Category", "Total Return (%)", "Annual Return (%)"]) 
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df_cat_returns.columns),
                align='left'),
    cells=dict(values=df_cat_returns.transpose().values.tolist(),
               align='left'))
])
# remove space between texts
fig.update_layout(height=150, margin=dict(r=5, l=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)

st.subheader('Figure - Art Sales by Category and Artist')

df['start_price'] = df['start_price'].fillna(df['end_price'])
df['overbid_%'] = (df['end_price'] - df['start_price'])/df['start_price'] * 100
df['art_work_age'] = df['date'] - df['year']
df2 = df.groupby(['author', 'technique', 'category']).agg({'end_price':['sum'], 'overbid_%':['mean']})
df2.columns = ['total_sales', 'overbid_%']
df2 = df2.reset_index()

fig = px.treemap(df2, path=[px.Constant("Categories"), 'category', 'technique', 'author'], values='total_sales',
                  color='overbid_%',
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(df2['overbid_%'], weights=df2['total_sales']),
                  range_color = (0, df['overbid_%'].mean() + df['overbid_%'].std()),
                  labels={
                     "overbid_%": "Overbid (%)",
                     "total_sales": "Total Sales",
                     "author": "Author",
                  })
fig.update_traces(hovertemplate='<b>%{label} </b> <br> Total Sales: %{value}<br> Overbid (%): %{color:.2f}',)
st.plotly_chart(fig, use_container_width=True)

# price inception by author
st.subheader('Table - Top Ten Best Performing Artists')
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
df_author_returns = pd.DataFrame(author_returns, columns=["Author", "Total Return (%)", "Annual Return (%)"])    
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df_author_returns.columns),
                align='left'),
    cells=dict(values=df_author_returns.transpose().values.tolist(),
               align='left'))
])
# remove space between texts
fig.update_layout(height=250, margin=dict(r=5, l=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)

# price inception by author
st.subheader('Table - Volume Growth for Top Ten Artists')
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
df_author_returns = pd.DataFrame(author_returns, columns=["Author", "Total Return (%)", "Annual Return (%)"])    
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df_author_returns.columns),
                align='left'),
    cells=dict(values=df_author_returns.transpose().values.tolist(),
               align='left'))
])
# remove space between texts
fig.update_layout(height=250, margin=dict(r=5, l=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)

st.subheader('Figure - Age of Art Work vs Price')

df = df.dropna(subset=["decade"])
fig = px.scatter(df, x="art_work_age", y="end_price", color="category",
                 size='decade', hover_data=['author'],
                 labels={
                     "end_price": "End Price (€)",
                     "art_work_age": "Art Work Age",
                     "author": "Author",
                     "category": "Category",
                     "decade": "Decade"
                  })

st.plotly_chart(fig, use_container_width=True)

st.subheader('Figure - Size of Art Work vs Price')

df = df.dropna(subset=["dimension"])
fig = px.scatter(df, x="dimension", y="end_price", color="category",
                 size='dimension', hover_data=['author'],
                 labels={
                     "end_price": "End Price (€)",
                     "dimension": "Dimension (cm x cm)",
                     "author": "Author",
                     "category": "Category",
                  })

st.plotly_chart(fig, use_container_width=True)

st.text('Copyright: Kanvas.ai')
st.text('Authors: Astid Laupmaa, Julian Kaljuvee, Markus Sulg')
st.text('Source: Estonian auctions (2001 - 2021)')
