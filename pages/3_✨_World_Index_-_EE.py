import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy import stats
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

df = read_df('data/europe1.csv')
df = df[df["auction_year"] >= 2000]
df = df[df["dimension"]>0]
df = df.dropna(subset=["currency"])
df["technique"] = df["technique"].str.capitalize() 
#df = df[df["author"]!="Tito Salas "]
df['date'] = df["auction_year"]
df = df.sort_values(by=["date"])

def change_value(change_from, change_to, column):
    df.loc[df[column]==change_from, column] = change_to
# Estonian categories and techniques
change_value("Painting", "Maal", "category")
change_value("Mixed media", "Segatehnika", "category")
change_value("Graphics", "Graafika", "category")
change_value("Drawing", "Joonistus", "category")
change_value("Other", "Muu", "category")

change_value("Oil", "Õli", "technique")
change_value("Acrylic", "Akrüül", "technique")
change_value("Gouache", "Guašš", "technique")
change_value("Painting", "Maal", "technique")
change_value("Watercolor", "Akvarell", "technique")
change_value("Pastel", "Pastell", "technique")
#change_value("Tempera", "Tempera", "technique")

change_value("Aquatint", "Akvatinta", "technique")
change_value("Etching", "Etsing", "technique")
change_value("Linoleum", "Linool", "technique")
change_value("Linocut", "Linool", "technique")
change_value("Etching", "Etsing", "technique")
change_value("Screenprint", "Siiditrükk", "technique")
change_value("Silkscreen", "Siiditrükk", "technique")
change_value("Serigraph", "Siiditrükk", "technique")
change_value("Silk print", "Siiditrükk", "technique")
change_value("Lithograph", "Litograafia", "technique")
change_value("Offset", "Litograafia", "technique")
change_value("Drypoint", "Kuivnõel", "technique")
change_value("Engraving", "Gravüür", "technique")
change_value("Graphics", "Graafika", "technique")

change_value("Drawing", "Joonistus", "technique")
change_value("Ink", "Tint", "technique")
change_value("Crayon", "Pastell", "technique")
df.loc[df["technique"]=="Pastell", "category"] = "Maal"
change_value("Pencil", "Pliiats", "technique")
change_value("Pen", "Pliiats", "technique")
change_value("Charcoal", "Süsi", "technique")
change_value("Graphite", "Grafiit", "technique")

change_value("Photograph", "Fotograaf", "technique")
change_value("Sculpture", "Skulptuur", "technique")
change_value("Collage", "Kollaaž", "technique")

change_value("Mixed", "Segatehnika", "technique")

# remove multi-word techniques
df.loc[df["technique"].str.contains(" "), "category"] = ""

#change_value("Vitrography", "Vitrograafia", "technique")
#change_value("Wood cut", "Puugravüür", "technique")

kanvas_logo = get_img_with_href('data/horisontal-BLACK.png', 'https://kanvas.ai', '200px')
st.sidebar.markdown(kanvas_logo, unsafe_allow_html=True)

kanvas_logo = get_img_with_href('data/horisontal-BLACK.png', 'https://kanvas.ai', '400px')
st.markdown(kanvas_logo, unsafe_allow_html=True)

# TITLE
st.title('Euroopa kunsti indeks')
toc.header('Ülevaade')
create_paragraph('''Kanvas.ai kunsti indeks on tööriist kunsti investeerijale.

Kanvas.ai kunsti indeks viimase 19 aasta (2002 kuni 2021) Eesti kunstioksjonite \nmüükide põhjal loodud andmebaas, eesmärgiga muuta kunst ja kunsti investeerimine \nlihtsamini mõistetavaks igale huvilisele.

Andmed on kogutud Euroopa põhiliste galeriide avalike oksjoni tulemuste põhjal, mis \nannab ülevaate kuidas käitub kunstiturg ajas ning millised kunstimeediumid ning \nautorid on kõige parema investeerimise tootlikkusega.

Kanvas.ai kunstiindeksist puuduvad oksjoniväline kunsti info kuid meil on plaan \nhakata koguma ka NFTKanvas.ai lehel müüdud NFT kunstimeediumi andmeid.

Kunstiindeksi metoodika on praegu väljatöötamisel. Soovituste ja kommentaaridega saatke meile e-kiri info@kanvas.ai.
''')

# FIGURE - treemap covering categories, techniques and authors by volume and overbid TOP 5
toc.subheader('Joonis - Kunsti müügid asukoha ja galerii järgi (Top 5 asukohta)')
top_10_loc = list(df["loc"].value_counts().nlargest(5).index)

df2 = df[df["loc"].isin(top_10_loc)]
#df2 = df2[df2["author"].isin(top_authors)]


table_data = create_table(df2, "src", list(df2["src"].unique()), calculate_volume=False, table_height=250)
df2["yearly_performance"] = [table_data[table_data["Tehnika"] == x]["Iga-aastane kasv (%)"] for x in df2["src"]]

df2 = df2.groupby(['loc', 'src']).agg({'end_price':['sum'], 'yearly_performance':['mean']})
df2.columns = ['total_sales', 'yearly_performance']
df2 = df2.reset_index()

@st.cache_data
def create_treemap_1():
    fig = px.treemap(df2, path=[px.Constant("Asukohad"), 'loc', 'src'], values='total_sales',
                      color='yearly_performance',
                      color_continuous_scale='RdBu',
                      range_color = (-20, df2['yearly_performance'].mean()),
                      labels={
                         "yearly_performance": "Aasta tootlus (%)",
                         "total_sales": "Kogumüük",
                         "author": "Autor",
                      })
    return fig
