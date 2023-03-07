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

df = read_df('data/auctions_clean.csv')
df = df[df["date"] >= 2001]
df = df[df["date"] <= 2021]
df = df.sort_values(by=["date"])
df_hist = read_df('data/historical_avg_price.csv')
df_hist = df_hist[df_hist["date"] >= 2001]
df_hist = df_hist.groupby("date").sum()

def change_value(change_from, change_to, column):
    df.loc[df[column]==change_from, column] = change_to
# Estonian categories and techniques
change_value("Oil paintings", "Õlimaalid", "category")
change_value("Other (non-oil) paintings", "Teised (mitte õli) maalid", "category")
change_value("Mixed medium", "Segatehnika", "category")
change_value("Graphics", "Graafika", "category")
change_value("Drawing", "Joonistus", "category")

change_value("Oil on canvas", "Õli lõuendil", "technique")
change_value("Oil on cardboard", "Õli papil", "technique")
change_value("Oil on wood", "Õli vineeril", "technique")
change_value("Aquatint", "Akvatinta", "technique")
change_value("Linoleum", "Linool", "technique")
change_value("Drawing", "Joonistus", "technique")
change_value("Gouache", "Guašš", "technique")
change_value("Watercolour", "Akvarell", "technique")
change_value("Tempera", "Tempera", "technique")
change_value("Acrylic", "Akrüül", "technique")
change_value("Etching", "Etsing", "technique")
change_value("Graphics", "Graafika", "technique")
change_value("Mixed tech", "Segatehnika", "technique")
change_value("Mixed technique", "Segatehnika", "technique")
change_value("Silk print", "Siiditrükk", "technique")
change_value("Vitrography", "Vitrograafia", "technique")
change_value("Wood cut", "Puugravüür", "technique")

kanvas_logo = get_img_with_href('data/horisontal-BLACK.png', 'https://kanvas.ai', '200px')
st.sidebar.markdown(kanvas_logo, unsafe_allow_html=True)

kanvas_logo = get_img_with_href('data/horisontal-BLACK.png', 'https://kanvas.ai', '400px')
st.markdown(kanvas_logo, unsafe_allow_html=True)

# TITLE
st.title('Eesti kunsti indeks')
toc.header('Ülevaade')
create_paragraph('''Kanvas.ai kunsti indeks on tööriist kunsti investeerijale.

Kanvas.ai kunsti indeks viimase 20 aasta (2001 kuni 2021) Eesti kunstioksjonite \nmüükide põhjal loodud andmebaas, eesmärgiga muuta kunst ja kunsti investeerimine \nlihtsamini mõistetavaks igale huvilisele.

Andmed on kogutud Eesti põhiliste galeriide avalike oksjoni tulemuste põhjal, mis \nannab ülevaate kuidas käitub kunstiturg ajas ning millised kunstimeediumid ning \nautorid on kõige parema investeerimise tootlikkusega.

Andmete põhjal on selgelt näha, kuidas kunsti populaarsus on viimastel aastatel \nsuure hüppe teinud nii hindades kui koguses. Näiteks on aastane hinna kasv ehk \ntootlikus mitme kunstivormi puhul üle 10% aastas. Õigesti valitud kunstiteos on \nhea valik, kuhu inflatsiooni eest oma raha paigutada.

Kanvas.ai kunstiindeksist puuduvad oksjoniväline kunsti info kuid meil on plaan \nhakata koguma ka NFTKanvas.ai lehel müüdud NFT kunstimeediumi andmeid.

Kunstiindeksi metoodika on praegu väljatöötamisel. Soovituste ja kommentaaridega saatke meile e-kiri info@kanvas.ai.
''')

# FIGURE - date and average price
toc.subheader('Joonis - Ajalooline hinnanäitaja')
fig = px.area(df_hist, x=df_hist.index, y="avg_price",
              labels={
                 "avg_price": "Ajalooline indeksinäitaja (€)",
                 "date": "Oksjoni aasta",
             })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)
create_paragraph('Ülalpoolne kunstiindeks annab ülevaate kunsti hinna tõusust ja langusest. Märgatava hüppe on kunsti hind teinud viimaste aastate jooksul. Alates pandeemiast on oksjoni turul kunsti investeerimise vastu huvi hüppeliselt tõusnud.')

# TABLE - categories average price
toc.subheader('Tabel - Ajalooline hinnanäitaja tehnikate kaupa')
table_data = create_table(df, category_column="category", category_list=df["category"].unique(), calculate_volume=False, table_height=150)
st.table(table_data)
create_paragraph('Meediumite ehk tehnika järgi järjestud vastavalt sellele, missugused meediumid domineerivad kõige kallimalt müüdud teoste hulgas.')

