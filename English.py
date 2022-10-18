import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import base64

st.set_page_config(
    page_title="Art Index",
    page_icon="data/Vertical-BLACK2.ico",
)
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
def create_table(df, category_column:str, category_list:list, calculate_volume:bool, table_height:int):
    category_returns = []
    for cat in category_list:
        df_cat = df[df[category_column]==cat]

        dates = np.sort(df_cat["date"].unique())

        prices = []
        start_year = df_cat["date"].min()
        df_cat_date = df_cat[df_cat["date"]==start_year]
        if calculate_volume: 
            prices.append(df_cat_date["end_price"].sum())
        else:
            prices.append(df_cat_date["end_price"].mean())
        price_changes = []
        last_year = start_year
        for date in dates[1:]:
            df_cat_date = df_cat[df_cat["date"]==date]

            start_sum = prices[-1]
            end_sum = 0
            if calculate_volume: 
                end_sum = df_cat_date["end_price"].sum()
            else:
                end_sum = df_cat_date["end_price"].mean()

            price_change = (end_sum - start_sum) / start_sum * 100 / (date-last_year)
            price_changes.append(price_change) # Kasvu arvutus
            prices.append(end_sum) # Jätame meelde selle aasta hinna
            last_year = date
        annual_return = round(np.mean(price_changes), 4)
        total_return = round(annual_return * len(dates), 4)
        category_returns.append([cat, total_return, annual_return])
        
    df_cat_returns = pd.DataFrame(category_returns, columns=[category_column.capitalize(), "Total Growth since Inception (%)", "Annual Growth Rate (%)"]) 
    df_cat_returns = df_cat_returns.sort_values(by="Annual Growth Rate (%)", ascending=False)
    return df_cat_returns.drop("Total Growth since Inception (%)", axis=1)

def create_paragraph(text):
    st.markdown('<span style="word-wrap:break-word;">' + text + '</span>', unsafe_allow_html=True)
    
df = read_df('data/auctions_clean.csv')
# Fix data
df = df[df["date"] >= 2001]
df = df[df["date"] <= 2021]
df.loc[df["technique"]=="Mixed tech", "technique"] = "Mixed technique"
df_hist = read_df('data/historical_avg_price.csv')
df_hist = df_hist[df_hist["date"] >= 2001]
df_hist = df_hist.groupby("date").sum()

# LOGO
# https://discuss.streamlit.io/t/href-on-image/9693/4
@st.cache(ttl=60*60*24*7, max_entries=300, allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(ttl=60*60*24*7, max_entries=300, allow_output_mutation=True)
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
create_paragraph('''Kanvas.ai Art Index is a tool for art investors.

Kanvas.ai's art index is a database created based on Estonian art auction sales \nhistory of the last 20 years (2001-2021), with an aim of making art and investing \nin art easier to understand for anyone interested.

The data has been collected based on the results of the public auctions of the \nmain galleries in Estonia, which provides an overview of how the art market \nbehaves over time and which art mediums and authors have the best investment \nperformance.

Based on the data, it is clear how the popularity of art has taken a big leap in \nrecent years, both in terms of prices and volume. For example, for many types of \nart work, the price increase or performance has been over 10% a year. Hence, a \nwell-chosen piece of art is a good choice to protect your money against inflation.

Kanvas.ai's Art Index currently does not include non-auction art information, but \nwe have a plan to start collecting data on NFT art media sold on the NFTKanvas.ai \npage as well.''')


# FIGURE - date and average price
st.subheader('Figure - Historical Price Performance')
fig = px.area(df_hist, x=df_hist.index, y="avg_price",
              labels={
                 "avg_price": "Historical Index Performance (€)",
                 "date": "Auction Year",
             })
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''The Art Index gives an overview of the rise and fall in the price of art. The price of art has made a noticeable jump in recent years. Interest in investing in art on the art auction market has skyrocketed since the pandemic.''')

# TABLE - categories average price
st.subheader('Table - Historical Price Performance by Category')
table_data = create_table(df, category_column="category", category_list=df["category"].unique(), calculate_volume=False, table_height=150)
st.table(table_data)
create_paragraph('''Ranked by medium, or technique, according to which medium dominates the highest-selling works.''')

# FIGURE - date and volume
st.subheader('Figure - Historical Volume Growth')
fig = px.area(df_hist, x=df_hist.index, y="volume", 
             labels={
                 "volume": "Volume (€)",
                 "date": "Auction Year",
             })
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''The increase in volume gives us an overview of how much the turnover of auctions has risen and fallen over time.

For example, in 2001 the auction turnover was around 174,000 euros, then in 2021 the auction turnover was 4.5 million. Certainly, the replacement of the kroon with the euro plays a very important role, and more auction galleries have been added. Still, art sales have seen a significant jump since 2019, the biggest in 20 years. The last major change occurred due to the effects of the 2006-2009 economic crisis.
''')

