import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="My Stock Tracker", layout="wide")

# Main title
st.title("📈 :rainbow[Daily Stock Tracker]")
st.write("Automatically fetching the last 15 trading days of Open, High, Low, Close, Volume, and Latest News.")

# Complete dictionary of requested stocks and their Yahoo Finance tickers
stocks = {
    # --- Original List ---
    "Paras Defence & Space Tech": "PARAS.NS",
    "Data Patterns India": "DATAPATTNS.NS",
    "PTC Industries": "PTCIL.NS",
    "Servotech Power Systems": "SERVOTECH.NS",
    "Vedanta Ltd": "VEDL.NS",
    "Multi Commodity Exchange (MCX)": "MCX.NS",
    "NMDC Ltd": "NMDC.NS",
    "IFCI Ltd": "IFCI.NS",
    "Pro Fin Capital": "511557.BO",
    "Bartronics India Ltd (ASMS)": "ASMS.NS",
    "Goldstar Power": "GOLDSTAR.NS",
    "Zee Media": "ZEEMEDIA.NS",
    "Cella Space Limited": "532701.BO",
    "KPIT Technologies": "KPITTECH.NS",
    "JBM Auto Ltd": "JBMA.NS", 
    "SPML Infra Ltd": "SPMLINFRA.NS", 
    "KNR Constructions": "KNRCON.NS",

    # --- Defense, Shipbuilding & Aviation ---
    "Hindustan Aeronautics Ltd (HAL)": "HAL.NS",
    "Bharat Electronics Ltd (BEL)": "BEL.NS",
    "Bharat Dynamics Ltd (BDL)": "BDL.NS",
    "Mazagon Dock Shipbuilders": "MAZDOCK.NS",
    "Cochin Shipyard Ltd (CSL)": "COCHINSHIP.NS",
    "Zen Technologies Ltd": "ZENTEC.NS",
    "Astra Microwave Products": "ASTRAMICRO.NS",
    "MTAR Technologies Ltd": "MTARTECH.NS",
    "Garden Reach Shipbuilders (GRSE)": "GRSE.NS",
    "Mishra Dhatu Nigam (MIDHANI)": "MIDHANI.NS",
    "Knowledge Marine & Engineering (KMEW)": "KMEW.BO",
    
    # --- Banking & Finance ---
    "State Bank of India (SBI)": "SBIN.NS",
    "Bank of Baroda": "BANKBARODA.NS",
    "Canara Bank": "CANBK.NS",
    "UCO Bank": "UCOBANK.NS",
    "Union Bank of India": "UNIONBANK.NS",
    "Central Bank of India": "CENTRALBK.NS",
    "Bank of Maharashtra": "MAHABANK.NS",
    "Bank of India": "BANKINDIA.NS",
    "Punjab & Sind Bank": "PSB.NS",
    "Indian Overseas Bank": "IOB.NS",
    "Indian Bank": "INDIANB.NS",
    "Punjab National Bank": "PNB.NS",
    "General Insurance Corp (GICRE)": "GICRE.NS",
    "Life Insurance Corp (LIC)": "LICI.NS",
    "The New India Assurance Co": "NIACL.NS",
    "Power Finance Corp (PFC)": "PFC.NS",
    "REC Ltd": "RECLTD.NS",
    "Indian Railway Finance Corp (IRFC)": "IRFC.NS",
    "Housing & Urban Development (HUDCO)": "HUDCO.NS",

    # --- Energy, Oil & Gas ---
    "Bharat Petroleum (BPCL)": "BPCL.NS",
    "Hindustan Petroleum (HPCL)": "HINDPETRO.NS",
    "Indian Oil Corporation (IOC)": "IOC.NS",
    "Oil India Ltd": "OIL.NS",
    "Oil And Natural Gas Corp (ONGC)": "ONGC.NS",
    "Mangalore Refinery (MRPL)": "MRPL.NS",
    "NTPC Ltd": "NTPC.NS",
    "Coal India Ltd": "COALINDIA.NS",
    "SJVN Ltd": "SJVN.NS",
    "NHPC Ltd": "NHPC.NS",
    "GAIL (India) Ltd": "GAIL.NS",
    "Gujarat Gas Ltd": "GUJGASLTD.NS",
    "Power Grid Corp of India": "POWERGRID.NS",

    # --- Metals, Mining & Heavy Engineering ---
    "MMTC Ltd": "MMTC.NS",
    "Steel Authority of India (SAIL)": "SAIL.NS",
    "National Aluminium Co (NALCO)": "NATIONALUM.NS",
    "Hindustan Copper Ltd": "HINDCOPPER.NS",
    "NLC India Ltd": "NLCINDIA.NS",
    "KIOCL Ltd": "KIOCL.NS",
    "Bharat Heavy Electricals (BHEL)": "BHEL.NS",
    "Engineers India Ltd": "ENGINERSIN.NS",
    "Larsen & Toubro (L&T)": "LT.NS",

    # --- Railways & Infrastructure ---
    "Ircon International Ltd": "IRCON.NS",
    "Container Corp of India (CONCOR)": "CONCOR.NS",
    "NBCC (India) Ltd": "NBCC.NS",
    "IRCTC": "IRCTC.NS",
    "Rites Ltd": "RITES.NS",
    "Rail Vikas Nigam Ltd (RVNL)": "RVNL.NS",

    # --- Others ---
    "Rashtriya Chemicals & Fertilizers (RCF)": "RCF.NS",
    "ITI Ltd": "ITI.NS"
}

