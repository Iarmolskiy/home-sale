import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

def calculate_property_price(data):
    type_ = data['housingType']
    land_size = float(data.get('landSize', 0))
    home_size = float(data['homeSize'])
    rooms = int(data['rooms'])
    bathrooms = int(data['bathrooms'])
    transport = int(data['transport'])
    store = int(data['store'])
    land_base = float(data.get('landBasePrice', 0))
    sqm_base = float(data['basePriceSqM'])

    land_discount = 0
    if type_ == 'house':
        if land_size <= 4:
            land_discount = 0.25
        elif land_size <= 6:
            land_discount = 0.15
        elif land_size <= 10:
            land_discount = 0.05
        elif land_size <= 20:
            land_discount = 0
        elif land_size <= 40:
            land_discount = 0.10
        elif land_size <= 100:
            land_discount = 0.25
        else:
            land_discount = 0.40

    if home_size <= 20:
        home_discount = 0.25
    elif home_size <= 30:
        home_discount = 0.15
    elif home_size <= 40:
        home_discount = 0.10
    elif home_size <= 50:
        home_discount = 0.0
    elif home_size <= 60:
        home_discount = 0.10
    elif home_size <= 90:
        home_discount = 0.15
    else:
        home_discount = 0.25

    if rooms == 3:
        room_discount = 0.05
    elif rooms >= 4:
        room_discount = 0.07
    else:
        room_discount = 0.0

    bathroom_markup = 0.01 if bathrooms >= 2 else 0.0

    if transport <= 5:
        transport_discount = 0.0
    elif transport <= 10:
        transport_discount = 0.02
    else:
        transport_discount = 0.03

    if store <= 5:
        store_discount = 0.0
    elif store <= 10:
        store_discount = 0.01
    else:
        store_discount = 0.02

    land_cost = land_size * land_base * (1 - land_discount) if type_ == 'house' else 0
    home_cost = home_size * sqm_base * (1 - home_discount)
    home_cost *= (1 - room_discount)
    home_cost *= (1 + bathroom_markup)
    home_cost *= (1 - transport_discount)
    home_cost *= (1 - store_discount)

    total_price = land_cost + home_cost

    return {
        "Знижка за ділянку": f"{land_discount * 100:.0f}%" if type_ == 'house' else "N/A",
        "Знижка за площу житла": f"{home_discount * 100:.0f}%",
        "Знижка за кімнати": f"{room_discount * 100:.0f}%",
        "Націнка за сан.вузли": f"{bathroom_markup * 100:.0f}%",
        "Знижка за транспорт": f"{transport_discount * 100:.0f}%",
        "Знижка за магазин": f"{store_discount * 100:.0f}%",
        "Кінцева вартість житла (грн)": f"{total_price:,.2f}"
    }


app.layout = dbc.Container([
    html.H2("Оцінка вартості житла 🏠", className="text-center mt-4 mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Label("Вид житла"),
            dcc.Dropdown(
                id="housingType",
                options=[
                    {"label": "Квартира", "value": "flat"},
                    {"label": "Приватний будинок", "value": "house"},
                ],
                value="flat"
            ),
            dbc.Label("Площа ділянки (соток)"),
            dbc.Input(id="landSize", type="number", min=0, step=1),
            dbc.Label("Площа житла (кв.м)"),
            dbc.Input(id="homeSize", type="number", min=1, step=1),
            dbc.Label("Кількість кімнат"),
            dbc.Input(id="rooms", type="number", min=1),
            dbc.Label("Кількість санвузлів"),
            dbc.Input(id="bathrooms", type="number", min=1),
            dbc.Label("Хвилин до транспорту"),
            dbc.Input(id="transport", type="number", min=0),
            dbc.Label("Хвилин до магазину"),
            dbc.Input(id="store", type="number", min=0),
            dbc.Label("Ціна сотки (грн)"),
            dbc.Input(id="landBasePrice", type="number", min=0),
            dbc.Label("Ціна за кв.м (грн)"),
            dbc.Input(id="basePriceSqM", type="number", min=0),
            dbc.Button("Розрахувати", id="calcButton", color="primary", className="mt-3 w-100")
        ], md=6),

        dbc.Col([
            html.H4("Результат", className="text-center"),
            html.Div(id="result", className="mt-4")
        ], md=6)
    ])
], fluid=True)


@app.callback(
    Output("result", "children"),
    Input("calcButton", "n_clicks"),
    State("housingType", "value"),
    State("landSize", "value"),
    State("homeSize", "value"),
    State("rooms", "value"),
    State("bathrooms", "value"),
    State("transport", "value"),
    State("store", "value"),
    State("landBasePrice", "value"),
    State("basePriceSqM", "value"),
)
def update_output(n_clicks, housingType, landSize, homeSize, rooms, bathrooms,
                  transport, store, landBasePrice, basePriceSqM):
    if not n_clicks:
        return ""

    data = {
        "housingType": housingType,
        "landSize": landSize or 0,
        "homeSize": homeSize,
        "rooms": rooms,
        "bathrooms": bathrooms,
        "transport": transport,
        "store": store,
        "landBasePrice": landBasePrice or 0,
        "basePriceSqM": basePriceSqM
    }

    result = calculate_property_price(data)

    return html.Ul([html.Li(f"{k}: {v}") for k, v in result.items()])


if __name__ == "__main__":
    app.run_server(debug=True)
