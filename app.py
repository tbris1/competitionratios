import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from sqlalchemy import insert
from db_setup import Session, feedback_table
# Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Specialty Training Competition"

df = pd.read_csv("CompRatios.csv")
# For purpose of adding predicted data later, add 'Source' column
df['Source'] = 'Historical'

# Load and reshape predictions
df_predictions = pd.read_csv("predictions.csv")
df_predictions.rename(columns={'Predicted_Ratio_2025': 2025, 'Predicted_Ratio_2026': 2026}, inplace=True)
# Melt df as currently in wrong format [[Specialty, Predictions for 2025, Predictions for 2026]]
df_predictions_long = df_predictions.melt(id_vars='Specialty', var_name='Year', value_name='Ratio')
df_predictions_long['Year'] = df_predictions_long['Year'].astype(int)
df_predictions_long['Source'] = 'Predicted'

# Create average across all specialties for each year
df_total_ave = df.groupby('Year', as_index=False)['Ratio'].mean()
df_total_ave['Specialty'] = 'Average (all specialties)'
df_total_ave['Source'] = 'Historical'
merged_df = pd.concat([df, df_total_ave, df_predictions_long], ignore_index=True)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("UK Specialty Training Competition Ratios",
                        className="text-center text-primary pt-4 mb-4"), width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.Label("Select Specialty:", className="fw-bold"),
            dcc.Dropdown(
                id='specialty-dropdown',
                options=[{'label': spec, 'value': spec} for spec in merged_df['Specialty'].unique()],
                value='Average (all specialties)',
                clearable=False
            )
        ], width=3),

        dbc.Col([
            html.Label("Select Year Range:", className="fw-bold"),
            dcc.RangeSlider(
                id='year-slider',
                min=int(merged_df['Year'].min()),
                max=int(merged_df['Year'].max()),
                value=[2013, 2024],
                marks={int(year): str(year) for year in sorted(merged_df['Year'].unique())},
                step=1,
                tooltip={"placement": "bottom", "always_visible": False}
            )
        ], width=6),

        dbc.Col(html.Div([
            html.H6("Created by ", className="mb-1 d-inline"),
            html.A("Tom Brisk.", href="https://www.linkedin.com/in/tom-brisk/", target="_blank"),
            html.Br(),
            html.Span("Data from "),
            html.A("NHS England", href="https://medical.hee.nhs.uk/medical-training-recruitment/medical-specialty-training/competition-ratios", target="_blank"),
            " (ST1 / CT1).",
            html.Br(),
            html.Small("Predictions for 2025 and 2026 are based on a polynomial regression model using 2013–2024 data."),
            html.Sup(html.A("[1]", href="#footnote1")),
        ], className="text-center small"), width=3)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='competition-graph')
        ])
    ]),
    dbc.Row([html.Br()]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("📣 We'd Love Your Feedback", className="mb-0 text-primary")),
                dbc.CardBody([
                    dbc.Form([
                        # Training stage
                        dbc.Label("Which stage of training are you at?", className="fw-bold mt-2"),
                        dbc.RadioItems(
                            id="training-stage",
                            options=[
                                {"label": "Pre-Clinical Medical Student (Years 1-3)", "value": "PreClinicalMedicalStudent"},
                                {"label": "Clinical Medical student (Years 4-6)", "value": "ClinicalMedicalStudent"},
                                {"label": "FY1", "value": "FY1"},
                                {"label": "FY2", "value": "FY2"},
                                {"label": "Core Trainee and above", "value": "CoreTraineeAndAbove"}
                            ],
                            inline=True,
                            className="mb-3"
                        ),

                        # Usefulness score
                        dbc.Label("How useful did you find this dashboard?", className="fw-bold"),
                        dbc.RadioItems(
                            id="usefulness",
                            options=[
                                {"label": "1 - Not useful", "value": 1},
                                {"label": "2", "value": 2},
                                {"label": "3", "value": 3},
                                {"label": "4", "value": 4},
                                {"label": "5 - Extremely useful", "value": 5}
                            ],
                            inline=False,
                            className="mb-3"
                        ),

                        # Specialty interests
                        dbc.Label("Which specialty/specialties are you most interested in?", className="fw-bold"),
                        dbc.Checklist(
                            id="specialty-interest",
                            options=[{"label": spec, "value": spec}
                                     for spec in sorted(
                                    [s for s in merged_df["Specialty"].unique()
                                     if isinstance(s, str) and s != "Average (all specialties)"]
                                )]
                            ,
                            inline=False,
                            className="mb-3"
                        ),
                        html.Br(),
                        # Confidence slider
                        dbc.Label("Has your confidence in your specialty choice(s) changed after using the dashboard?",
                                  className="fw-bold"),
                        dcc.Slider(
                            id="confidence-slider",
                            min=0,
                            max=10,
                            step=1,
                            value=5,
                            marks={
                                0: {"label": "Less confident", 'style': {'fontSize': '16px', 'color': '#C00000'}},
                                5: {"label": "No change", 'style': {'fontSize': '16px', 'color': '#000000'}},
                                10: {"label": "More confident", 'style': {'fontSize': '16px', 'color': '#0c9e00'}}
                            },
                            tooltip={"placement": "bottom", "always_visible": False},
                            className="mb-4"
                        ),
                        html.Br(),

                        dbc.Label("How are you feeling about the current competition for specialty training?", className="fw-bold"),
                        dbc.Textarea(
                            id="feelings",
                            placeholder="Write your comments here...",
                            rows=1,
                            className="mb-4"
                        ),

                        # Free text
                        dbc.Label("Suggestions or other feedback?", className="fw-bold"),
                        dbc.Textarea(
                            id="suggestions",
                            placeholder="Write your comments here...",
                            rows=2,
                            className="mb-4"
                        ),

                        # Submit button + response
                        dbc.Button("Submit Feedback", id="submit-btn", color="primary", n_clicks=0),
                        html.Div(id="feedback-response", className="mt-3 text-success fw-semibold")
                    ])
                ])
            ], className="shadow-sm")
        ], width=10, className="mx-auto")
    ]),
    html.Br(),
    dbc.Row([
        html.P([
            "[1] Polynomial regression can model complex, nonlinear relationships, but using high-degree polynomials on small datasets often leads to overfitting. For a deeper explanation, see ",
            html.A("this helpful article.",
                   href="https://shonit2096.medium.com/over-fitting-in-polynomial-regression-ee67c2113344",
                   target="_blank"),
            " The future predictions in this graph have been included primarily to demonstrate recent increases in competition ratios rather to guide decision making.",
            html.Br(),
            "These predictions take no external factors into account. They are simply regression models based on previous competition ratio data."
        ], id='footnote1', style={'fontSize': '14px', 'color': '#393939'})
    ])
]),


    # Callback
@app.callback(
    Output('competition-graph', 'figure'),
    Input('specialty-dropdown', 'value'),
    Input('year-slider', 'value')
)
def update_graph(selected_specialty, selected_years):
    filtered_df = merged_df[
        (merged_df['Specialty'] == selected_specialty) &
        (merged_df['Year'] >= selected_years[0]) &
        (merged_df['Year'] <= selected_years[1])
    ]

    historical = filtered_df[filtered_df['Source'] == 'Historical']
    predicted = filtered_df[(filtered_df['Source'] == 'Predicted') | (filtered_df['Year'] == 2024)]

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

    fig.update_layout(
        title=f"<b>Competition Ratio for {selected_specialty}</b>",
        title_x=0.5,
        height=520,
        margin=dict(l=60, r=40, t=60, b=60),
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


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