# --- NEW: Sidebar Index Creation ---
st.sidebar.header("🔍 Stock Index")
st.sidebar.write("Select a stock to view its data.")

# Create a list of options: "Overview" first, then all the company names alphabetically
options = ["Overview (All Stocks)"] + sorted(list(stocks.keys()))

# Create the dropdown selector in the sidebar
selected_option = st.sidebar.selectbox("Choose a view:", options)

# Filter the dictionary based on the user's selection
if selected_option == "Overview (All Stocks)":
    stocks_to_display = stocks
    st.info(f"Loading overview of all {len(stocks)} stocks. This may take a minute.")
else:
    # Create a mini-dictionary with just the one selected stock
    stocks_to_display = {selected_option: stocks[selected_option]}

# Function to fetch and process data
@st.cache_data(ttl=3600) 
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    
    try:
        news = stock.news[:3]
    except:
        news = []
    
    if not hist.empty:
        data = hist[['Open', 'High', 'Low', 'Close', 'Volume']].tail(15)
        data.index = data.index.strftime('%Y-%m-%d')
        data[['Open', 'High', 'Low', 'Close']] = data[['Open', 'High', 'Low', 'Close']].round(2)
        return data, news
    return pd.DataFrame(), news

# Layout: Create a grid of columns (only used if multiple stocks are displayed)
# If only one stock is selected, we just use a single column to make it nice and wide
num_cols = 2 if len(stocks_to_display) > 1 else 1
cols = st.columns(num_cols)

for index, (company_name, ticker) in enumerate(stocks_to_display.items()):
    col = cols[index % num_cols]
    
    with col:
        st.subheader(f":blue[{company_name}] ({ticker})")
        
        df, news = get_stock_data(ticker)
        
        if not df.empty:
            latest_close = df['Close'].iloc[-1]
            previous_close = df['Close'].iloc[-2]
            pct_change = ((latest_close - previous_close) / previous_close) * 100
            
            st.metric(
                label="Latest Close", 
                value=f"₹{latest_close:.2f}", 
                delta=f"{pct_change:.2f}%"
            )
            
            styled_df = df.style.background_gradient(subset=['Close'], cmap='Blues') \
                                .background_gradient(subset=['Volume'], cmap='Purples')
            
            st.dataframe(styled_df, use_container_width=True)
            
            chart_color = "#00FF00" if pct_change >= 0 else "#FF0000"
            st.line_chart(df['Close'], height=250 if num_cols == 1 else 200, color=chart_color)
            
            with st.expander("📰 View Latest News"):
                if news:
                    for article in news:
                        title = article.get('title', 'No Title Available')
                        link = article.get('link', '#')
                        publisher = article.get('publisher', 'Unknown Publisher')
                        st.markdown(f"- [{title}]({link}) *(Source: {publisher})*")
                else:
                    st.write("No recent news found for this ticker.")
            
        else:
            st.error(f"Could not fetch data for {company_name}")
            
        if num_cols > 1:
            st.divider()

st.caption(f"Data last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data provided by Yahoo Finance")