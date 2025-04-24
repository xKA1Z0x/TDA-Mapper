import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import json
import os
FIGURE_DIR = r"Y:\LabMembers\S Daneshgar\P2C\TDA\Results\3-18-2025 Sajjad\Interactive mapper"
figure_files = sorted([f for f in os.listdir(FIGURE_DIR) if f.endswith(".json")])
figure_files
# Create the Dash app
app = dash.Dash(__name__)
app.title = "Interactive Mapper Viewer"

# App layout
app.layout = html.Div([
    html.H2("Interactive Mapper Viewer"),
    
    dcc.Dropdown(
        id='figure-dropdown',
        options=[{'label': f.replace('.json', ''), 'value': f} for f in figure_files],
        value=figure_files[0],  # default selection
        style={'width': '60%'}
    ),
    
    dcc.Graph(id='plot-area', style={'height': '700px'})
])
# Helper for button groups
def make_button_group(id_prefix, options, default_value):
    return html.Div([
        html.Span(f"{id_prefix}: "),
        *[
            html.Button(
                label,
                id=f"{id_prefix}-{label}",
                n_clicks=0,
                style={"margin": "4px", "padding": "6px 10px"}
            )
            for label in options
        ]
    ], style={"margin-bottom": "10px"})

# Updated layout
app.layout = html.Div([
    html.H2("Interactive Mapper Viewer"),

    make_button_group("cube", ["8", "13", "18"], "13"),
    make_button_group("overlap", ["50", "59", "70"], "59"),
    make_button_group("condition", ["PD", "CVA", "HC", "LL"], "HC"),

    dcc.Graph(id='plot-area', style={'height': '700px'})
])
@app.callback(
    Output('plot-area', 'figure'),
    [Input(f"cube-{i}", "n_clicks") for i in ["8", "13", "18"]] +
    [Input(f"overlap-{i}", "n_clicks") for i in ["50", "59", "70"]] +
    [Input(f"condition-{i}", "n_clicks") for i in ["PD", "CVA", "HC", "LL"]]
)
def update_figure(*args):
    # Split button clicks into categories
    cube_clicks = args[0:3]
    overlap_clicks = args[3:6]
    condition_clicks = args[6:10]

    # Determine which button in each group was most recently clicked
    cube = ["8", "13", "18"][cube_clicks.index(max(cube_clicks))]
    overlap = ["50", "59", "70"][overlap_clicks.index(max(overlap_clicks))]
    condition = ["PD", "CVA", "HC", "LL"][condition_clicks.index(max(condition_clicks))]

    # Build filename
    filename = f"cube{cube}-perc{overlap}-{condition}.json"
    print("Loading figure:", filename)

    file_path = os.path.join(FIGURE_DIR, filename)

    try:
        with open(file_path, 'r') as f:
            fig_dict = json.load(f)
        return go.Figure(fig_dict)
    except Exception as e:
        print("Error loading figure:", e)
        return go.Figure()

if __name__ == '__main__':
    app.run(debug=True)