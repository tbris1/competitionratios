import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from sqlalchemy import insert
from db_setup import Session, feedback_table
from data import merged_df

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

GA_TRACKING_CODE = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-223CESF5SH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-223CESF5SH');
</script>
"""

app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Specialty Training Competition Dashboard</title>
        {GA_TRACKING_CODE}
        {{%metas%}}
        {{%favicon%}}
        {{%css%}}
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

app.layout = dbc.Container([
    dbc.Nav([
        dbc.NavLink("Home", href="/", active="exact"),
        dbc.NavLink("About", href="/about", active="exact")
    ], pills=True, className="mt-3"),
    dash.page_container
])

    # Callback for graph
@app.callback(
    Output('competition-graph', 'figure'),
    Input('specialty-dropdown', 'value'),
    Input('year-slider-desktop', 'value'),
    # Input('year-slider-mobile', 'value')
)
def update_graph(selected_specialty, selected_years_desktop):

    # trigger = ctx.triggered_id
    #
    # if trigger == 'years-slider mobile' and selected_years_mobile:
    #     selected_years = selected_years_mobile
    # elif trigger == 'year-slider-desktop' and selected_years_desktop:
    #     selected_years = selected_years_desktop
    # else:
    #     selected_years = selected_years_mobile if selected_years_desktop is None else selected_years_desktop

    selected_years = selected_years_desktop

    filtered_df = merged_df[
        (merged_df['Specialty'] == selected_specialty) &
        (merged_df['Year'] >= selected_years[0]) &
        (merged_df['Year'] <= selected_years[1])
    ]

    historical = filtered_df[filtered_df['Source'] == 'Historical']
    historical = historical.sort_values('Year')
    predicted = filtered_df[(filtered_df['Source'] == 'Predicted') | (filtered_df['Year'] == 2024)]
    predicted = predicted.sort_values('Year')

    fig = go.Figure()

    # Historical line
    fig.add_trace(go.Scatter(
        x=historical['Year'],
        y=historical['Ratio'],
        mode='lines+markers',
        name='Historical',
        line=dict(color='#1f77b4', width=3, dash='solid'),
        marker=dict(size=6),
        hovertemplate="Year: %{x}<br>Ratio: %{y}<extra></extra>"
    ))

    # Predicted line
    fig.add_trace(go.Scatter(
        x=predicted['Year'],
        y=predicted['Ratio'],
        mode='lines+markers',
        name='Predicted',
        line=dict(color='#1f77b4', width=3, dash='dot'),
        marker=dict(size=6, symbol='circle-open'),
        hovertemplate="Year: %{x}<br>Predicted: %{y}<extra></extra>"
    ))

    # Add Oxbridge line
    fig.add_trace(go.Scatter(
        x=historical['Year'],
        y=[6] * len(historical['Year']),
        mode='lines',
        name='Oxbridge',
        line=dict(color='#950000', width=3, dash='dot'),
        opacity=0.5,
        showlegend=True,
        visible='legendonly'
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>Competition Ratio for: {selected_specialty}</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=16)
        ),
        title_x=0.5,
        height=560,
        margin=dict(l=60, r=40, t=80, b=20),
        plot_bgcolor='white',
        paper_bgcolor='#f9f9f9',
        font=dict(family="Arial", size=14, color='black'),
        xaxis=dict(
            title='Year',
            gridcolor='#eeeeee',
            linecolor='black',
            showline=True,
            ticks='outside',
            tickmode='linear',
            dtick=1  # Forces 1-year intervals only
        ),
        yaxis=dict(
            title='Competition Ratio',
            gridcolor='#eeeeee',
            linecolor='black',
            showline=True,
            ticks='outside'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.35,
            xanchor="center",
            x=0.5,
            title=None,
            font=dict(size=14)
        ),
        hovermode='x unified'

    )

    return fig

@app.callback(
    Output('feedback-response', 'children'),
    Input('submit-btn', 'n_clicks'),
    Input('training-stage', 'value'),
    Input('usefulness', 'value'),
    Input('specialty-interest', 'value'),
    Input('confidence-slider', 'value'),
    Input('feelings', 'value'),
    Input('suggestions', 'value')
)
def submit_feedback(n_clicks, stage, usefulness, specialty, confidence, feelings, suggestions):
    if n_clicks:
        try:
            print("Submit button clicked!")

            timestamp = datetime.now()
            specialty_str = ', '.join(specialty) if specialty else ''

            print("Collected inputs:",
                  stage, usefulness, specialty_str, confidence, feelings, suggestions)

            session = Session()

            stmt = insert(feedback_table).values(
                timestamp=timestamp,
                training_stage=stage or "",
                usefulness=usefulness or 0,
                specialty=specialty_str,
                confidence=confidence or 0,
                feelings=feelings or "",
                suggestions=suggestions or ""
            )

            session.execute(stmt)
            session.commit()
            session.close()

            return dbc.Alert("✅ Thanks for submitting your feedback!", color='success')

        except Exception as e:
            print("❌ Error while submitting:", e)
            return dbc.Alert(f"❌ Error: {e}", color='danger')

    return dash.no_update

# Add pop up to prompt feedback
@dash.callback(
    Output("feedback-popup", "is_open"),
    [Input("popup-timer", "n_intervals"), Input("close-popup", "n_clicks")],
    [dash.State("feedback-popup", "is_open")]
)
def toggle_popup(n_intervals, n_clicks, is_open):
    if n_clicks:
        return False
    if n_intervals:
        return True
    return is_open


server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)

