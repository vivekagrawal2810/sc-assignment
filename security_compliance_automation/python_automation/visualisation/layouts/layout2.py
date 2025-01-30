from dash import dcc, html
import plotly.express as px

def create_layout2(df):
    """Creates the layout for vendor compliance visualizations."""
    vendor_summary = df.groupby(["Vendor", "Status"]).size().reset_index(name="Count")
    fig = px.bar(
        vendor_summary,
        x="Vendor",
        y="Count",
        color="Status",
        barmode="group",
        title="Vendor Compliance Summary",
        color_discrete_sequence=[ "tomato","lightgreen"],
    )
    return html.Div([
        html.H2("Vendor Compliance Summary"),
        dcc.Graph(figure=fig)
    ])
