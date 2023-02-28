import streamlit as st
import plotly.express as px
import pandas as pd
from StreamlitHelper import Toc, get_img_with_href, read_df, create_table

st.set_page_config(
    page_title="Art Index",
    page_icon="data/Vertical-BLACK2.ico",
)
# inject CSS to hide row indexes and style fullscreen button
inject_style_css = """
            <style>
            /*style hide table row index*/
            thead tr th:first-child {display:none}
            tbody th {display:none}
            
            /*style fullscreen button*/
            button[title="View fullscreen"] {
                background-color: #004170cc;
                right: 0;
                color: white;
            }

            button[title="View fullscreen"]:hover {
                background-color:  #004170;
                color: white;
                }
            a { text-decoration:none;}
            </style>
            """
st.markdown(inject_style_css, unsafe_allow_html=True)

def create_paragraph(text):
    st.markdown('<span style="word-wrap:break-word;">' + text + '</span>', unsafe_allow_html=True)
    
# Sidebar Table of Contents
toc = Toc()
toc.placeholder(sidebar=True)

df = read_df('data/haus_cleaned.csv')
df = df[df["date"] >= 2001]
df = df[df["date"] <= 2023]
df = df.sort_values(by=["date"])
df = df.dropna(subset=["author"])

kanvas_logo = get_img_with_href('data/horisontal-BLACK.png', 'https://kanvas.ai', '200px')
st.sidebar.markdown(kanvas_logo, unsafe_allow_html=True)

kanvas_logo = get_img_with_href('data/haus_logo.png', 'https://haus.ee', '200px')
st.markdown(kanvas_logo, unsafe_allow_html=True)

# TITLE
st.title('Haus kunsti indeks')
toc.header('Ülevaade')
create_paragraph('''Kanvas.ai kunsti indeks on tööriist kunsti investeerijale.

Andmed on kogutud Haus galerii avalike oksjoni tulemuste põhjal, mis \nannab ülevaate kuidas käitub kunstiturg ajas ning millised kunstimeediumid ning \nautorid on kõige parema investeerimise tootlikkusega.

Kanvas.ai kunstiindeksist puuduvad oksjoniväline kunsti info kuid meil on plaan \nhakata koguma ka NFTKanvas.ai lehel müüdud NFT kunstimeediumi andmeid.

Kunstiindeksi metoodika on praegu väljatöötamisel. Soovituste ja kommentaaridega saatke meile e-kiri info@kanvas.ai.
''')

prices = []
volumes = []
dates = []
for year in range(df["date"].min(), df["date"].max()+1):
    print(year)
    dates.append(year)
    prices.append(df[df["date"] == year]["end_price"].mean())
    volumes.append(df[df["date"] == year]["end_price"].sum())
data = {'avg_price': prices, 'volume': volumes, 'date': dates}
df_hist = pd.DataFrame.from_dict(data)

# FIGURE - date and average price
toc.subheader('Joonis - Ajalooline hinnanäitaja')
fig = px.area(df_hist, x="date", y="avg_price",
              labels={
                 "avg_price": "Ajalooline indeksinäitaja (€)",
                 "date": "Oksjoni aasta",
             })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)
create_paragraph('Tekst')

# TABLE - categories average price
toc.subheader('Tabel - Ajalooline hinnanäitaja kategooriate kaupa')
table_data = create_table(df.dropna(subset=["date"]), category_column="category", category_list=df["category"].unique(), calculate_volume=False, table_height=150)
st.table(table_data)
create_paragraph('Meediumite ehk tehnika järgi järjestud vastavalt sellele, missugused meediumid domineerivad kõige kallimalt müüdud teoste hulgas.')

# FIGURE - date and volume
toc.subheader('Joonis - Ajalooline volüümi kasv')
fig = px.area(df_hist, x="date", y="volume", 
             labels={
                 "volume": "Volüüm (€)",
                 "date": "Oksjoni aasta",
             })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''Volüümi kasv annab meile ülevaate, kui palju on ajas tõusnud ja langenud oksjonite käive. 
Näiteks 2001 aastal oli oksjoni käive 174 000- euro ringis, siis 2021 aastal oli oksjonite käive 4.5miljonit. Kindlasti on väga oluline roll krooni asendumisel euroga ja juurde on tulnud oksjonimaju. Sellegipoolest on kunsti müük märkimisväärse hüppe teinud alates 2019, mis on 20 aasta lõikes kõige suurem. Viimane suurem muutus toimus 2006-2009 majanduskriisi mõjutustest.
''')

# TABLE - categories volume
toc.subheader('Tabel - Ajalooline volüümi kasv kategooriate kaupa')
table_data = create_table(df.dropna(subset=["date"]), category_column="category", category_list=df["category"].unique(), calculate_volume=True, table_height=150)
st.table(table_data)
create_paragraph('Sellest tabelist näeme, milline meedium on olnud kõige suurema käibega. Antud andmete põhjal võime näiteks näha, et graafika on kõige populaarsem ning kõige suurema käibe tõusu protsendiga.(Keskmiselt 204% 20 aasta jooksul ja õlimaalil samal ajal 35%)')

# FIGURE - treemap covering categories, techniques and authors by volume and overbid
toc.subheader('Joonis - Kunsti müügid kategooria ja kunstniku järgi')

df['start_price'] = df['start_price'].fillna(df['end_price'])
df['overbid_%'] = (df['end_price'] - df['start_price'])/df['start_price'] * 100
df['art_work_age'] = df['date'] - df['year']
df2 = df[df["technique"] != " "]
df2 = df2.groupby(['author', 'technique', 'category']).agg({'end_price':['sum'], 'overbid_%':['mean']})
df2.columns = ['total_sales', 'overbid_%']
df2 = df2.reset_index()

fig = px.treemap(df2, path=[px.Constant("Categories"), 'category', 'technique', 'author'], values='total_sales',
                  color='overbid_%',
                  color_continuous_scale='RdBu',
                  range_color = (0, df['overbid_%'].mean() + df['overbid_%'].std()),
                  labels={
                     "overbid_%": "Ülepakkumine (%)",
                     "total_sales": "Kogumüük",
                     "author": "Autor",
                  })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
fig.update_traces(hovertemplate='<b>%{label} </b> <br> Kogumüük: %{value}<br> Ülepakkumine (%): %{color:.2f}',)
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''tekst
''')