fig = create_treemap_1()
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
fig.update_traces(hovertemplate='<b>%{label} </b> <br> Kogumüük: %{value}<br> Aasta tootlus (%): %{color:.2f}',)
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''Tekst
''')

# FIGURE - treemap covering categories, techniques and authors by volume and overbid OTHER
toc.subheader('Joonis - Kunsti müügid asukoha ja galerii järgi (Teised asukohad)')

df2 = df[~df["loc"].isin(top_10_loc)]

table_data = create_table(df2, "src", list(df2["src"].unique()), calculate_volume=False, table_height=250)
df2["yearly_performance"] = [table_data[table_data["Tehnika"] == x]["Iga-aastane kasv (%)"] for x in df2["src"]]

df2 = df2.groupby(['loc', 'src']).agg({'end_price':['sum'], 'yearly_performance':['mean']})
df2.columns = ['total_sales', 'yearly_performance']
df2 = df2.reset_index()

@st.cache_data
def create_treemap_2():
    fig = px.treemap(df2, path=[px.Constant("Asukohad"), 'loc', 'src'], values='total_sales',
                      color='yearly_performance',
                      color_continuous_scale='RdBu',
                      range_color = (-20, df2['yearly_performance'].mean()),
                      labels={
                         "yearly_performance": "Aasta tootlus (%)",
                         "total_sales": "Kogumüük",
                         "author": "Autor",
                      })
    return fig
fig = create_treemap_2()
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
fig.update_traces(hovertemplate='<b>%{label} </b> <br> Kogumüük: %{value}<br> Aasta tootlus (%): %{color:.2f}',)
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''...
''')

prices = []
volumes = []
dates = []

for year in range(df["date"].min(), df["date"].max()+1):
    dates.append(year)
    df2 = df[df["date"] == year]
    df3 = df2[(np.abs(stats.zscore(df2["end_price"])) < 2)]

    prices.append(df3["end_price"].mean())
    volumes.append(df3["end_price"].sum())
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
df2 = df[df["category"]!=""]
categories = list(df2["category"].unique())
#categories.remove("Segatehnika")
table_data = create_table(df2, "category", categories, calculate_volume=False, table_height=150)
st.table(table_data)
create_paragraph('Tekst')

# FIGURE - date and volume
toc.subheader('Joonis - Ajalooline volüümi kasv')
fig = px.area(df_hist, x="date", y="volume", 
             labels={
                 "volume": "Volüüm (€)",
                 "date": "Oksjoni aasta",
             })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''Tekst
''')

# TABLE - categories volume
toc.subheader('Tabel - Ajalooline volüümi kasv kategooriate kaupa')
df2 = df[df["category"]!=""]
table_data = create_table(df2, "category", categories, calculate_volume=True, table_height=150)
st.table(table_data)
create_paragraph('Tekst')

# TABLE - best authors average price
author_sum = df.groupby(["author"], sort=False)["end_price"].sum()
top_authors = []
for author in author_sum.sort_values(ascending=False).index:
    if df[df["author"] == author]["date"].nunique() > 1:
        top_authors.append(author)
        if len(top_authors) >= 10:
            break

toc.subheader('Tabel - Top 10 parimat kunstnikku')
table_data = create_table(df, "author", top_authors, calculate_volume=False, table_height=250)    
st.table(table_data)
create_paragraph('''Tekst
''')

# FIGURE - treemap covering categories, techniques and authors by volume and overbid
toc.subheader('Joonis - Kunsti müügid kategooria ja kunstniku järgi')

df2 = df[df["category"]!=""]
df2 = df2[df["author"].isin(top_authors)]
table_data = create_table(df2, "author", top_authors, calculate_volume=False, table_height=250)
df2["yearly_performance"] = [table_data[table_data["Autor"] == x]["Iga-aastane kasv (%)"] for x in df2["author"]]

df2 = df2.groupby(['author', 'technique', 'category']).agg({'end_price':['sum'], 'yearly_performance':['mean']})
df2.columns = ['total_sales', 'yearly_performance']
df2 = df2.reset_index()

@st.cache_data
def create_treemap_3():
    fig = px.treemap(df2, path=[px.Constant("Tehnikad"), 'category', 'technique', 'author'], values='total_sales',
                      color='yearly_performance',
                      color_continuous_scale='RdBu',
                      range_color = (-20, df2['yearly_performance'].mean()),
                      labels={
                         "yearly_performance": "Aasta tootlus (%)",
                         "total_sales": "Kogumüük",
                         "author": "Autor",
                      })
    return fig
fig = create_treemap_3()
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
fig.update_traces(hovertemplate='<b>%{label} </b> <br> Kogumüük: %{value}<br> Aasta tootlus (%): %{color:.2f}',)
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''Tekst
''')

# TABLE - best authors volume
toc.subheader('Tabel - Volüümi kasv Top 10 kunstnikul')
table_data = create_table(df, "author", top_authors, calculate_volume=True, table_height=250)    
st.table(table_data)
create_paragraph('''Tekst
''')

def create_credits(text):
    st.markdown('<span style="word-wrap:break-word;font-family:Source Code Pro;font-size: 14px;">' + text + '</span>', unsafe_allow_html=True)
create_credits('''Copyright: Kanvas.ai''')
create_credits('''Autorid: Astrid Laupmaa, Julian Kaljuvee, Markus Sulg''')
create_credits('''Allikad: Euroopa avalikud kunsti oksjonid (2001-2021)''')
create_credits('''Muu: Inspireeritud Riivo Antoni loodud kunstiindeksist; <br>Heldet toetust pakkus <a href="https://tezos.foundation/">Tezos Foundation</a>''')
toc.generate()

@st.cache_data
def convert_df():
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return read_df('data/europe2.csv').to_csv().encode('utf-8')

csv = convert_df()
st.download_button(label="Laadi alla andmed",data=csv, file_name='europe_art_index.csv', mime='text/csv')