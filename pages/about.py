import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/about")

layout = dbc.Card([
    dbc.CardHeader(html.H3("About This Dashboard", className="mb-0 text-primary text-center")),
    dbc.CardBody([
        html.Div([
            html.H5("Who's this nerd?", className="mt-4"),
            html.Span("Thanks for asking. I'm "),
            html.A("Tom.", href="https://www.linkedin.com/in/tom-brisk/", target="_blank"),
            html.Span(" I'm an FY2 in the north of England and have started to enjoy dabbling in data science "),
            html.I("- weird, I know..."),
            html.Br(),
            html.Span(" Any queries / issues / concerns to be directed to tombrisk@gmail.com.")
        ]),
        html.P(""),
        html.H5("What is this?", className="mt-4"),
        html.P(
            "This dashboard is designed primarily to demonstrate the trends in competition for a UK specialty training place "
            "and make visualising the data easier than reading through tables on separate NHS webpages. "
            "It has not been designed to make any political points, nor has it been designed to guide career choices."
        ),

        html.P(
            "Data collected via the feedback form may be used as part of a publication in the future. "
            "The project and data collection has been discussed with a member of the local NHS trust's research team "
            "who has agreed that ethics approval is not needed."
        ),

        html.H5("Technical Notes", className="mt-4"),
        html.I("Boring but important bit"),
        html.P(""),

        html.P(
            "\"Average (outliers removed)\" has been calculated by removing any values with fewer than 100 applicants, "
            "and then applying a basic statistical technique to exclude outliers: any values less than or greater than "
            "1.5 times the interquartile range. A mean has then been calculated across all specialties remaining for each year."
        ),

        html.P(
            "\"Average (all specialties)\" is a simple mean of all the specialty competition ratios per year. "
            "Importantly, it is not weighted by number of applicants so will be skewed by niche specialties that are highly competitive."
        ),

        html.Span(
            "The data used is taken from "),
        html.A("NHS England", href="https://medical.hee.nhs.uk/medical-training-recruitment/medical-specialty-training/competition-ratios", target="_blank"),
        html.Span(" for competition ratios at ST1 / CT1 level. "
            "The future predictions are from a polynomial regression model (degree 4). These predictions are purely to illustrate "
            "recent trends rather than to guide or influence decision making. "
            "Polynomial regression can model complex, nonlinear relationships, but using high-degree polynomials on small datasets often"
            " leads to overfitting. For a deeper explanation, see "),
        html.A("this helpful article.", href="https://developers.google.com/machine-learning/crash-course/overfitting/overfitting", target="_blank"),
        html.Span(" Future competition ratios will almost certainly be "
            "very different to the predictions shown here due to the political nature of training place numbers. I will update the page with "
            "2025 data when it is released."
        ),
        html.P(""),

        html.P(
            "\"Oxbridge\" competition ratios refer to average competition ratios for entry to an undergraduate course at "
            "Oxford and Cambridge University (6:1). "
            "These have been included purely as a rudimentary comparison for something most people would consider \"highly competitive\"."
            " It's a bit silly, really. But I found it interesting."
        )
    ])
], className="shadow-sm my-4")


