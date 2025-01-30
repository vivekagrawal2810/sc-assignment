from dash import dcc, html, Dash, Input, Output
from helpers.utils import load_json_data, json_to_dataframe,get_shared_data_file_path
from layouts.layout1 import create_layout1
from layouts.layout2 import create_layout2
from layouts.executive_layout import create_executive_layout, register_callbacks

# Load JSON data
json_data = load_json_data(get_shared_data_file_path())
all_standards = list(json_data.keys())  # Extract compliance standards
default_standard = all_standards[0] if all_standards else None

# Validate standards
if not default_standard:
    raise ValueError("No compliance standards found in the JSON data!")

# Initialize Dash app
app = Dash(__name__)
app.title = "Compliance Dashboard"

# App layout
app.layout = html.Div([
    # Dropdown for compliance standard
    html.Div([
        html.Label("Select Compliance Standard:"),
        dcc.Dropdown(
            id="compliance-standard-dropdown",
            options=[{"label": "PCI-DSS" if standard == "pci_dss" else "CIS", "value": standard} for standard in all_standards],
            value=default_standard,
            clearable=False
        )
    ], style={"marginBottom": "20px", "width": "50%"}),

    # Tabs for layouts
    dcc.Tabs(id="tabs", value="executive", children=[
        dcc.Tab(label="Executive Dashboard", value="executive"),
        dcc.Tab(label="Scan Results", value="layout1"),
        dcc.Tab(label="Vendor Compliance", value="layout2"),
    ]),
    html.Div(id="tabs-content")
])

# Callback for tab and dropdown interaction
@app.callback(
    Output("tabs-content", "children"),
    [Input("tabs", "value"),
     Input("compliance-standard-dropdown", "value")]
)
def update_layout(tab, compliance_standard):
    standard_data = json_data.get(compliance_standard, {})
    if not standard_data:
        return html.Div(f"No data available for: {compliance_standard}")
    
    df = json_to_dataframe(standard_data)
    if tab == "layout1":
        return create_layout1(app, df)
    elif tab == "layout2":
        return create_layout2(df)
    return create_executive_layout(df)

register_callbacks(app, json_data, json_to_dataframe)
if __name__ == "__main__":
    app.run_server(debug=True)
