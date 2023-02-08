from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import json, urllib
import plotly.express as px
import pandas as pd                        # pip install pandas

# incorporate data into app
# Source - https://www.cdc.gov/nchs/pressroom/stats_of_the_states.htm
#   df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Good_to_Know/Dash2.0/social_capital.csv")
#   print(df.head())

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H4('Generalised Domestic Energy Cash flow, Oct 2021 - Dec 2022'),
    dcc.Graph(id="graph"),
    html.P("Opacity"),
    dcc.Slider(id='slider', min=0, max=1, 
               value=0.5, step=0.1)
])

@app.callback(
    Output("graph", "figure"), 
    Input("slider", "value"))
def display_sankey(opacity):
    url = 'https://raw.githubusercontent.com/B3thers/Data/main/DomEn.json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read()) # replace with your own data source

    node = data['data'][0]['node']
    node['color'] = [
        f'rgba(255,0,255,{opacity})' 
        if c == "magenta" else c.replace('0.8', str(opacity)) 
        for c in node['color']]

    link = data['data'][0]['link']
    link['color'] = [
        node['color'][src] for src in link['source']]

    fig = go.Figure(go.Sankey(link=link, node=node))
    fig.update_layout(font_size=10)
    return fig

if __name__ == "__main__":
    app.run_server(debug=False)
