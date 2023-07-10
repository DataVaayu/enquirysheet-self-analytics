from dash import Dash, html, Input, Output, dcc, callback, dash_table
import plotly.express as px
import pandas as pd

#importing the data and filling the na values
data_enquiry_dash = pd.read_csv(r"D:\All Data\desktop\Enquiry Sheet and Design\Excel Reports\Retail Osaa Enquiry Sheet.xlsx - 2023.csv")
data_enquiry_dash.fillna("no data",inplace=True)

app = Dash(__name__)
server=app.server

app.layout = html.Div(children=[
    
            html.Div([html.H1(children="Drill Down Analysis",style={"textalign":"center","color":"rgb(0,0,0)"}),
            dcc.Dropdown(data_enquiry_dash.columns,value=["Platform","Category","Price Bracket"],id="dropdown-selection",multi=True),
            dcc.Graph(id="graph-content")]),
    
            html.Div([html.H1(children="Popular Category Analysis",style={"textalign":"center","color":"rgb(0,0,0)"}),
            dcc.Dropdown(["Category","Price Bracket","Outfit Tried","Outfit Bought","Color"],value="Color",id="dropdown-selection2"),
            dcc.Graph(id="graph-content2")]),
    
            html.Div([html.H1(children="Repeating Sentiment of Customers",style={"textalign":"center","color":"rgb(0,0,0)"}),
            dcc.Dropdown(["2","3","4"],value=2,id="dropdown-selection3"),            
            dcc.Graph(id="datatable-content")]),    
    
])    

@callback(
    
    Output("graph-content","figure"),
    Output("graph-content2","figure"),
    Output("datatable-content","figure"),
    Input("dropdown-selection","value"),    
    Input("dropdown-selection2","value"),
    Input("dropdown-selection3","value")
)



def update_graph(value,value2,value3):
    
    #Creating the sunburst drill-down analysis
    dff1 = data_enquiry_dash[value]
    
    #polular category analysis
    dff2 = data_enquiry_dash[value2]
    dff2=dff2.value_counts()
    dff2=dff2.reset_index()
    dff2.rename(columns={dff2.columns[0]:"Item",dff2.columns[1]:"Count"},inplace=True)
    dff2=dff2[dff2["Item"]!='no data']
    
    #n-grams analysis
    from nltk import ngrams
    from collections import Counter
    n_gram_list = []
    
    dff3 = data_enquiry_dash["Requirement"]
    n=int(value3)
    print(value3)
    for i_ in dff3:
        n_grams=ngrams(i_.split(),n)
        for j_ in n_grams:
            n_gram_list.append(" ".join(j_))
            
    n_gram_dict=Counter(n_gram_list)
    n_gram_df=pd.DataFrame(n_gram_dict.items(),columns=["Phrase","Count"])
    n_gram_df.sort_values("Count",ascending=False,inplace=True)
    fig3 = go.Figure()
    fig3.add_trace(go.Table(header=dict(values=list(n_gram_df.columns)),cells=dict(values=[n_gram_df.Phrase,n_gram_df.Count])))
    print(fig3.data)      
    
    
    return px.sunburst(dff1,path=value,height=700,width=1000), px.bar(dff2,x="Item",y="Count",text="Count",height=700,width=1500),fig3

if __name__ =="__main__":
    app.run(debug=True)
    