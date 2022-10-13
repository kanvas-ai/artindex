import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import base64

# Table config - inject CSS to hide row indexes
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)

@st.cache(ttl=60*60*24*7, max_entries=300)
def read_df(path:str):
    return pd.read_csv(path)


@st.cache(ttl=60*60*24*7, max_entries=300)
def create_table(df, category_column:str, category_list:list, use_price_sum:bool, table_height:int):
    category_returns = []
    for cat in category_list:
        df_cat = df[df[category_column]==cat]

        start_year = df_cat["date"].min()
        end_year = df_cat["date"].max()
        
        start_sum = 0
        end_sum = 0
        if use_price_sum:               
            start_sum = df_cat.loc[df_cat["date"] == start_year, "end_price"].sum()
            end_sum = df_cat.loc[df_cat["date"] == end_year, "end_price"].sum()
        else:    
            start_sum = df_cat.loc[df_cat["date"] == start_year, "end_price"].mean()
            end_sum = df_cat.loc[df_cat["date"] == end_year, "end_price"].mean()        
        
        total_return = round((end_sum - start_sum) / start_sum * 100, 4)
        annual_return = round(total_return / (end_year - start_year), 4)
        category_returns.append([cat, total_return, annual_return])
        
    df_cat_returns = pd.DataFrame(category_returns, columns=[category_column.capitalize(), "Total Growth since Inception (%)", "Annual Growth Rate (%)"]) 
    df_cat_returns = df_cat_returns.sort_values(by="Total Growth since Inception (%)", ascending=False)
    return df_cat_returns

df = read_df('data/auctions_clean.csv')
df = df[df["date"] >= 2001]
df_hist = read_df('data/historical_avg_price.csv')
df_hist = df_hist[df_hist["date"] >= 2001]
df_hist = df_hist.groupby("date").sum()

# LOGO
# https://discuss.streamlit.io/t/href-on-image/9693/4
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url, max_width):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" style="max-width:{max_width};width:100%" />
        </a>'''
    return html_code


kanvas_logo = get_img_with_href('data/horisontal-BLACK.png', 'https://kanvas.ai', '200px')
st.sidebar.markdown(kanvas_logo, unsafe_allow_html=True)

kanvas_logo = get_img_with_href('data/horisontal-BLACK.png', 'https://kanvas.ai', '400px')
st.markdown(kanvas_logo, unsafe_allow_html=True)

# TITLE
st.title('Estonian Art Index')
st.header('Overview')
st.markdown('''<span style="word-wrap:break-word;">
Kanvas.ai Art Index is a tool for art investors.

Kanvas.ai's art index is a database created based on Estonian art auction sales \nhistory of the last 20 years (2001-2021), with an aim of making art and investing \nin art easier to understand for anyone interested.

The data has been collected based on the results of the public auctions of the \nmain galleries in Estonia, which provides an overview of how the art market \nbehaves over time and which art mediums and authors have the best investment \nperformance.

Based on the data, it is clear how the popularity of art has taken a big leap in \nrecent years, both in terms of prices and volume. For example, for many types of \nart work, the price increase or performance has been over 10% a year. Hence, a \nwell-chosen piece of art is a good choice to protect your money against inflation.

Kanvas.ai's Art Index currently does not include non-auction art information, but \nwe have a plan to start collecting data on NFT art media sold on the NFTKanvas.ai \npage as well.
''', unsafe_allow_html=True)


# FIGURE - date and average price
st.subheader('Figure - Historical Price Performance')
fig = px.area(df_hist, x=df_hist.index, y="avg_price",
              labels={
                 "avg_price": "Historical Index Performance (€)",
                 "date": "Auction Year",
             })
st.plotly_chart(fig, use_container_width=True)

# TABLE - categories average price
st.subheader('Table - Historical Price Performance by Category')
table_data = create_table(df, category_column="category", category_list=df["category"].unique(), use_price_sum=False, table_height=150)
st.table(table_data)

# FIGURE - date and volume
st.subheader('Figure - Historical Volume Growth by Category')
fig = px.area(df_hist, x=df_hist.index, y="volume", 
             labels={
                 "volume": "Volume (€)",
                 "date": "Auction Year",
             })
st.plotly_chart(fig, use_container_width=True)

# TABLE - categories volume
st.subheader('Table - Historical Volume Growth')
table_data = create_table(df, category_column="category", category_list=df["category"].unique(), use_price_sum=True, table_height=150)
st.table(table_data)

# FIGURE - treemap covering categories, techniques and authors by volume and overbid
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

# TABLE - best authors average price
author_sum = df.groupby(["author"], sort=False)["end_price"].sum()
top_authors = author_sum.sort_values(ascending=False)[:10]

st.subheader('Table - Top 10 Best Performing Artists')
table_data = create_table(df, category_column="author", category_list=top_authors.index, use_price_sum=False, table_height=250)    
st.table(table_data)

# TABLE - best authors volume
st.subheader('Table - Volume Growth for Top 10 Artists')
table_data = create_table(df, category_column="author", category_list=top_authors.index, use_price_sum=True, table_height=250)    
st.table(table_data)

# FIGURE - date and price
st.subheader('Figure - Age of Art Work vs Price')
fig = px.scatter(df.dropna(subset=["decade"]), x="art_work_age", y="end_price", color="category",
                 size='decade', hover_data=['author'],
                 labels={
                     "end_price": "Auction Final Sales Price (€)",
                     "art_work_age": "Art Work Age",
                     "author": "Author",
                     "category": "Category",
                     "decade": "Decade"
                  })
st.plotly_chart(fig, use_container_width=True)

# FIGURE - size and price
st.subheader('Figure - Size of Art Work vs Price')
df["dimension"] = df["dimension"] / (1000*1000)
fig = px.scatter(df.dropna(subset=["dimension"]), x="dimension", y="end_price", color="category",
                 size='dimension', hover_data=['author'],
                 labels={
                     "end_price": "Auction Final Sales Price (€)",
                     "dimension": "Dimension (m²)",
                     "author": "Author",
                     "category": "Category",
                  })

st.plotly_chart(fig, use_container_width=True)

st.text('Copyright: Kanvas.ai')
st.text('Authors: Astrid Laupmaa, Julian Kaljuvee, Markus Sulg')
st.text('Source: Estonian public art auction sales (2001-2021)')
