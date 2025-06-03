import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from calculate_price_logic import calculate_property_price  # Імпортуємо функцію з окремого файлу

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA])
server = app.server
app.title = "Оцінка вартості житла"

app.layout = dbc.Container([
    html.Br(),
    dbc.Card([
        dbc.CardHeader(html.H3("🏡 Оцінка вартості житла", className="text-center")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Вид житла:"),
                    dcc.Dropdown(
                        id="housing-type",
                        options=[
                            {"label": "Квартира", "value": "flat"},
                            {"label": "Приватний будинок", "value": "house"}
                        ],
                        value="flat"
                    )
                ], md=6),
                dbc.Col([
                    dbc.Label("Площа ділянки (сотки):"),
                    dbc.Input(id="land-size", type="number", min=0, placeholder="Лише для будинку"),
                ], md=6),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Площа житла (м²):"),
                    dbc.Input(id="home-size", type="number", min=1, value=50)
                ], md=4),
                dbc.Col([
                    dbc.Label("Кількість кімнат:"),
                    dbc.Input(id="rooms", type="number", min=1, value=2)
                ], md=4),
                dbc.Col([
                    dbc.Label("Кількість санвузлів:"),
                    dbc.Input(id="bathrooms", type="number", min=1, value=1)
                ], md=4),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Відстань до транспорту (хв):"),
                    dbc.Input(id="transport", type="number", min=0, value=5)
                ], md=6),
                dbc.Col([
                    dbc.Label("Відстань до магазину (хв):"),
                    dbc.Input(id="store", type="number", min=0, value=5)
                ], md=6),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Базова вартість сотки (грн):"),
                    dbc.Input(id="land-base", type="number", min=0, value=5000)
                ], md=6),
                dbc.Col([
                    dbc.Label("Базова вартість 1 м² (грн):"),
                    dbc.Input(id="sqm-base", type="number", min=0, value=15000)
                ], md=6),
            ], className="mb-3"),

            dbc.Button("🔍 Розрахувати", id="calc-btn", color="primary", className="w-100 mb-3"),

            html.Hr(),

            dbc.Alert(id="result-table", color="success", is_open=False, className="fw-bold")
        ])
    ])
], fluid=True)


@app.callback(
    Output("result-table", "children"),
    Output("result-table", "is_open"),
    Input("calc-btn", "n_clicks"),
    State("housing-type", "value"),
    State("land-size", "value"),
    State("home-size", "value"),
    State("rooms", "value"),
    State("bathrooms", "value"),
    State("transport", "value"),
    State("store", "value"),
    State("land-base", "value"),
    State("sqm-base", "value"),
)
def run_calc(n, housing_type, land_size, home_size, rooms, bathrooms, transport, store, land_base, sqm_base):
    if not n:
        return "", False

    data = {
        "housingType": housing_type,
        "landSize": land_size or 0,
        "homeSize": home_size,
        "rooms": rooms,
        "bathrooms": bathrooms,
        "transport": transport,
        "store": store,
        "landBasePrice": land_base or 0,
        "basePriceSqM": sqm_base
    }

    result = calculate_property_price(data)
    formatted = html.Ul([html.Li(f"{k}: {v}") for k, v in result.items()])
    return formatted, True


if __name__ == "__main__":
    app.run_server(debug=True)
