import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
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
    
def create_credits(text):
    st.markdown('<span style="word-wrap:break-word;font-family:Source Code Pro;font-size: 14px;">' + text + '</span>', unsafe_allow_html=True)
# Sidebar Table of Contents
toc = Toc()
toc.placeholder(sidebar=True)

df = read_df('data/haus_cleaned.csv')
#df = df[df["date"] >= 2001]
df = df[df["date"] <= 2023]

df["category_parent"] = "Muu"
df.loc[df["category"] == "Õlimaal", "category_parent"] = "Maal"
df.loc[df["category"] == "Muu maalitehnika", "category_parent"] = "Maal"

df.loc[df["category"] == "Kõrgtrükk", "category_parent"] = "Graafika"
df.loc[df["category"] == "Sügavtrükk", "category_parent"] = "Graafika"
df.loc[df["category"] == "Lametrükk", "category_parent"] = "Graafika"
df.loc[df["category"] == "Digitrükk", "category_parent"] = "Graafika"

df.loc[df["category"] == "Joonistustehnika", "category_parent"] = "Joonistus"

df.loc[df["technique"] == "segatehnika", "category_parent"] = "Segatehnika"
df.loc[df["technique"]=="segatehnika", "category"] = "Segatehnika" 

order_categories = ["Maal", "Graafika", "Joonistus", "Segatehnika", "Muu"]
df["cat_sort"] = [order_categories.index(x) for x in df["category_parent"]]
df = df.sort_values(by=["date", "cat_sort"])
df = df.dropna(subset=["author"])

kanvas_logo = get_img_with_href('data/horisontal-BLACK.png', 'https://kanvas.ai', '200px')
st.sidebar.markdown(kanvas_logo, unsafe_allow_html=True)

kanvas_logo = get_img_with_href('data/haus_logo.png', 'https://haus.ee', '200px')
st.markdown(kanvas_logo, unsafe_allow_html=True)

# TITLE
st.title('Haus Galerii kunsti-indeks')
toc.header('Ülevaade')
create_paragraph('''Käesolev majandusanalüüsi loogikal põhinev ja graafiliselt teostatud kunsti-indeks on
koostatud Haus Galerii 25 aasta kunstioksjonite müügitulemuste põhjal.

Indeks annab ülevaate kuidas Haus Galerii poolt aktiivselt arendatud kunstiturg on ajas
käitunud ning millised autorid ja kunstitehnikad on olnud selle perioodi jooksul kõige
parema investeerimise tootlikusega.

Indeksi eesmärk on olla abistavaks tööriistaks kunstiostjale, kes peab silmas lisaks
emotsionaalsele väärtusele ka kunsti hinnakasvu väärtust.
''')

create_credits("Indeks on koostatud Kanvas.ai poolt. Kunsti-indeksi metoodika on täiustamisel ja edasiarendamisel ning kõik soovitused ja kommentaarid on oodatud info@kanvas.ai")

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
# unfinished trendlines
fig2 = px.scatter(df_hist, x="date", y="avg_price", trendline="ols")
fig2.data = [t for t in fig2.data if t.mode == "lines"]
#fig = go.Figure(data= fig.data + fig2.data)

st.plotly_chart(fig, use_container_width=True)
create_paragraph('''
See joonis näitab keskmise kunstiteose hinna kõikumist aastate vältel.
''')

# TABLE - categories average price
toc.subheader('Tabel - Ajalooline hinnanäitaja tehnikate kaupa')
table_data = create_table(df.dropna(subset=["date"]), category_column="category_parent", category_list=order_categories[:-1], calculate_volume=False, table_height=150)
st.table(table_data)
create_paragraph('See tabel näitab üldisemate tehnikate keskmise hinna kõikumist aastavahemikus.')

