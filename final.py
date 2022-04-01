import streamlit as st
import pandas as pd
import numpy as np
import keras
import yfinance as yf
import cufflinks as cf
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import chart_studio.plotly as plotly
import plotly.figure_factory as ff
import spacy
import os
from spacy import displacy
from bs4 import BeautifulSoup
import requests
import matplotlib
from plotly import graph_objs as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from datetime import date
from PIL import Image
from datetime import datetime
import lxml
from lxml import html

img = Image.open('/content/drive/MyDrive/png/Share.png')
st.set_page_config(page_title='$HARE BAZZA₹', page_icon=img)
 
 
 
hide_menu_style = """
<style>
 
footer {visibility: hidden; }
</style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)
 
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")
 
 
st.sidebar.title('Select Stocks')
stocks = ('ITC.NS','AMARAJABAT.NS',
 '3MINDIA.NS','ABB.NS','POWERINDIA.NS','ACC.NS','AIAENG.NS','APLAPOLLO.NS','AUBANK.NS',
 'AARTIDRUGS.NS','AARTIIND.NS','AAVAS.NS','ABBOTINDIA.NS','ADANIENT.NS','ADANIGREEN.NS',
 'ADANIPORTS.NS','ATGL.NS','ADANITRANS.NS','ABCAPITAL.NS','ABFRL.NS','ADVENZYMES.NS',
 'AEGISCHEM.NS','AFFLE.NS','AJANTPHARM.NS','AKZOINDIA.NS','ALEMBICLTD.NS','APLLTD.NS',
 'ALKEM.NS','ALKYLAMINE.NS','ALOKINDS.NS','AMARAJABAT.NS','AMBER.NS','AMBUJACEM.NS',
 'ANGELBRKG.NS','APOLLOHOSP.NS','APOLLOTYRE.NS','ASAHIINDIA.NS','ASHOKLEY.NS',
 'ASHOKA.NS','ASIANPAINT.NS','ASTRAZEN.NS','ASTRAL.NS','ATUL.NS','AUROPHARMA.NS',
 'AVANTIFEED.NS','DMART.NS','AXISBANK.NS','BASF.NS','BEML.NS','BSE.NS','BAJAJAUTO.NS',
 'BAJAJCON.NS','BAJAJELEC.NS','BAJFINANCE.NS','BAJAJFINSV.NS','BAJAJHLDNG.NS',
 'BALAMINES.NS','BALKRISIND.NS',
 'BALMLAWRIE.NS',
 'BANDHANBNK.NS','BANKBARODA.NS','BANKINDIA.NS','MAHABANK.NS','BATAINDIA.NS',
 'BAYERCROP.NS','BERGEPAINT.NS','BDL.NS','BEL.NS','BHARATFORG.NS','BHEL.NS','BPCL.NS',
 'BHARATRAS.NS','BHARTIARTL.NS','BIOCON.NS','BIRLACORPN.NS','BSOFT.NS','BLISSGVS.NS',
 'BLUEDART.NS','BBTC.NS','BOSCHLTD.NS','BRIGADE.NS','BRITANNIA.NS','BURGERKING.NS',
 'CCL.NS','CESC.NS','CRISIL.NS','CSBBANK.NS','CADILAHC.NS','CANFINHOME.NS','CANBK.NS',
 'CAPLIPOINT.NS','CGCL.NS','CARBORUNIV.NS','CASTROLIND.NS','CEATLTD.NS','CENTRALBK.NS',
 'CDSL.NS',
 'CENTURYTEX.NS','CERA.NS','CHALET.NS','CHAMBLFERT.NS','CHOLAHLDNG.NS','CHOLAFIN.NS',
 'CIPLA.NS','CUB.NS','COALINDIA.NS','COCHINSHIP.NS','COFORGE.NS','COLPAL.NS','CAMS.NS',
 'CONCOR.NS','COROMANDEL.NS','CREDITACC.NS','CROMPTON.NS','CUMMINSIND.NS',
 'CYIENT.NS',
 'DCMSHRIRAM.NS','DLF.NS','DABUR.NS','DALBHARAT.NS','DEEPAKNTR.NS','DELTACORP.NS',
 'DHANI.NS','DHANUKA.NS','DBL.NS','DISHTV.NS','DCAL.NS','DIVISLAB.NS','DIXON.NS',
 'LALPATHLAB.NS','DRREDDY.NS','EICHERMOT.NS','EIDPARRY.NS','EIHOTEL.NS','EPL.NS','EDELWEISS.NS',
 'ELGIEQUIP.NS','EMAMILTD.NS','ENDURANCE.NS','ENGINERSIN.NS','EQUITAS.NS','ERIS.NS',
 'ESCORTS.NS','EXIDEIND.NS','FDC.NS','FEDERALBNK.NS','FINEORG.NS','FINCABLES.NS',
 'FINPIPE.NS','FSL.NS','FORTIS.NS','FCONSUMER.NS','FRETAIL.NS','GAIL.NS','GEPIL.NS',
 'GMRINFRA.NS','GALAXYSURF.NS','GRSE.NS','GARFIBRES.NS','GICRE.NS','GILLETTE.NS',
 'GLAND.NS','GLAXO.NS','GLENMARK.NS','GODFRYPHLP.NS','GODREJAGRO.NS','GODREJCP.NS',
 'GODREJIND.NS','GODREJPROP.NS','GRANULES.NS','GRAPHITE.NS','GRASIM.NS','GESHIP.NS',
 'GREAVESCOT.NS', 'GUJALKALI.NS','GAEL.NS','FLUOROCHEM.NS','GUJGASLTD.NS','GNFC.NS','GPPL.NS','GSFC.NS',
 'GSPL.NS','GULFOILLUB.NS','HEG.NS','HCLTECH.NS','HDFCAMC.NS','HDFCBANK.NS',
 'HDFCLIFE.NS','HFCL.NS','HAPPSTMNDS.NS','HATSUN.NS','HAVELLS.NS','HEIDELBERG.NS',
 'HEROMOTOCO.NS','HSCL.NS','HINDALCO.NS','HAL.NS','HINDCOPPER.NS','HINDPETRO.NS',
 'HINDUNILVR.NS','HINDZINC.NS','HONAUT.NS','HUDCO.NS','HDFC.NS','HUHTAMAKI.NS',
 'ICICIBANK.NS','ICICIGI.NS','ICICIPRULI.NS','ISEC.NS','IDBI.NS','IDFCFIRSTB.NS','IDFC.NS',
 'IIFL.NS','IIFLWAM.NS','IOLCP.NS','IRB.NS','IRCON.NS','ITC.NS','ITI.NS','INDIACEM.NS',
 'IBULHSGFIN.NS','IBREALEST.NS','INDIAMART.NS','INDIANB.NS','IEX.NS','INDHOTEL.NS','IOC.NS',
 'IOB.NS','IRCTC.NS','ICIL.NS','INDOCO.NS',
 'INDUSTOWER.NS','INDUSINDBK.NS','INFIBEAM.NS','NAUKRI.NS','INFY.NS','INGERRAND.NS',
 'INOXLEISUR.NS','INTELLECT.NS','INDIGO.NS','IPCALAB.NS','JBCHEPHARM.NS','JKCEMENT.NS',
 'JKLAKSHMI.NS','JKPAPER.NS','JKTYRE.NS','JMFINANCIL.NS','JSWENERGY.NS','JSWSTEEL.NS',
 'JTEKTINDIA.NS',
 'JINDALSAW.NS','JSLHISAR.NS','JSL.NS','JINDALSTEL.NS','JCHAC.NS','JUBLFOOD.NS',
 'JUSTDIAL.NS','JYOTHYLAB.NS','KPRMILL.NS','KEI.NS','KNRCON.NS','KPITTECH.NS','KRBL.NS',
 'KSB.NS','KAJARIACER.NS','KALPATPOWR.NS','KANSAINER.NS','KARURVYSYA.NS','KSCL.NS',
 'KOTAKBANK.NS','L&TFH.NS','LTTS.NS','LICHSGFIN.NS','LAOPALA.NS','LAXMIMACH.NS','LTI.NS',
 'LT.NS','LAURUSLABS.NS','LEMONTREE.NS','LINDEINDIA.NS','LUPIN.NS','LUXIND.NS','MASFIN.NS',
 'MMTC.NS','MOIL.NS','MRF.NS','MGL.NS','MAHSCOOTER.NS',
 'M&MFIN.NS','M&M.NS','MAHINDCIE.NS','MHRIL.NS','MAHLOG.NS','MANAPPURAM.NS','MRPL.NS',
 'MARICO.NS','MARUTI.NS','MFSL.NS','MAXHEALTH.NS','MAZDOCK.NS','METROPOLIS.NS',
 'MINDTREE.NS','MINDACORP.NS','MINDAIND.NS','MIDHANI.NS','MOTILALOFS.NS','MPHASIS.NS',
 'MUTHOOTFIN.NS','NATCOPHARM.NS','NBCC.NS','NCC.NS','NESCO.NS','NHPC.NS','NLCINDIA.NS',
 'NMDC.NS','NOCIL.NS','NTPC.NS','NH.NS','NATIONALUM.NS','NFL.NS','NAVINFLUOR.NS',
 'NESTLEIND.NS','NETWORK18.NS','NILKAMAL.NS','NAM-INDIA.NS','OBEROIRLTY.NS',
 'OIL.NS','OFSS.NS','ORIENTELEC.NS','PIIND.NS','PNBHOUSING.NS','PNCINFRA.NS','PVR.NS',
 'PAGEIND.NS','PERSISTENT.NS','PETRONET.NS','PFIZER.NS','PHILIPCARB.NS','PHOENIXLTD.NS',
 'PIDILITIND.NS','PEL.NS','POLYMED.NS','POLYCAB.NS','POLYPLEX.NS','PFC.NS',
 'PRESTIGE.NS','PRINCEPIPE.NS','PRSMJOHNSN.NS','PGHL.NS','PGHH.NS','PNB.NS','QUESS.NS',
 'RBLBANK.NS','RECLTD.NS','RHIM.NS','RITES.NS','RADICO.NS','RVNL.NS','RAIN.NS',
 'RAJESHEXPO.NS','RALLIS.NS','RCF.NS','RATNAMANI.NS','RAYMOND.NS',
 'RELAXO.NS','RELIANCE.NS','RESPONIND.NS','ROSSARI.NS','ROUTE.NS','SBICARD.NS',
 'SBILIFE.NS','SIS.NS','SJVN.NS','SKFINDIA.NS','SRF.NS','SANOFI.NS','SCHAEFFLER.NS',
 'SCHNEIDER.NS','SEQUENT.NS','SHARDACROP.NS','SFL.NS','SHILPAMED.NS','SCI.NS',
 'SHREECEM.NS','SHRIRAMCIT.NS','SRTRANSFIN.NS','SIEMENS.NS','SOBHA.NS','SOLARINDS.NS',
 'SOLARA.NS','SONATSOFTW.NS','SPANDANA.NS','SPICEJET.NS','STARCEMENT.NS','SBIN.NS',
 'SAIL.NS','SWSOLAR.NS','STLTECH.NS','STAR.NS','SUDARSCHEM.NS','SUMICHEM.NS','SPARC.NS',
 'SUNTV.NS','SUNCLAYLTD.NS','SUNDARMFIN.NS','SUNDRMFAST.NS','SUNTECK.NS',
 'SUPRAJIT.NS','SUPREMEIND.NS','SUPPETRO.NS','SUVENPHAR.NS','SUZLON.NS',
 'SWANENERGY.NS','SYMPHONY.NS','SYNGENE.NS','TCIEXP.NS','TCNSBRANDS.NS',
 'TTKPRESTIG.NS','TV18BRDCST.NS','TVSMOTOR.NS','TANLA.NS',
 'TATACHEM.NS','TATACOFFEE.NS','TATACOMM.NS','TCS.NS','TATACONSUM.NS','TATAELXSI.NS',
 'TATAINVEST.NS','TATAMTRDVR.NS','TATAMOTORS.NS','TATAPOWER.NS','TATASTEEL.NS',
 'TEAMLEASE.NS','TECHM.NS','NIACL.NS','RAMCOCEM.NS','THERMAX.NS','THYROCARE.NS',
 'TIMKEN.NS','TITAN.NS',
 'TORNTPOWER.NS','TRENT.NS','TRIDENT.NS','TRITURBINE.NS','TIINDIA.NS','UCOBANK.NS',
 'UFLEX.NS','UPL.NS','UTIAMC.NS','UJJIVAN.NS','UJJIVANSFB.NS','ULTRACEMCO.NS',
 'UNIONBANK.NS','UBL.NS','MCDOWELL-N.NS','VGUARD.NS','VMART.NS','VIPIND.NS','VSTIND.NS',
 'VAKRANGEE.NS','VALIANTORG.NS','VTL.NS','VARROC.NS','VBL.NS','VEDL.NS','VENKEYS.NS',
 'VINATIORGA.NS','IDEA.NS','VOLTAS.NS','WABCOINDIA.NS','WELCORP.NS','WELSPUNIND.NS',
 'WESTLIFE.NS','WHIRLPOOL.NS','WIPRO.NS','WOCKPHARMA.NS','YESBANK.NS','ZEEL.NS',
 'ZYDUSWELL.NS','ECLERX.NS'
 
 
 
 
 
)
selected_stock = st.sidebar.selectbox('',stocks)
 
year = st.sidebar.slider('Years Of Prediction:', 1, 4)
period = year * 365
 
st.title('Predict Your Future')
 
@st.cache
def load_data(ticker):
     data = yf.download(ticker, START, TODAY)
     data.reset_index(inplace=True)
     return data
 
     
data_load_state = st.text('Loading Data...')
data = load_data(selected_stock)
data_load_state.text('Done!')
 
st.subheader(selected_stock)
st.write(data.tail())
 
 
 
 
 
def plot_fig():
     fig = go.Figure()
     fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open",line_color='098E1D'))
     fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close",line_color='F1190F'))
     fig.add_trace(go.Candlestick(x=data['Date'],open=data['Open'],high=data['High'],low=data['Low'],close=data['Close']))
     fig.layout.update(title_text='['+selected_stock+']' 'Chart View', xaxis_rangeslider_visible=True)
     st.plotly_chart(fig)
     
 
if st.checkbox('Market Depth'):
     st.subheader(selected_stock)
     st.write(data)
     
 
plot_fig()

st.header('**Bollinger Bands**')
qf=cf.QuantFig(data,title='First Quant Figure',legend='top',name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)
 
 
 
 
data_pred = data[['Date','Close']]
data_pred=data_pred.rename(columns={"Date": "ds", "Close": "y"})
 
 
 
m = Prophet()
m.fit(data_pred)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)
 
 
 
fig1 = plot_plotly(m, forecast)
if st.checkbox('Predicted Data'):
     st.subheader('['+selected_stock+']''Predicted data')
     st.write(forecast)
st.subheader('PREDICTION FOR: '+str(year)+'year')
st.plotly_chart(fig1)
 
 
 
st.subheader("Time Frame Forecast")
fig2 = m.plot_components(forecast)
st.write(fig2)
 
st.title('Events & Workshop')
st.write("$HARE BAZZA₹")
 
st.image(['/content/drive/MyDrive/png/Shareall.jpg'])
 
st.subheader('🙂Open Your Demat Account In Few Minutes🙂')
st.write('https://zerodha.com/open-account?c=OGY600')
 
