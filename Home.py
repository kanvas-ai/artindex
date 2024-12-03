import streamlit as st
from StreamlitHelper import Toc, get_img_with_href

# Page configuration
st.set_page_config(
    page_title="Art Index by Kanvas.ai",
    page_icon="data/Vertical-BLACK2.ico",
)

# Initialize Table of Contents
toc = Toc()
toc.placeholder(sidebar=True)

# Add Kanvas logo to sidebar
kanvas_logo = get_img_with_href('data/horisontal-BLACK.png', 'https://kanvas.ai', '200px')
st.sidebar.markdown(kanvas_logo, unsafe_allow_html=True)

# Main logo
kanvas_logo = get_img_with_href('data/horisontal-BLACK.png', 'https://kanvas.ai', '400px')
st.markdown(kanvas_logo, unsafe_allow_html=True)

# Title and Introduction
st.title('Welcome to Kanvas.ai Art Index')
toc.header('Overview')

st.markdown("""
Welcome to the Kanvas.ai Art Index platform! This tool provides comprehensive insights into the art market through various indices and analytics tools.

Here's what you can explore in our platform:
""")

# Estonian Index Section
toc.subheader('Estonian Art Index')
st.markdown("""
The Estonian Art Index provides detailed analysis of the Estonian art market over the past 20 years (2001-2021). You can access it in two languages:

- 🎨 **Estonian Index - EN**: Comprehensive analysis in English
- 🎨 **Estonian Index - EE**: Same analysis in Estonian

Key features:
- Historical price performance
- Volume analysis
- Artist rankings
- Technique-based analysis
""")

# Haus Gallery Section
toc.subheader('Haus Gallery Analysis')
st.markdown("""
Explore detailed analysis of Haus Gallery's auction data:

- 🖌️ **Haus Galerii - EN**: Analysis of Haus Gallery data in English
- 🖌️ **Haus Galerii - EE**: Analysis in Estonian

Features:
- Top 20 all-time artworks
- Top 50 classical works
- Top 50 modern works
- Graphics top 20
- Price and volume trends
""")

# AI Art Advisor Section
toc.subheader('AI Art Advisor')
st.markdown("""
Our 🖌️ **AI Art Advisor** is an innovative tool that helps you:

- Ask questions about art market trends
- Analyze specific artists or techniques
- Get insights about price developments
- Understand market dynamics

To use the AI Art Advisor, you'll need to:
1. Navigate to the AI Art Advisor page
2. Enter your OpenAI API key
3. Ask questions about the art market data
""")

# Data Sources Section
toc.subheader('Data Sources')
st.markdown("""
Our analyses are based on:
- Estonian public art auction sales (2001-2021)
- Haus Gallery auction data (1997-2022)
- Comprehensive artwork details including:
  - Prices
  - Dimensions
  - Techniques
  - Artists
  - Years
""")

# Credits
st.markdown("---")
st.markdown("""
<div style='font-size: 14px; font-family: Source Code Pro;'>
<p>Copyright: Kanvas.ai</p>
<p>Authors: Astrid Laupmaa, Julian Kaljuvee, Markus Sulg</p>
<p>Other credits: Inspired by the original Estonian Art Index created by Riivo Anton</p>
<p>Generous support from <a href="https://tezos.foundation/">Tezos Foundation</a></p>
</div>
""", unsafe_allow_html=True)

# Generate Table of Contents
toc.generate()
