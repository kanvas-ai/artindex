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

            print(date, last_year)

            price_change = (end_sum - start_sum) / start_sum * 100 / (date-last_year)
            price_changes.append(price_change) # Kasvu arvutus
            prices.append(end_sum) # Jätame meelde selle aasta hinna
            last_year = date
        annual_return = round(np.mean(price_changes), 4)
        total_return = round(annual_return * len(dates), 4)
        category_returns.append([cat, total_return, annual_return])
        
    df_cat_returns = pd.DataFrame(category_returns, columns=["Kategooria", "Kogukasv algusest (%)", "Iga-aastane kasv (%)"]) 
    df_cat_returns = df_cat_returns.sort_values(by="Iga-aastane kasv (%)", ascending=False)
    return df_cat_returns.drop("Kogukasv algusest (%)", axis=1)

def create_paragraph(text):
    st.markdown('<span style="word-wrap:break-word;">' + text + '</span>', unsafe_allow_html=True)

df = read_df('data/auctions_clean.csv')
df = df[df["date"] >= 2001]
df = df[df["date"] <= 2021]
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
st.title('Eesti kunsti indeks')
st.header('Ülevaade')
create_paragraph('''Kanvas.ai kunsti indeks on tööriist kunsti investeerijale.

Kanvas.ai kunsti indeks viimase 20 aasta (2001 kuni 2021) Eesti kunstioksjonite \nmüükide põhjal loodud andmebaas, eesmärgiga muuta kunst ja kunsti investeerimine \nlihtsamini mõistetavaks igale huvilisele.

Andmed on kogutud Eesti põhiliste galeriide avalike oksjoni tulemuste põhjal, mis \nannab ülevaate kuidas käitub kunstiturg ajas ning millised kunstimeediumid ning \nautorid on kõige parema investeerimise tootlikkusega.

Andmete põhjal on selgelt näha, kuidas kunsti populaarsus on viimastel aastatel \nsuure hüppe teinud nii hindades kui koguses. Näiteks on aastane hinna kasv ehk \ntootlikus mitme kunstivormi puhul üle 10% aastas. Õigesti valitud kunstiteos on \nhea valik, kuhu inflatsiooni eest oma raha paigutada.

Kanvas.ai kunstiindeksist puuduvad oksjoniväline kunsti info kuid meil on plaan \nhakata koguma ka NFTKanvas.ai lehel müüdud NFT kunstimeediumi andmeid.''')

# FIGURE - date and average price
st.subheader('Joonis - Ajalooline hinnanäitaja')
fig = px.area(df_hist, x=df_hist.index, y="avg_price",
              labels={
                 "avg_price": "Ajalooline indeksinäitaja (€)",
                 "date": "Oksjoni aasta",
             })
st.plotly_chart(fig, use_container_width=True)
create_paragraph('Ülalpoolne kunstiindeks annab ülevaate kunsti hinna tõusust ja langusest. Märgatava hüppe on kunsti hind teinud viimaste aastate jooksul. Alates pandeemiast on oksjoni turul kunsti investeerimise vastu huvi hüppeliselt tõusnud.')

# TABLE - categories average price
st.subheader('Tabel - Ajalooline hinnanäitaja kategooriate kaupa')
table_data = create_table(df, category_column="category", category_list=df["category"].unique(), calculate_volume=False, table_height=150)
st.table(table_data)
create_paragraph('Meediumite ehk tehnika järgi järjestud vastavalt sellele, missugused meediumid domineerivad kõige kallimalt müüdud teoste hulgas.')

