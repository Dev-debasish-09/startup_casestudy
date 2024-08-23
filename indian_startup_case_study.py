import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Devs Startup Analysis')

df = pd.read_csv('D:\Data_science\startup_casestudy\startup_funding.csv')

#drop remark columns
df.drop(columns = ['Remarks'],inplace = True)
#make sr no as index no
df.set_index('Sr No',inplace = True)
#changing the name of the col
df.rename(columns = {
    'Date dd/mm/yyyy':'date',
    'Startup Name':'startup',
    'Industry Vertical':'vertical',
    'SubVertical':'subvertical',
    'City  Location':'city',
    'Investors Name':'investors',
    'InvestmentnType':'round',
    'Amount in USD':'amount'
    
    },inplace = True)

# remove unwanted amount->convertto rupee->to cr
df['amount'] = df['amount'].fillna('0')
df['amount'] = df['amount'].str.replace(',','')
df['amount'] = df['amount'].str.replace('undisclosed','0')
df['amount'] = df['amount'].str.replace('Undisclosed','0')
df['amount'] = df['amount'].str.replace('unknown','0')
df = df[df['amount'].str.isdigit()]
df['amount']=df['amount'].astype('float')
#function to make dollar to rupee
def to_rupee(dollar):
    inr = dollar*82.6
    return inr/10000000
#apply to amount
df['amount'].apply(to_rupee)
#convert date string to date time format
pd.to_datetime(df['date'],errors='coerce')
#drop null value
df.dropna(subset=['date','startup','vertical','investors','round','amount'])
# fill the null space of investorname
df['investors']=df['investors'].fillna('Undisclosed')
#making the investors single one
sorted(set(df['investors'].str.split(',').sum()))


#maxing function of investor details
def load_investor(investor):
    st.title(investor)
    
    #load the recent 10 investment
    last_5_df = df[df['investors'].str.contains('investor')].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most recent Investment')
    st.dataframe(last_5_df)
    #two coloms
    col1 ,col2 = st.columns(2)

    with col1:
        #investors biggest investment
        biggest_investment_series= df[df['investors'].str.contains('investor')].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        st.dataframe(biggest_investment_series)
    with col2:
        #draw graph
        fig,ax = plt.subplots()
        ax.bar(biggest_investment_series.index,biggest_investment_series.values)
        ax.set_title('Investor Top 5 Investment')
        ax.set_xlabel('biggest_investment_series.index')
        ax.set_ylabel('biggest_investment_series.values')
        st.pyplot(fig)
        #create the pie chart
   
    v_series = df[df['investors'].str.contains('investor')].groupby('vertical')['amount'].sum()
    fig,ax = plt.subplots()


    col3,col4 = st.columns(2)
    with col3:
        ax.plot(v_series.index,v_series.values)
        ax.set_title('Invest sector')
        ax.set_xlabel('v_series.index')
        ax.set_ylabel('v_series.values')
        st.pyplot(fig)

    with col4:
        r_series = df[df['investors'].str.contains('investor')].groupby('round')['amount'].sum()
        fig,ax = plt.subplots()

        ax.pie(r_series,labels=r_series.index,autopct="%0.01f%%")
        ax.set_title('Invest round')
        ax.set_xlabel('r_series.index')
        ax.set_ylabel('r_series.values')
        st.pyplot(fig)
    col5,col6 = st.columns(2)
    with col5:
        c_series = df[df['investors'].str.contains('investor')].groupby('city')['amount'].sum()
        fig,ax = plt.subplots()

        ax.pie(c_series,labels=c_series.index,autopct="%0.01f%%")
        ax.set_title('Invest city')
        ax.set_xlabel('c_series.index')
        ax.set_ylabel('c_series.values')
        st.pyplot(fig)
    with col6:
        df['date'] =  pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year
        y_series = df[df['investors'].str.contains('investor')].groupby('year')['amount'].sum()
        fig, ax = plt.subplots()
        ax.plot(y_series.index,y_series.values)
        ax.set_title('Invest year by year')
        ax.set_xlabel('y_series.index')
        ax.set_ylabel('y_series.values')
        st.pyplot(fig)





st.sidebar.title('Start-up Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','Start-up','Investor'])
if option == 'Overall Analysis':
    st.title('Overall Analysis')
elif option == 'Start-up':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find The Startup Details')
    st.title('Start-up Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(df['investors'].unique().tolist()))
    btn2 = st.sidebar.button('Find The Investor Details')
    if btn2:
        load_investor(selected_investor)

    