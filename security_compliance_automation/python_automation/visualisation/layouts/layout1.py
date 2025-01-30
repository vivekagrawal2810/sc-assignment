from dash import dcc, html, dash_table

def create_layout1(app, df):
    """Creates the layout for showing scan results in a table."""
    short_width_cols = ["Status","Vendor","RuleID"]
    long_width_cols = ["ScanID","ScanDate","RuleDescription","Message"]

    return html.Div([
        html.H2("Scan Results"),
        dash_table.DataTable(
            id="scan-results-table",
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict("records"),
            style_data_conditional=[
                {
                    "if": {"column_id": "Status", "filter_query": "{Status} = 'FAIL'"},
                    "backgroundColor": "#FFCCCC",
                    "color": "black"
                },
                {
                    "if": {"column_id": "Status", "filter_query": "{Status} = 'PASS'"},
                    "backgroundColor": "#CCFFCC",
                    "color": "black"
                }
            ],
            style_cell={
            'whiteSpace': 'normal',  # Allow text wrapping
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',  # Show "..." for long text
            },
            style_table={'overflowX': 'auto'},  # Make table scrollable
            filter_action="native",
            sort_action="native",
            page_size=10
        )
    ])