# FIGURE - date and volume
st.subheader('Joonis - Ajalooline volüümi kasv')
fig = px.area(df_hist, x=df_hist.index, y="volume", 
             labels={
                 "volume": "Volüüm (€)",
                 "date": "Oksjoni aasta",
             })
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''Volüümi kasv annab meile ülevaate, kui palju on ajas tõusnud ja langenud oksjonite käive. 
Näiteks 2001 aastal oli oksjoni käive 174.000- euro ringis, siis 2021 aastal oli oksjonite käive 4.5miljonit. Kindlasti on väga oluline roll krooni asendumisel euroga ja juurde on tulnud oksjoni galeriisid.  Sellegipoolest on kunsti müük märkimisväärse hüppe teinud alates 2019, mis on 20 aasta lõikes kõige suurem. Viimane suurem muutus toimus 2006-2009 majanduskriisi mõjutustest.
''')

# TABLE - categories volume
st.subheader('Tabel - Ajalooline volüümi kasv kategooriate kaupa')
table_data = create_table(df, category_column="category", category_list=df["category"].unique(), calculate_volume=True, table_height=150)
st.table(table_data)
create_paragraph('Sellest tabelist näeme, milline meedium on olnud kõige suurema käibega. Antud andmete põhjal võime näiteks näha, et graafika on kõige populaarsem ning kõige suurema käibe tõusu protsendiga.(Keskmiselt 204% 20 aasta jooksul ja õlimaalil samal ajal 34%)')

# FIGURE - treemap covering categories, techniques and authors by volume and overbid
st.subheader('Joonis - Kunsti müügid kategooria ja kunstniku järgi')

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
                     "overbid_%": "Ülepakkumine (%)",
                     "total_sales": "Kogumüük",
                     "author": "Autor",
                  })
fig.update_traces(hovertemplate='<b>%{label} </b> <br> Kogumüük: %{value}<br> Ülepakkumine (%): %{color:.2f}',)
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''Kategooriad ja kunstnikud, kus värviskaala annab meile protsentuaalse ülevaate, kui palju antud teos on oksjonil oma alghinnast ülepakutud ning kategooria ja eraldi kunstniku teoste käivet. 

Näiteks sinise tooniga on kunstnikud ja meediumid, mille puhul on oksjonil alghinnast ülepakkumine olnud kõige suurem. Kunstniku nime juurest võib lisaks ülepakkumis protsendile leida ka tema teoste käibe. Näiteks, kui kõige kallimalt müüdud teos kuulub Konrad Mäele, siis selle tabeli pealt võime välja lugeda, et kõige suurem ülepakkumine on tehtud hoopis Olev Subbi teostele, meediumiks tempera (711, 69 % tõus alghinnast haamrihinnani, Konrad Mäel samal ajal vastav number õli papil meedium 59,06 % ja õli lõuendil 86,58%). Konrad Mäe kogu käive jääb siiski Subbi omast kõrgemaks.
''')


# TABLE - best authors average price
author_sum = df.groupby(["author"], sort=False)["end_price"].sum()
top_authors = author_sum.sort_values(ascending=False)[:10]

st.subheader('Tabel - Top 10 parimat kunstnikku')
table_data = create_table(df, category_column="author", category_list=top_authors.index, calculate_volume=False, table_height=250)    
st.table(table_data)

# TABLE - best authors volume
st.subheader('Tabel - Volüümi kasv Top 10 kunstnikul')
table_data = create_table(df, category_column="author", category_list=top_authors.index, calculate_volume=True, table_height=250)    
st.table(table_data)

# FIGURE - date and price
st.subheader('Joonis - Kunstitöö vanus vs hind')
fig = px.scatter(df.dropna(subset=["decade"]), x="art_work_age", y="end_price", color="category",
                 size='decade', hover_data=['author'],
                 labels={
                     "end_price": "Haamrihind (€)",
                     "art_work_age": "Kunstitöö vanus",
                     "author": "Autor",
                     "category": "Kategooria",
                     "decade": "Kümnend"
                  })
st.plotly_chart(fig, use_container_width=True)
create_paragraph('''Antud graafikult on võimalik kunstiteose vanuse ja tehnika järgi määrata teose hinda.
Tehnika on eraldatud värvide järgi. 

Kõige vanem teos pärineb aastast 1900, kuid ei ole kõige kallimalt müüdud. Üldiselt on näha, et vanemad teosed on kallimad, v.a Olev Subbi. Võib näha, et kõrgemalt on müüdud teise maailmasõja eelseid teoseid 1910-1940.
''')

# FIGURE - size and price
st.subheader('Joonis - Kunstitöö pindala vs hind')
df["dimension"] = df["dimension"] / (1000*1000)
fig = px.scatter(df.dropna(subset=["dimension"]), x="dimension", y="end_price", color="category",
                 size='dimension', hover_data=['author'],
                 labels={
                     "end_price": "Haamrihind (€)",
                     "dimension": "Pindala (m²)",
                     "author": "Autor",
                     "category": "Kategooria",
                  })

st.plotly_chart(fig, use_container_width=True)
create_paragraph('''Ülevaade teose mõõtmete, tehnika ja hinna seosest. Paljud väiksema formaadilised teosed on tihti kallimad, kui suured. Teose suurus ei tähenda, et kindlasti kallim on. Pigem on olulisem autor ning siis teose mõõt. Näiteks Konrad Mägi Õlimaal on mõõtgraafikul keskmiste hulgas, kuid hinna skaalal teistest tunduvalt kõrgemal (127 823 eurot haamrihind), samal ajal kõige suurema teose (Toomas Vint) haamrihind on 7094€.
''')

st.text('Copyright: Kanvas.ai')
st.text('Autorid: Astrid Laupmaa, Julian Kaljuvee, Markus Sulg')
st.text('Allikad: Eesti avalikud kunsti oksjonid (2001-2021)')
st.text('Muu: Inspireeritud Riivo Antoni loodud kunstiindeksist')

