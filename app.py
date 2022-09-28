import pandas as pd
import plotly
import plotly.express as px
import plotly.io as pio
from flask import Flask, redirect, jsonify, current_app, url_for, render_template, request,flash,g,session, Response,send_file, make_response,send_from_directory
import numpy as np
import json
import io
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

app = Flask(__name__)
i=0
names_1=[]
names_2=[]
names_3=[]
names_4=[]
nrx_1=[]
trx_1=[]
nrx_2=[]
trx_2=[]
nrx_3=[]
trx_3=[]
nrx_4=[]
trx_4=[]
nrx_5=[]
trx_5=[]
nrx_6=[]
trx_6=[]
data=[]

df = pd.read_csv('/home/veeva/mysite/static/Veeva_Prescriber_Data.csv',encoding='utf-8-sig', sep='\s*,\s*', engine='python', header = 0)
df['sumTRx']=df.TRx_Month_1 + df.TRx_Month_2 + df.TRx_Month_3 + df.TRx_Month_4 + df.TRx_Month_5 + df.TRx_Month_6
df['sumNRx']=df.NRx_Month_1 + df.NRx_Month_2 + df.NRx_Month_3 + df.NRx_Month_4 + df.NRx_Month_5 + df.NRx_Month_6
topFiveTRx = df.groupby(by=['Product','State'])['sumTRx'].nlargest(5).to_frame(name = 'TRx').reset_index()
df_new = pd.read_csv('/home/veeva/mysite/static/Veeva_Prescriber_Data_2.csv',header=0)


@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
def home():
    if request.method=='POST':
        names_1.clear()
        names_2.clear()
        names_3.clear()
        names_4.clear()
        state=request.form["state"]
        if state=='All':
            topFive = df.groupby(by=['Product'])['sumTRx'].nlargest(5).to_frame(name = 'TRx').reset_index()
            for i in range(len(topFive)):
                if topFive['Product'][i]=='Cholecap':
                    id=topFive['level_1'][i]
                    first_name=df['first_name'][id]
                    last_name=df['last_name'][id]
                    state=df['State'][id]
                    names_1.append(f'{first_name} {last_name}, {state}')
                    i+=1
                elif topFive['Product'][i]=='Zap-a-Pain':
                    id=topFive['level_1'][i]
                    first_name=df['first_name'][id]
                    last_name=df['last_name'][id]
                    state=df['State'][id]
                    names_2.append(f'{first_name} {last_name}, {state}')
                    i+=1
                elif topFive['Product'][i]=='Nasalclear':
                    id=topFive['level_1'][i]
                    first_name=df['first_name'][id]
                    last_name=df['last_name'][id]
                    state=df['State'][id]
                    names_3.append(f'{first_name} {last_name}, {state}')
                    i+=1
                else:
                    id=topFive['level_1'][i]
                    first_name=df['first_name'][id]
                    last_name=df['last_name'][id]
                    state=df['State'][id]
                    names_4.append(f'{first_name} {last_name}, {state}')
                    i+=1
        else:
            for i in range(len(topFiveTRx)):
                if topFiveTRx['State'][i]==state:
                    if topFiveTRx['Product'][i]=='Cholecap':
                        id=topFiveTRx['level_2'][i]
                        first_name=df['first_name'][id]
                        last_name=df['last_name'][id]
                        state=df['State'][id]
                        names_1.append(f'{first_name} {last_name}, {state}')
                        i+=1
                    elif topFiveTRx['Product'][i]=='Zap-a-Pain':
                        id=topFiveTRx['level_2'][i]
                        first_name=df['first_name'][id]
                        last_name=df['last_name'][id]
                        state=df['State'][id]
                        names_2.append(f'{first_name} {last_name}, {state}')
                        i+=1
                    elif topFiveTRx['Product'][i]=='Nasalclear':
                        id=topFiveTRx['level_2'][i]
                        first_name=df['first_name'][id]
                        last_name=df['last_name'][id]
                        state=df['State'][id]
                        names_3.append(f'{first_name} {last_name}, {state}')
                        i+=1
                    else:
                        id=topFiveTRx['level_2'][i]
                        first_name=df['first_name'][id]
                        last_name=df['last_name'][id]
                        state=df['State'][id]
                        names_4.append(f'{first_name} {last_name}, {state}')
                        i+=1
        return render_template('index.html',names_1=names_1,names_2=names_2,names_3=names_3,names_4=names_4)
    return render_template('index.html')