# FIGURE - date and volume
toc.subheader('Joonis - Ajalooline volüümi kasv')
fig = px.area(df_hist, x="date", y="volume", 
             labels={
                 "volume": "Volüüm (€)",
                 "date": "Oksjoni aasta",
             })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
# unfinished trendlines
fig2 = px.scatter(df_hist, x="date", y="volume", trendline="ols")
fig2.data = [t for t in fig2.data if t.mode == "lines"]
#fig = go.Figure(data= fig.data + fig2.data)

st.plotly_chart(fig, use_container_width=True)
create_paragraph('''
See joonis näitab oksjonite volüümi kõikumist aastate vältel.
''')

# TABLE - categories volume
toc.subheader('Tabel - Ajalooline volüümi kasv tehnikate kaupa')
table_data = create_table(df.dropna(subset=["date"]), category_column="category_parent", category_list=order_categories[:-1], calculate_volume=True, table_height=150)
st.table(table_data)
create_paragraph('See tabel näitab üldisemate tehnikate volüümi kõikumist aastavahemikus.')

# FIGURE - treemap covering categories, techniques and authors by volume and overbid
toc.subheader('Joonis - Kunsti müügid tehnika ja kunstniku järgi')

df['start_price'] = df['start_price'].fillna(df['end_price'])
df['overbid_%'] = (df['end_price'] - df['start_price'])/df['start_price'] * 100
df2 = df[df["technique"] != " "]
df2.loc[df2["category"] == "Muu maalitehnika", "category"] = df2["technique"]

df2 = df2.groupby(['author', 'technique', 'category', 'category_parent']).agg({'end_price':['sum'], 'overbid_%':['mean']})
df2.columns = ['total_sales', 'overbid_%']
df2 = df2.reset_index()

# fix treemap parenting
df2.loc[df2["category"] == "Muu maalitehnika", "category"] = df2["technique"]
df2.loc[df2["technique"] == "tempera", "technique"] = df2["author"]
df2.loc[df2["category"] == "tempera", "author"] = None

df2.loc[df2["technique"] == "akvarell", "technique"] = df2["author"]
df2.loc[df2["category"] == "akvarell", "author"] = None

df2.loc[df2["technique"] == "pastell", "technique"] = df2["author"]
df2.loc[df2["category"] == "pastell", "author"] = None

df2.loc[df2["technique"] == "akrüül", "technique"] = df2["author"]
df2.loc[df2["category"] == "akrüül", "author"] = None

df2.loc[df2["technique"] == "guašš", "technique"] = df2["author"]
df2.loc[df2["category"] == "guašš", "author"] = None

df2.loc[df2["category"] == "Joonistustehnika", "category"] = df2["author"]
df2.loc[df2["category_parent"] == "Joonistus", "author"] = None

df2.loc[df2["category"] == "Muu", "category"] = df2["author"]
df2.loc[df2["category_parent"] == "Muu", "author"] = None

df2.loc[df2["category"] == "Segatehnika", "category"] = df2["author"]
df2.loc[df2["category_parent"] == "Segatehnika", "author"] = None

