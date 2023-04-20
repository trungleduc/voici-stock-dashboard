from datetime import datetime
from typing import Dict, List
import json
import ipyvuetify as v
import ipywidgets as ipw
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

v.theme.dark = True
import re


def camel_case_split(string: str):
    cap = string[0].upper() + string[1:]
    list_str = re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", cap)
    return " ".join(list_str)


def new_factory(news: List[Dict]) -> v.Html:
    children = []
    for new in news:
        date = datetime.fromtimestamp(new["providerPublishTime"])
        btn = v.Btn(
            small=True,
            text=True,
            block=True,
            children=["Open"],
            href=new["link"],
            target="_blank",
        )
        card = v.Card(
            outlined=True,
            children=[
                v.CardTitle(
                    children=[new["title"]],
                    style_="font-size: 1.1rem",
                ),
                v.CardSubtitle(
                    children=[
                        f'{new["publisher"]} ({date.strftime("%m/%d/%Y, %H:%M")})'
                    ]
                ),
                v.CardActions(children=[btn]),
            ],
        )
        children.append(card)
    return v.Html(tag="div", class_="d-flex flex-column", children=children)


def financial_info_factory(data: List[Dict], logo_url: str = None) -> v.Html:
    children = []
    if logo_url is not None:
        logo = v.Card(
            outlined=True,
            class_="ma-1",
            children=[v.Img(src=logo_url, height="100px", contain=True)],
            style_="width: calc(14.28% - 8px); min-width: 150px",
        )
        children.append(logo)

    for item in data:
        card = v.Card(
            outlined=True,
            class_="ma-1",
            children=[
                v.CardTitle(
                    primary_title=True,
                    children=[item["title"]],
                    style_="font-size: 18px; color: #51ef98",
                ),
                v.CardText(children=[str(item["value"])]),
            ],
            style_="width: calc(14.28% - 8px); min-width: 150px",
        )
        children.append(card)
    return v.Html(
        tag="div",
        class_="d-flex flex-row",
        children=children,
        style_="flex-wrap: wrap",
    )


def price_chart_factory(df: List, ticker: str = "") -> ipw.Widget:
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    keys = df["Open"].keys()
    index = [datetime.fromtimestamp(int(timestamp) / 1000).strftime("%Y-%m-%d") for timestamp in keys]
    openData = list(df["Open"].values())
    highData = list(df["High"].values())
    lowData = list(df["Low"].values())
    closeData = list(df["Close"].values())
    volume = list(df["Volume"].values())
    # include candlestick with rangeselector
    fig.add_trace(
        go.Candlestick(
            x=index,
            open=openData,
            high=highData,
            low=lowData,
            close=closeData,
            name="OHLC",
        ),
        secondary_y=True,
    )
    fig.add_trace(
        go.Bar(
            x=index,
            y=volume,
            marker_color="rgba(91, 91, 91, 0.73)",
            name="Volume",
        ),
        secondary_y=False,
    )

    fig.layout.yaxis2.showgrid = False
    fig.update_layout(
        autosize=True,
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        title={
            "text": f"{ticker.upper()} PRICE CHART",
            "xanchor": "center",
            "yanchor": "top",
            "x": 0.5,
        },
    )
    widget = go.FigureWidget(fig, layout=ipw.Layout(height="100%"))
    return widget


def price_history_factory(df: List, ticker: str = "") -> ipw.Widget:
    keys = df["Close"].keys()
    index = [datetime.fromtimestamp(int(timestamp) / 1000).strftime("%Y-%m-%d") for timestamp in keys]
    closeData = list(df["Close"].values())
    widget = go.FigureWidget(go.Scatter(x=index, y=closeData))
    widget.update_layout(
        autosize=True,
        template="plotly_dark",
        title={
            "text": f"{ticker.upper()} PRICE HISTORY",
            "xanchor": "center",
            "yanchor": "top",
            "x": 0.5,
        },
    )
    return widget


def text_widget(title: str, text: str) -> ipw.Widget:
    return v.Card(
        outlined=True,
        children=[
            v.CardTitle(
                children=[title],
                style_="font-size: 1.1rem",
            ),
            v.CardText(children=[text]),
        ],
    )


def balance_sheet_factory(df) -> ipw.Widget:
    props = [k for k in df[0].keys() if k != "asOfDate"]
    items = [{"name": camel_case_split(prop)} for prop in props]
    headers = [
        {
            "text": "Property",
            "align": "start",
            "sortable": False,
            "value": "name",
        }
    ]

    for data in df:
        asOf = data["asOfDate"]
        date = datetime.fromtimestamp(int(asOf) / 1000).strftime("%Y-%m-%d")
        for idx, key in enumerate(props):
            items[idx][str(asOf)] = data[key]

        headers.append(
            {
                "text": date,
                "value": str(asOf),
            }
        )

    return v.DataTable(
        headers=headers,
        items=items,
    )


def analysis_factory(df) -> ipw.Widget:
    items = []
    for i in range(df.shape[0]):
        row = df.iloc[i]
        item = {"name": row.name}
        item.update(json.loads(row.to_json()))
        items.append(item)
    titles = [x for x in items[0].keys() if x != "name"]
    headers = [
        {
            "text": "Property",
            "align": "start",
            "sortable": False,
            "value": "name",
        }
    ]
    for title in titles:
        header = {"text": title, "value": title}
        headers.append(header)
    return v.DataTable(
        headers=headers,
        items=items,
    )