chart=pd.DataFrame()
@app.route("/prescribers",methods=["GET","POST"])
def prescribers():
    chart=pd.DataFrame()
    if request.method=='POST':
        level=request.form['prescriber']
        p25=np.percentile(df['sumTRx'],25)
        p50=np.percentile(df['sumTRx'],50)
        p75=np.percentile(df['sumTRx'],75)
        print(p25,p50,p75)
        if level=='0+':
            data=df[(df.sumTRx<p25)]
            first_name=data['first_name']
            last_name=data['last_name']
            state=data['State']
            product=data['Product']
            sumTRx=data['sumTRx']
            sumNRx=data['sumNRx']
            chart['First Name']=first_name
            chart['Last Name']=last_name
            chart['State']=state
            chart['Product']=product
            chart['Total Number of Prescriptions Over the Last Six Months']=sumTRx
        elif level=='25+':
            data=df[(df.sumTRx < p50) & (df.sumTRx>=p25)]
            first_name=data['first_name']
            last_name=data['last_name']
            state=data['State']
            product=data['Product']
            sumTRx=data['sumTRx']
            sumNRx=data['sumNRx']
            chart['First Name']=first_name
            chart['Last Name']=last_name
            chart['State']=state
            chart['Product']=product
            chart['Total Number of Prescriptions Over the Last Six Months']=sumTRx
        elif level=='50+':
            data=df[(df.sumTRx>=p50) & (df.sumTRx<p75)]
            first_name=data['first_name']
            last_name=data['last_name']
            state=data['State']
            product=data['Product']
            sumTRx=data['sumTRx']
            sumNRx=data['sumNRx']
            chart['First Name']=first_name
            chart['Last Name']=last_name
            chart['State']=state
            chart['Product']=product
            chart['Total Number of Prescriptions Over the Last Six Months']=sumTRx
        else:
            data=df[(df.sumTRx >= p75)]
            first_name=data['first_name']
            last_name=data['last_name']
            state=data['State']
            product=data['Product']
            sumTRx=data['sumTRx']
            sumNRx=data['sumNRx']
            chart['First Name']=first_name
            chart['Last Name']=last_name
            chart['State']=state
            chart['Product']=product
            chart['Total Number of Prescriptions Over the Last Six Months']=sumTRx
        print(f'This is my data {data}')
        return render_template('prescribers.html',tables=[chart.to_html()])
    return render_template('prescribers.html')

@app.route("/trends",methods=["GET","POST"])
def trends():
    if request.method=="POST":
        state=request.form['state']
        product=request.form['Medicine']
        for i in range(len(df_new)):
            if df_new['Product'][i]==product and df_new['State'][i]==state:
                data.append([df_new['Month'][i],df_new['NRx'][i],df_new['TRx'][i]])
                i+=1
            else:
                pass
        for items in data:
            if items[0]==1:
                nrx_1.append(items[1])
                trx_1.append(items[2])
            elif items[0]==2:
                nrx_2.append(items[1])
                trx_2.append(items[2])
            elif items[0]==3:
                nrx_3.append(items[1])
                trx_3.append(items[2])
            elif items[0]==4:
                nrx_4.append(items[1])
                trx_4.append(items[2])
            elif items[0]==5:
                nrx_5.append(items[1])
                trx_5.append(items[2])
            else:
                nrx_6.append(items[1])
                trx_6.append(items[2])
        df_filter=pd.DataFrame()
        df_filter['Month']=['1','2','3','4','5','6']
        df_filter['NRx']=[sum(nrx_1),sum(nrx_2),sum(nrx_3),sum(nrx_4),sum(nrx_5),sum(nrx_6)]
        df_filter['TRx']=[sum(trx_1),sum(trx_2),sum(trx_3),sum(trx_4),sum(trx_5),sum(trx_6)]
        fig = px.bar(x=df_filter['Month'], y =df_filter['TRx'],labels=dict(x="Months",y="Total Prescriptions"), title="Total Prescriptions per Month")
        fig.update_xaxes(type='category')
        ymax=max(df_filter['TRx'])
        fig.update_layout(yaxis_range=[0,ymax+500],title={'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})

        fig2 = px.bar(x=df_filter['Month'], y =df_filter['NRx'],labels=dict(x="Months",y="Total New Prescriptions"), title="Total New Prescriptions per Month")
        fig2.update_xaxes(type='category')
        ymax2=max(df_filter['NRx'])
        fig2.update_layout(yaxis_range=[0,ymax2+100],title={'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})

        # Group data together
        month_data = [df.TRx_Month_1, df.TRx_Month_2, df.TRx_Month_3, df.TRx_Month_4, df.TRx_Month_5, df.TRx_Month_6]
        month_labels = ['1', '2', '3', '4', '5', '6']

        # Create distplot with custom bin_size
        fig3 = px.histogram(df, x=df["sumTRx"], y=df["id"], marginal="box",labels=dict(x="Total Prescriptions Over the Past Six Months",y="Total Prescribers"),title="Total Prescriptions Per Doctoro Over the Past Six Months")
        fig3.update_layout(title={'text':"Total Prescriptions Per Doctor Over the Past Six Months", 'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},xaxis_title="Total Prescriptions Over the Past Six Months", yaxis_title="Total Prescribers")
        fig4 = px.histogram(df, x=df["sumNRx"], y=df["id"], marginal="box",labels=dict(x="Total New Presciptions Over the Past Six Months",y="Total Prescribers"), title="Total New Prescriptions Per Doctor Over the Past Six Months")
        fig4.update_layout(title={'text':"Total New Prescriptions Per Doctor Over the Past Six Months", 'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},xaxis_title="Total New Prescriptions Over the Past Six Months", yaxis_title="Total Prescribers")


        fig5 = px.scatter(df_filter, x=df_filter['Month'], y=df_filter['TRx'], trendline="ols",labels=dict(x="Months",y="Total Prescriptions"), title="Total Prescriptions Over Time")
        fig5.update_layout(title={'text':"Total Prescriptions Over Time",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},xaxis_title="Months", yaxis_title="Total Prescriptions")

        fig6=  px.scatter(df_filter, x=df_filter['Month'], y=df_filter['NRx'], trendline="ols",labels=dict(x="Months",y="Total New Prescriptions"), title="Total New Prescriptions Over Time")
        fig6.update_layout(title={'text':"Total New Prescriptions Over Time",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'},xaxis_title="Months", yaxis_title="Total Prescriptions")

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON6 = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('trends.html', graphJSON=graphJSON,graphJSON2=graphJSON2,graphJSON3=graphJSON3,graphJSON4=graphJSON4,graphJSON5=graphJSON5,graphJSON6=graphJSON6)
    return render_template('trends.html')

if __name__ == "__main__":
	app.run_server(debug=True)