# FIGURE - treemap covering categories, techniques and authors by volume and overbid
toc.subheader('Joonis - Kunsti müügid kategooria ja kunstniku järgi')

table_data = create_table(df, category_column="author", category_list=list(df["author"].unique()), calculate_volume=False, table_height=250)
df["yearly_performance"] = [table_data[table_data["Kategooria"] == x]["Iga-aastane kasv (%)"] for x in df["author"]]
df['art_work_age'] = df['date'] - df['year']
df2 = df.groupby(['author', 'technique', 'category']).agg({'end_price':['sum'], 'yearly_performance':['mean']})
df2.columns = ['total_sales', 'yearly_performance']
df2 = df2.reset_index()

fig = px.treemap(df2, path=[px.Constant("Categories"), 'category', 'technique', 'author'], values='total_sales',
                  color='yearly_performance',
                  color_continuous_scale='RdBu',
                  range_color = (-20, 100),
                  labels={
                     "yearly_performance": "Aasta tootlus",
                     "total_sales": "Kogumüük",
                     "author": "Autor",
                  })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
fig.update_traces(hovertemplate='<b>%{label} </b> <br> Kogumüük: %{value}<br> Aasta tootlus (%): %{color:.2f}',)
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''...
''')

# TABLE - best authors average price
author_sum = df.groupby(["author"], sort=False)["end_price"].sum()
top_authors = author_sum.sort_values(ascending=False)[:10]

toc.subheader('Tabel - Top 10 parimat kunstnikku')
table_data = create_table(df, category_column="author", category_list=top_authors.index, calculate_volume=False, table_height=250)    
st.table(table_data)
create_paragraph('''tekst
''')

# TABLE - best authors volume
toc.subheader('Tabel - Volüümi kasv Top 10 kunstnikul')
table_data = create_table(df, category_column="author", category_list=top_authors.index, calculate_volume=True, table_height=250)    
st.table(table_data)
create_paragraph('''tekst
''')

# FIGURE - date and price
toc.subheader('Joonis - Kunstitöö vanus vs hind')
df2 = df[df["technique"] != " "]
fig = px.scatter(df2.dropna(subset=["decade"]), x="art_work_age", y="end_price", color="category",
                 animation_frame="date", animation_group="technique", hover_name="technique",
                 size='date', hover_data=['author'], size_max=15, range_x=[-2,130], range_y=[-1000,100000],
                 labels={
                     "end_price": "Haamrihind (€)",
                     "art_work_age": "Kunstitöö vanus",
                     "author": "Autor",
                     "category": "Kategooria",
                     "decade": "Kümnend"
                  })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''tekst
''')

# FIGURE - size and price
toc.subheader('Joonis - Kunstitöö pindala vs hind')
df["dimension"] = df["dimension"] / (100*100)
df2 = df[df["technique"] != " "]
fig = px.scatter(df2.dropna(subset=["dimension"]), x="dimension", y="end_price", color="category",
                 animation_frame="date", animation_group="technique", hover_name="technique",
                 size='date', hover_data=['author'], size_max=15, range_x=[-2,60], range_y=[-5000,100000],
                 labels={
                     "end_price": "Haamrihind (€)",
                     "dimension": "Pindala (m²)",
                     "author": "Autor",
                     "category": "Kategooria",
                  })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''tekst
''')

def create_credits(text):
    st.markdown('<span style="word-wrap:break-word;font-family:Source Code Pro;font-size: 14px;">' + text + '</span>', unsafe_allow_html=True)
create_credits('''Copyright: Kanvas.ai''')
create_credits('''Autorid: Astrid Laupmaa, Julian Kaljuvee, Markus Sulg''')
create_credits('''Allikad: Haus kunsti oksjonid (2001-2022)''')
create_credits('''Muu: Inspireeritud Riivo Antoni loodud kunstiindeksist; <br>Heldet toetust pakkus <a href="https://tezos.foundation/">Tezos Foundation</a>''')
toc.generate()

@st.cache
def convert_df():
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return read_df('data/haus_cleaned.csv').to_csv().encode('utf-8')

csv = convert_df()
st.download_button(label="Laadi alla andmed",data=csv, file_name='haus_kunsti_indeks.csv', mime='text/csv')