# TABLE - categories volume
st.subheader('Table - Historical Volume Growth by Category')
table_data = create_table(df, category_column="category", category_list=df["category"].unique(), calculate_volume=True, table_height=150)
st.table(table_data)
create_paragraph('''From this table, we can see which medium has had the highest turnover. Based on the given data, we can see, for example, that graphics are the most popular and with the highest annual turnover increase percentage (204% annually over 20 years and 34% for oil painting at the same time).''')

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
create_paragraph('''Categories and artists, where the color scale gives us an overview, how much art has been overbidi during auctions ,and volume ranked by category and artist.

For example, the blue color shows artists and mediums, which had the highest overbidding percentage. Volume is also shown next to the artist’s name. For example, Konrad Mägi has the highest art piece sold, but this table shows that the highest overbidding goes to the works of Olev Subbi, in regards to the tempera medium. (711.69 % price increase from the starting price, while the numbers for Konrad Mägi are 59.06 % for oil on cardboard and 85.44% for oil on canvas medium). Although Konrad Mägi still has the edge over Subbi in terms of volume.
''')

# TABLE - best authors average price
author_sum = df.groupby(["author"], sort=False)["end_price"].sum()
top_authors = author_sum.sort_values(ascending=False)[:10]

st.subheader('Table - Top 10 Best Performing Artists')
table_data = create_table(df, category_column="author", category_list=top_authors.index, calculate_volume=False, table_height=250)    
st.table(table_data)
create_paragraph('''This table shows the most popular artists and their growth percentage. The percentage is calculated based on annual average end price differences.

Leading this table is Konrad Mägi, whose growth percentage is on average 198.95%. This growth percentage is definitely affected by the uniqueness of his works. Konrad Mägi has a limited number of works displayed at auctions. In second place we find Eduard Wiiralt, who in contrast to Konrad Mägi has a lot of his works displayed at auctions. The starting prices of Wiiralt’s works are low and he is very popular amongst collectors.
''')

# TABLE - best authors volume
st.subheader('Table - Volume Growth for Top 10 Artists')
table_data = create_table(df, category_column="author", category_list=top_authors.index, calculate_volume=True, table_height=250)    
st.table(table_data)
create_paragraph('''This table shows the turnover and average annual growth of art works. Here Wiiralt is positioned at 8th place and Konrad Mägi at 1st. Because the growth percentage is during the whole period (2001-2021) turnover, then the artists, who have the most works bought, are situated at the top of the table.
''')

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
create_paragraph('''From the given graph, it is possible to determine the price of the work according to the age and technique of the work of art. Techniques are separated by color.

The oldest work dates back to 1900, but is not the most expensive. In general, it can be seen that older works are more expensive, with the exception of Olev Subbi. It can be seen that pre-World War II works from 1910-1940 have been sold higher.
''')

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
create_paragraph('''An overview of the relationship between the dimensions, technique and price of the work. Many smaller format works are often more expensive than large ones. The size of the piece does not necessarily mean that it is more expensive. Rather, the author is more important, and then the size of the work. For example, Konrad Mägi's Õlimaa is among the averages on the measurement chart, but considerably higher than the others on the price scale (127,823 euros hammer price), while the hammer price of the largest work (Toomas Vint) is €7,094.
''')

st.text('Copyright: Kanvas.ai')
st.text('Authors: Astrid Laupmaa, Julian Kaljuvee, Markus Sulg')
st.text('Source: Estonian public art auction sales (2001-2021)')
st.text('Other credits: Inspired by the original Estonian Art Index created by Riivo Anton')

