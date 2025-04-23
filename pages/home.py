import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from data import merged_df

dash.register_page(__name__, path="/")


layout = dbc.Container([
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
                marks={
                    int(year): {
                        "label": str(year),
                        "style": {"color": "#000000", "fontWeight": "bold"} if year in [2025, 2026] else {}
                    }
                    for year in sorted(merged_df['Year'].unique())
                },
                step=1,
                tooltip={"placement": "bottom", "always_visible": False}
            )
        ], width=8),
        html.Br(),
        html.Br(),
        html.Br()
        ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='competition-graph')
        ])
    ]),
    dbc.Row([html.Br()]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("📣 We'd Love Your Feedback", className="mb-0 text-primary"), id='survey'),
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
                                {"label": "FY3 / Trust grade", "value": "OOT"},
                                {"label": "Core Trainee and above", "value": "CoreTraineeAndAbove"},
                                {"label": "Other", "value": "Other"}
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
                                     if isinstance(s, str) and s not in ["Average (all specialties)", "Average (outliers removed)"]]
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
            ], className="shadow-sm mb-4")
        ], width=10, className="mx-auto")
    ]),
    dcc.Interval(id="popup-timer", interval=30000, max_intervals=1),
    dbc.Modal([
        dbc.ModalHeader("Got 15 seconds to give some feedback? 📋"),
        dbc.ModalBody("Help us turn this into a QIP by filling out the super-quick feedback form below."),
        dbc.ModalFooter([
            dbc.Button("Dismiss", id="close-popup", className="ms-2", color="secondary")
        ])
    ], id="feedback-popup", is_open=False)

])