# FIGURE - date and volume
toc.subheader('Joonis - Ajalooline volüümi kasv')
fig = px.area(df_hist, x=df_hist.index, y="volume", 
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
toc.subheader('Tabel - Ajalooline volüümi kasv tehnikate kaupa')
table_data = create_table(df, category_column="category", category_list=df["category"].unique(), calculate_volume=True, table_height=150)
st.table(table_data)
create_paragraph('Sellest tabelist näeme, milline meedium on olnud kõige suurema käibega. Antud andmete põhjal võime näiteks näha, et graafika on kõige populaarsem ning kõige suurema käibe tõusu protsendiga.(Keskmiselt 204% 20 aasta jooksul ja õlimaalil samal ajal 35%)')

# FIGURE - treemap covering categories, techniques and authors by volume and overbid
toc.subheader('Joonis - Kunsti müügid tehnika ja kunstniku järgi')

df['start_price'] = df['start_price'].fillna(df['end_price'])
df['overbid_%'] = (df['end_price'] - df['start_price'])/df['start_price'] * 100
df['art_work_age'] = df['date'] - df['year']
df2 = df.groupby(['author', 'technique', 'category']).agg({'end_price':['sum'], 'overbid_%':['mean']})
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
create_paragraph('''Tehnikad ja kunstnikud, kus värviskaala annab meile protsentuaalse ülevaate, kui palju antud teos on oksjonil oma alghinnast ülepakutud ning tehnika ja eraldi kunstniku teoste käivet. 

Näiteks sinise tooniga on kunstnikud ja meediumid, mille puhul on oksjonil alghinnast ülepakkumine olnud kõige suurem. Kunstniku nime juurest võib lisaks ülepakkumis protsendile leida ka tema teoste käibe. Näiteks, kui kõige kallimalt müüdud teos kuulub Konrad Mäele, siis selle tabeli pealt võime välja lugeda, et kõige suurem ülepakkumine on tehtud hoopis Olev Subbi teostele, meediumiks tempera (711,69 % tõus alghinnast haamrihinnani, Konrad Mäel samal ajal vastav number õli papil meedium 59,06 % ja õli lõuendil 85,44%). Konrad Mäe kogu käive jääb siiski Subbi omast kõrgemaks.
''')

# FIGURE - treemap covering categories, techniques and authors by volume and overbid
toc.subheader('Joonis - Kunsti müügid tehnika ja kunstniku järgi')

table_data = create_table(df, category_column="author", category_list=list(df["author"].unique()), calculate_volume=False, table_height=250)
df["yearly_performance"] = [table_data[table_data["Autor"] == x]["Iga-aastane kasv (%)"] for x in df["author"]]
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
create_paragraph('''Selles tabelis on näha, millised kunstnikud on kõige populaarsemad ning nende kasvuprotsent. Protsent on arvutatud aastate vältel keskmise haamrihinna põhjal.

Selles tabelis on esikohal Konrad Mägi, kelle teoste väärtuse kasvuprotsent on keskmiselt 198,95%. Konrad Mäe kõrget kasvu protsenti on mõjutanud, kindlasti tema unikaalsus. Oksjonil esineb Konrad Mäe töid pigem harva. Teiselt kohalt leiame Eduard Wiiralti, kelle töid vastupidiselt Konrad Mäele liigub oksjonitel palju. Wiiralti alghinnad on madalamad ning ta on väga populaarne kogujate hulgas.
''')

# TABLE - best authors volume
toc.subheader('Tabel - Volüümi kasv Top 10 kunstnikul')
table_data = create_table(df, category_column="author", category_list=top_authors.index, calculate_volume=True, table_height=250)    
st.table(table_data)
create_paragraph('''Siin on näha kunstnike teoste käive ning selle keskmine tõus aastas. Antud tabelis on Wiiralt kaheksandal kohal ja esimesel Konrad Mägi. Kuna tabelis esitatud protsent on kogu perioodi (2001-2021) käibe peale, siis need kunstnikud, kelle töid on müüdud rohkem on sattunud ka tabeli etteotsa.
''')

# FIGURE - date and price
toc.subheader('Joonis - Kunstitöö vanus vs hind')
fig = px.scatter(df.dropna(subset=["decade"]), x="art_work_age", y="end_price", color="category",
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
create_paragraph('''Antud graafikult on võimalik kunstiteose vanuse ja tehnika järgi määrata teose hinda.
Tehnika on eraldatud värvide järgi. 

Kõige vanem teos pärineb aastast 1900, kuid ei ole kõige kallimalt müüdud. Üldiselt on näha, et vanemad teosed on kallimad, v.a Olev Subbi. Võib näha, et kõrgemalt on müüdud teise maailmasõja eelseid teoseid 1910-1940.
''')

# FIGURE - size and price
toc.subheader('Joonis - Kunstitöö pindala vs hind')
df["dimension"] = df["dimension"] / (1000*1000)
fig = px.scatter(df.dropna(subset=["dimension"]), x="dimension", y="end_price", color="category",
                 animation_frame="date", animation_group="technique", hover_name="technique",
                 size='date', hover_data=['author'], size_max=15, range_x=[-0.03,0.35], range_y=[-1000,100000],
                 labels={
                     "end_price": "Haamrihind (€)",
                     "dimension": "Pindala (m²)",
                     "author": "Autor",
                     "category": "Kategooria",
                  })
fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''Ülevaade teose mõõtmete, tehnika ja hinna seosest. Paljud väiksema formaadilised teosed on tihti kallimad, kui suured. Teose suurus ei tähenda, et kindlasti kallim on. Pigem on olulisem autor ning siis teose mõõt. Näiteks Konrad Mägi Õlimaal on mõõtgraafikul keskmiste hulgas, kuid hinna skaalal teistest tunduvalt kõrgemal (127 823 eurot haamrihind), samal ajal kõige suurema teose (Toomas Vint) haamrihind on 7094€.
''')

def create_credits(text):
    st.markdown('<span style="word-wrap:break-word;font-family:Source Code Pro;font-size: 14px;">' + text + '</span>', unsafe_allow_html=True)
create_credits('''Copyright: Kanvas.ai''')
create_credits('''Autorid: Astrid Laupmaa, Julian Kaljuvee, Markus Sulg''')
create_credits('''Allikad: Eesti avalikud kunsti oksjonid (2001-2021)''')
create_credits('''Muu: Inspireeritud Riivo Antoni loodud kunstiindeksist; <br>Heldet toetust pakkus <a href="https://tezos.foundation/">Tezos Foundation</a>''')
toc.generate()

@st.cache
def convert_df():
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return read_df('data/auctions_clean.csv').to_csv().encode('utf-8')

csv = convert_df()
st.download_button(label="Laadi alla andmed",data=csv, file_name='eesti_kunsti_indeks.csv', mime='text/csv')