fig = px.treemap(df2, path=[px.Constant("Tehnikad"), 'category_parent', 'category', 'technique', 'author'], values='total_sales',
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
create_paragraph('''
See joonis näitab suuruse poolest spetsiifiliste tehnikate ja autorite kogutulu. Värviga on erastatud alghinnast ülepakkumine.
''')

# FIGURE - treemap covering categories, techniques and authors by volume and overbid
toc.subheader('Joonis - Kunsti müügid tehnika ja kunstniku järgi')

table_data = create_table(df, category_column="author", category_list=list(df["author"].unique()), calculate_volume=False, table_height=250)
df["yearly_performance"] = [table_data[table_data["Autor"] == x]["Iga-aastane kasv (%)"] for x in df["author"]]
df2 = df.groupby(['author', 'technique', 'category', 'category_parent']).agg({'end_price':['sum'], 'yearly_performance':['mean']})
df2.columns = ['total_sales', 'yearly_performance']
df2 = df2.reset_index()

# fix treemap parenting
df2.loc[df2["category"] == "Muu maalitehnika", "category"] = df2["technique"]
df2.loc[df2["technique"] == "tempera", "technique"] = df2["author"]
df2.loc[df2["category"] == "tempera", "author"] = None

df2.loc[df2["technique"] == "akvarell", "technique"] = df2["author"]
df2.loc[df2["category"] == "akvarell", "author"] = None

df2.loc[df2["technique"] == "pastell", "technique"] = df2["author"]
df2.loc[df2["category"] == "pastell", "author"] = None

df2.loc[df2["technique"] == "akrüül", "technique"] = df2["author"]
df2.loc[df2["category"] == "akrüül", "author"] = None

df2.loc[df2["technique"] == "guašš", "technique"] = df2["author"]
df2.loc[df2["category"] == "guašš", "author"] = None

df2.loc[df2["category"] == "Joonistustehnika", "category"] = df2["author"]
df2.loc[df2["category_parent"] == "Joonistus", "author"] = None

df2.loc[df2["category"] == "Muu", "category"] = df2["author"]
df2.loc[df2["category_parent"] == "Muu", "author"] = None

df2.loc[df2["category"] == "Segatehnika", "category"] = df2["author"]
df2.loc[df2["category_parent"] == "Segatehnika", "author"] = None

fig = px.treemap(df2, path=[px.Constant("Tehnikad"), 'category_parent', 'category', 'technique', 'author'], values='total_sales',
                  color='yearly_performance',
                  color_continuous_scale='RdBu',
                  range_color = (-20, 100),
                  labels={
                     "yearly_performance": "Aasta tootlus (%)",
                     "total_sales": "Kogumüük",
                     "author": "Autor",
                  })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
fig.update_traces(hovertemplate='<b>%{label} </b> <br> Kogumüük: %{value}<br> Aasta tootlus (%): %{color:.2f}',)
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''
See joonis näitab suuruse poolest spetsiifiliste tehnikate ja autorite kogutulu. Värviga on erastatud kunstitööde aasta tootlused.
''')

# TABLE - best authors average price
author_sum = df.groupby(["author"], sort=False)["end_price"].sum()
top_authors = author_sum.sort_values(ascending=False)[:25]

toc.subheader('Tabel - Top 25 volüümiga kunstnike hinna kasv')
table_data = create_table(df, category_column="author", category_list=top_authors.index, calculate_volume=False, table_height=250)    
st.table(table_data)
create_paragraph('''
See tabel näitab (alates suurimast kogutuluga autorist) autorite tööde keskmist hinnakasvu aastas.
''')

# TABLE - best authors volume
toc.subheader('Tabel - Top 25 volüümiga kunstnike volüümi kasv')
table_data = create_table(df, category_column="author", category_list=top_authors.index, calculate_volume=True, table_height=250)    
st.table(table_data)
create_paragraph('''
See tabel näitab (alates suurimast kogutuluga autorist) aurotite tööde kogutulu kasvu aastas.
''')

# FIGURE - date and price
toc.subheader('Joonis - Kunstitöö vanus vs hind')
df['art_work_age'] = df['date'] - df['year']

df2 = df[df["technique"] != " "]
df2 = df2[df["category_parent"] != "Muu"]
# create overview for first view - TODO add to slider
df3 = df2.groupby(['category_parent']).agg({'end_price':['mean'], 'art_work_age':['mean']})
df3.columns = ['sales', 'age']
df3 = df3.reset_index()
df3["cat_sort"] = [order_categories.index(x) for x in df3["category_parent"]]
df3 = df3.sort_values(by=["cat_sort"])
fig_all = px.scatter(df3.dropna(subset=['age']), x="age", y="sales", color="category_parent",
                 size='sales', 
                 labels={
                     "sales": "Haamrihind (€)",
                     "age": "Kunstitöö vanus",
                     "category_parent": "Tehnika",
                     "decade": "Kümnend",
                     "date":"Aasta",
                  })

fig = px.scatter(df2.dropna(subset=["decade"]), x="art_work_age", y="end_price", color="category_parent",
                 animation_frame="date", animation_group="category_parent", hover_name="category_parent",
                 size='date', size_max=15, range_x=[-2,125], range_y=[-200,15000],
                 labels={
                     "end_price": "Haamrihind (€)",
                     "art_work_age": "Kunstitöö vanus",
                     "category_parent": "Tehnika",
                     "decade": "Kümnend",
                     "date":"Aasta",
                  })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))

fig = go.Figure(data=fig_all.data, frames=fig['frames'], layout=fig.layout)

st.plotly_chart(fig, use_container_width=True)
create_paragraph('''
See joonis näitab esmalt kunstitehnika tööde keskmist hinda ja vanust. Animatsiooni alustades näeb aastate kaupa keskmist hinda ja vanust.
''')

# FIGURE - size and price
toc.subheader('Joonis - Kunstitöö pindala vs hind')
df["dimension"] = df["dimension"] / (100*100)
df2 = df[df["technique"] != " "]
df2 = df2[df["category_parent"] != "Muu"]
df2 = df2.dropna(subset=["dimension"])
# create overview for first view - TODO add to slider
df3 = df2.groupby(['category_parent']).agg({'end_price':['mean'], 'dimension':['mean']})
df3.columns = ['sales', 'dim']
df3 = df3.reset_index()
df3["cat_sort"] = [order_categories.index(x) for x in df3["category_parent"]]
df3 = df3.sort_values(by=["cat_sort"])
df3["date"] = 1000
#df2.loc[df2.index < 100, "category_parent"] = "Joonistus"
#df2 = df2.sort_values(by=["date"], ascending=False)
fig_all = px.scatter(df3, x="dim", y="sales", color="category_parent",
                 size="sales",
                 labels={
                     "sales": "Haamrihind (€)",
                     "dim": "Pindala (m²)",
                     "category_parent": "Tehnika",
                     "date":"Aasta",
                  })

fig = px.scatter(df2, x="dimension", y="end_price", color="category_parent",
                 animation_frame="date", animation_group="category_parent", hover_name="category_parent",
                 size='date', size_max=15, range_x=[-2,36], range_y=[-200,15000],
                 labels={
                     "end_price": "Haamrihind (€)",
                     "dimension": "Pindala (m²)",
                     "category_parent": "Tehnika",
                     "date":"Aasta",
                  })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
frames= []
fig = go.Figure(data=fig_all.data, frames=fig['frames'], layout=fig.layout)
#fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 0
#fig.layout.updatemenus = [fig.layout.updatemenus[0]] + list(fig.layout.updatemenus)
#fig.data = fig.frames[0].data

st.plotly_chart(fig, use_container_width=True)
create_paragraph('''
See joonis näitab esmalt kunstitehnika tööde keskmist hinda ja suurust. Animatsiooni alustades näeb aastate kaupa keskmist hinda ja suurust.
''')

create_credits('''Copyright: Kanvas.ai''')
create_credits('''Autorid: Astrid Laupmaa, Julian Kaljuvee, Markus Sulg''')
create_credits('''Allikad: Haus kunsti oksjonid (1997-2022)''')
create_credits('''Muu: Inspireeritud Riivo Antoni loodud kunstiindeksist; <br>Heldet toetust pakkus <a href="https://tezos.foundation/">Tezos Foundation</a>''')
toc.generate()

@st.cache
def convert_df():
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return read_df('data/haus_cleaned.csv').to_csv().encode('utf-8')

csv = convert_df()
st.download_button(label="Laadi alla andmed",data=csv, file_name='haus_kunsti_indeks.csv', mime='text/csv')
