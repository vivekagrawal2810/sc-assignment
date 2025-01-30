from dash import dcc, html,Input, Output,State
import plotly.express as px
from io import BytesIO
from reportlab.pdfgen import canvas
import dash

def create_executive_layout(df):
   
    overall_compliance_score = (
        (df["Status"] == "PASS").sum() / len(df) * 100
    )  # Calculate compliance percentage
    total_failed = (df["Status"] == "FAIL").sum()
    total_passed = (df["Status"] == "PASS").sum()

    pie_chart = px.pie(
        values=[total_passed, total_failed],
        names=["Passed", "Failed"],
        title="Overall Compliance Status",
        color_discrete_sequence=["lightgreen", "tomato"],
    )

   # pie_chart.write_image("pie_chart.png")


    return html.Div([
        html.H1("Executive Dashboard", style={"textAlign": "center"}),

        html.Div([
            html.Div(f"Overall Compliance Score: {overall_compliance_score:.2f}%", style={"fontSize": 20}),
            html.Div(f"Total Failed Rules: {total_failed}", style={"fontSize": 20}),
            html.Div(f"Total Passed Rules: {total_passed}", style={"fontSize": 20}),
        ], style={"textAlign": "center", "marginBottom": "20px"}),

        dcc.Graph(id="compliance-score-pie", figure=pie_chart),
          # Download Button
        html.Button("Download Executive Summary (PDF)", id="download-pdf-button"),
        dcc.Download(id="download-pdf")
       
    ])
def register_callbacks(app, json_data, json_to_dataframe):
   
    @app.callback(
        Output("download-pdf", "data"),
        Input("download-pdf-button", "n_clicks"),
        State("compliance-standard-dropdown", "value"),
    )
    def download_pdf(n_clicks, compliance_standard):
        if not n_clicks:
            return dash.no_update

        # Get the data for the selected standard
        standard_data = json_data.get(compliance_standard, {})
        if not standard_data:
            return dash.no_update
        
        df = json_to_dataframe(standard_data)
        total_rules = len(df)
        failed_rules = df[df["Status"] == "FAIL"].shape[0]
        pass_percentage = ((total_rules - failed_rules) / total_rules) * 100

        # Prepare data for the PDF
        pdf_data = {
            "total_rules": total_rules,
            "failed_rules": failed_rules,
            "pass_percentage": pass_percentage,
        }

        # Generate the PDF
        pdf_buffer = generate_pdf(pdf_data)
        return dcc.send_bytes(pdf_buffer.getvalue(), filename="executive_summary.pdf")
# PDF generation logic
def generate_pdf(data):
    """Generates a PDF from executive summary data."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer)

    # Add a title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, "Executive Summary Report")

    # Add details
    c.setFont("Helvetica", 12)
    c.drawString(100, 770, f"Total Rules: {data['total_rules']}")
    c.drawString(100, 750, f"Failed Rules: {data['failed_rules']}")
    c.drawString(100, 730, f"Compliance Percentage: {data['pass_percentage']:.2f}%")

    #c.drawImage("pie_chart.png", 100, 500, width=400, height=300)

    # Finalize the PDF
    c.save()
    buffer.seek(0)
    return buffer


 