import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from dash import Dash, html, dcc, Input, Output, callback

df = pd.read_csv("China.csv")
df = df.sort_values(by="Year")

fig = go.Figure()

colors = [
    "#117733",
    "#000",
    "#88ccee",
    "#999933",
    "#882255",
    "#cc6677",
    "#d55e00",
    "#44aa99",
    "#ddcc77",
    "#332288",
    "#aa4499",
    "#ddd",
]

attributes = [
    "coal",
    "oil",
    "gas",
    "Energy",
    "Fugi",
    "FC",
    "CO2 MARBUNK",
    "CO2 AVBUNK",
    "CO2-TES",
    "CO2-GDP",
    "CO2-GDP PPP",
    "CO2-POP",
]

for i, col in enumerate(attributes):
    fig.add_trace(
        go.Scatter(
            x=list(df.Year),
            y=list(df[col]),
            name=col,
            line=dict(color=colors[i % len(colors)]),
            marker=dict(color=colors[i % len(colors)]),
        )
    )

fig.update_layout(plot_bgcolor="white")
fig.update_xaxes(
    mirror=True,
    ticks="outside",
    showline=True,
    linecolor="black",
    gridcolor="lightgrey",
)
fig.update_yaxes(
    mirror=True,
    ticks="outside",
    showline=True,
    linecolor="black",
    gridcolor="lightgrey",
)
fig.update_layout(title=dict(text="Actual Greenhouse Emissions in China"))
fig.update_layout(hovermode="x unified")


df_lowest = df.loc[df["Year"] == 1971].melt(var_name="Attribute", value_name="Value")
df_highest = df.loc[df["Year"] == 2021].melt(var_name="Attribute", value_name="Value")

fig2 = go.Figure()
fig2.add_trace(
    go.Bar(
        x=df_lowest["Attribute"][2:],
        y=df_lowest["Value"][2:],
        name=df_lowest["Value"].iloc[1],
    )
)

fig2.add_trace(
    go.Bar(
        x=df_highest["Attribute"][2:],
        y=df_highest["Value"][2:],
        name=df_highest["Value"].iloc[1],
    )
)

fig2.update_layout(plot_bgcolor="white", width=500)
fig2.update_xaxes(
    mirror=True,
    ticks="outside",
    showline=True,
    linecolor="black",
    gridcolor="white",
)
fig2.update_yaxes(
    mirror=True,
    ticks="outside",
    showline=True,
    linecolor="black",
    gridcolor="lightgrey",
)
fig2.update_layout(title=dict(text="Emissions Growth Over The Years"))



def create_timeseries_chart(df, attribute):
    fig3 = go.Figure()
    fig3.update_layout(showlegend=False)

    fig3.add_trace(go.Scatter(x=df["Year"], y=df[attribute], mode="lines"))
    fig3.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        title=f"{attribute} Prediction",
    )
    return dcc.Graph(figure=fig3)


divs_timeseries = []
for attribute in attributes:
    divs_timeseries.append(html.Div(create_timeseries_chart(df, attribute)))


def predicting_values(df, attribute, selected_range):
    historical_data = df[df["Year"] <= df["Year"].max()]

    initial_values = historical_data[
        historical_data["Year"] == historical_data["Year"].max()
    ][attribute].iloc[0]

    predicted_years = np.arange(df["Year"].max(), df["Year"].max() + selected_range + 1)
    predicted_values = []

    if attribute == "coal":
        diff = 0.958181405
    elif attribute == "oil":
        diff = 0.975838003
    elif attribute == "gas":
        diff = 0.981606674

    if attribute in ["coal", "oil", "gas"]:
        for year in predicted_years:
            if year == df["Year"].max():
                predicted_values.append(initial_values)
            else:
                initial_values = initial_values * diff
                predicted_values.append(initial_values)
    else:
        for year in predicted_years:
            if year == 2021:
                predicted_values.append(initial_values)
            else:
                coal_value = historical_data[historical_data["Year"] == 2021][
                    "coal"
                ].iloc[0] * (0.958181405 ** (year - 2021))
                oil_value = historical_data[historical_data["Year"] == 2021][
                    "oil"
                ].iloc[0] * (0.975838003 ** (year - 2021))
                gas_value = historical_data[historical_data["Year"] == 2021][
                    "gas"
                ].iloc[0] * (0.981606674 ** (year - 2021))
                if attribute == "Energy":
                    x1 = 1.05408192168614
                    x2 = 1.0609875788184
                    x3 = 0.930551833114963
                    c = 75.780406144242
                elif attribute == "Fugi":
                    x1 = 55.2147357349027
                    x2 = 55.7209319135846
                    x3 = 0.930551833114963
                    c = -54.6684558372447
                elif attribute == "FC":
                    x1 = 0.998867185883502
                    x2 = 1.00526664767438
                    x3 = 0.985220287660759
                    c = 67.4491328290705
                elif attribute == "CO2 MARBUNK":
                    x1 = 0.00189418347036375
                    x2 = 0.00921755298134628
                    x3 = 0.0169152723753817
                    c = -0.881610327945175
                elif attribute == "CO2 AVBUNK":
                    x1 = 0.00127573095530592
                    x2 = 0.0124705358071595
                    x3 = -0.00119155208659054
                    c = -4.47360813698833
                elif attribute == "CO2-TES":
                    x1 = 0.00171632487824995
                    x2 = 0.0274804047452477
                    x3 = -0.0578450535030414
                    c = 48.0469811364253
                elif attribute == "CO2-GDP":
                    x1 = 0.0000855082589487124
                    x2 = -0.00430724491771043
                    x3 = 0.00546978711021504
                    c = 3.44213683261782
                elif attribute == "CO2-GDP PPP":
                    x1 = 0.0000531458120897602
                    x2 = -0.00267731437109122
                    x3 = 0.00340018932769287
                    c = 2.13960478774652
                else:
                    x1 = 0.000767091509274247
                    x2 = 0.000151336787045177
                    x3 = 0.000600262787090968
                    c = 0.420288600803255

                initial_values = x1 * coal_value + x2 * oil_value + x3 * gas_value + c

                predicted_values.append(initial_values)

    return predicted_values, predicted_years


def create_combined_timeseries_chart(df, attribute, selected_range):
    historical_data = df[df["Year"] <= df["Year"].max()]

    fig = go.Figure()
    fig.update_layout(showlegend=False)

    fig.add_trace(
        go.Scatter(
            x=historical_data["Year"],
            y=historical_data[attribute],
            mode="lines",
            name="Historical Data",
        )
    )
    predicted_values, predicted_years = predicting_values(df, attribute, selected_range)

    fig.add_trace(
        go.Scatter(
            x=predicted_years,
            y=predicted_values,
            mode="lines",
            line=dict(dash="dash"),
            name="Predicted Data",
        )
    )

    fig.update_layout(plot_bgcolor="white", height=300)
    fig.update_xaxes(
        mirror=True,
        ticks="outside",
        showline=True,
        linecolor="black",
        gridcolor="lightgrey",
    )
    fig.update_yaxes(
        mirror=True,
        ticks="outside",
        showline=True,
        linecolor="black",
        gridcolor="lightgrey",
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        title=f"{attribute} Prediction",
    )
    return dcc.Graph(figure=fig)


fig4 = go.Figure()


df_copy = df.copy()
df_copy["Total_Value"] = df.iloc[:, 2:].sum(axis=1)
fig4.add_trace(
    go.Scatter(
        x=list(df_copy.Year),
        y=list(df_copy["Total_Value"]),
        name="Total Emission (Actual)",
    )
)

predicted_data = {}

for col in attributes:
    predicted_values, predicted_years = predicting_values(df, col, 67)
    predicted_data["Years"] = predicted_years
    predicted_data[col] = predicted_values

predicted_data = pd.DataFrame(predicted_data)
predicted_data["Total_Value"] = predicted_data.iloc[:, 1:].sum(axis=1)
fig4.add_trace(
    go.Scatter(
        x=list(predicted_data.Years),
        y=list(predicted_data["Total_Value"]),
        mode="lines",
        line=dict(dash="dash"),
        name="Total Emission (Prediction)",
    )
)

fig4.update_layout(plot_bgcolor="white")
fig4.update_xaxes(
    mirror=True,
    ticks="outside",
    showline=True,
    linecolor="black",
    gridcolor="lightgrey",
)
fig4.update_yaxes(
    mirror=True,
    ticks="outside",
    showline=True,
    linecolor="black",
    gridcolor="lightgrey",
)
fig4.update_layout(title=dict(text="Total Emissions"))
fig4.update_layout(hovermode="x unified")
fig4.update_layout(
    margin=dict(l=0, r=0, t=30, b=0),
    legend=dict(orientation="h", yanchor="bottom", y=-0.15),
)


donut_data = predicted_data[
    predicted_data["Years"] == predicted_data["Years"].min() + 67
].melt(var_name="Attribute", value_name="Value")

fig5 = go.Figure(
    data=[
        go.Pie(
            labels=donut_data["Attribute"][1:-1],
            values=donut_data["Value"][1:-1],
            hole=0.3,
            marker_colors=colors,
        )
    ]
)

fig5.update_traces(
    textinfo="none",
)
fig5.update_layout(
    margin=dict(l=0, r=0, t=30, b=0),
    title="Percentage Breakdown of Predicted Emissions in Year 2088",
)


desired_attribute = "Energy"
year_value = df["Year"][:-1]
value_att = df[desired_attribute][:-1]
value_coal = df['coal'][:-1]
value_oil = df['oil'][:-1]
value_gas = df['gas'][:-1]
animate_y_coal, animate_x_coal = predicting_values(df, "coal", 100)
animate_y_oil, animate_x_oil = predicting_values(df, "oil", 100)
animate_y_gas, animate_x_gas = predicting_values(df, "gas", 100)
animate_y_desired, animate_x_desired = predicting_values(df, desired_attribute, 100)

year_value = pd.concat([year_value, pd.Series(animate_x_coal)])
value_att = pd.concat([value_att, pd.Series(animate_y_desired)])
value_coal = pd.concat([value_coal, pd.Series(animate_y_coal)])
value_oil = pd.concat([value_oil, pd.Series(animate_y_oil)])
value_gas = pd.concat([value_gas, pd.Series(animate_y_gas)])

animate_data = pd.DataFrame({
    'Year': year_value,
    'coal': value_coal,
    'oil': value_oil,
    'gas': value_gas,
    desired_attribute: value_att
})

data_melted = animate_data.melt(id_vars='Year', var_name='Attribute', value_name='Value')

fig_animation = px.bar(
    data_melted,
    x="Attribute",
    y="Value",
    title="Oil, Gas, Coal, and CO2/GHG Emission Over Time",
    animation_frame="Year",
    range_y=[0, 12000],
) 

app = Dash(__name__, title="What can we do about GHG/CO2 emissions?")
server = app.server

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    "What can we do about GHG/CO2 emissions?",
                    className="header-text title",
                ),
                html.Div(
                    "Dataset is taken from the International Energy Agency (iea.org).",
                    className="header-text",
                ),
            ],
            className="header",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            "Greenhouse Gas Emissions in China",
                            className="subtitle",
                        ),
                        html.Div(
                            "Ever since 2006, China has led the world in emissions of heat-trapping gases. In 2021, more than 30% of heat-trapping gases emitted globally came from China. Its cumulative emissions since the beginning of Industrial Revolution are 15% of the global total (second only to the United States) and growing fast.",
                            className="p",
                        ),
                        html.Div(
                            [
                                dcc.Store(id="memory-output"),
                                dcc.Dropdown(
                                    options=[
                                        {"label": col, "value": col}
                                        for col in attributes
                                    ],
                                    id="memory-field",
                                    multi=True,
                                    value=attributes,
                                ),
                            ],
                            className="dropdown-menu",
                        ),
                        dcc.Graph(figure=fig, id="line-plot", className="main-plot"),
                        dcc.Graph(figure=fig2, id="compare-plot"),
                        html.Div(
                            dcc.RangeSlider(
                                df["Year"].min(),
                                df["Year"].max(),
                                1,
                                count=1,
                                marks=None,
                                value=[df["Year"].min(), df["Year"].max()],
                                id="year-slider",
                                tooltip={"placement": "bottom", "always_visible": True},
                                className="custom-slider",
                            ),
                            className="slider-container",
                        ),
                    ],
                    className="inner-container border",
                ),
                html.Div(
                    [
                        html.Div(
                            "Predicting Upcoming Emission in China",
                            className="subtitle",
                        ),
                        html.Div(
                            [
                                dcc.Dropdown(
                                    options=attributes[3:],
                                    value="Energy",
                                    id="fig-animation-dropdown",
                                ),
                                html.Div("Background", className="section-title"),
                                html.Div(
                                    "As the world's largest energy consumer and carbon emitter, China's emissions reductions over the coming decades will be important in determining the succession of global warning prevention from exceeding 1.5 °C. In September 2020, President Xi Jinping announced that China will 'aim' to have CO2 emissions peak before 2030 and achieve carbon neutrality before 2060."
                                ),
                                html.Div(
                                    "This will be possible by relying in three key areas: energy deficiency, renewables, and reducing coal use. By 2060, it is prognosticated that the demand for coal will drop by more than 80%, oil by 60%, and natural gas by 45%."
                                ),
                                html.Div(
                                    "Based on this policy, we decided to do regression models for coal, oil, and gas over 9 other attributes to see the change it might take over years if this policy is to happen."
                                ),
                                dcc.Link(
                                    "IEA (2021), An energy sector roadmap to carbon neutrality in China, IEA, Paris https://www.iea.org/reports/an-energy-sector-roadmap-to-carbon-neutrality-in-china, License: CC BY 4.0",
                                    href="https://www.iea.org/reports/an-energy-sector-roadmap-to-carbon-neutrality-in-china/executive-summary",
                                    className="citation",
                                ),
                                html.Div("Regression Model", className="section-title"),
                                dcc.Markdown(
                                    mathjax=True,
                                    id="regression-function",
                                    className="function",
                                ),
                                html.Div("with x1 = coal, x2 = oil, and x3 = gas"),
                            ],
                            className="text",
                        ),
                        dcc.Graph(
                            figure=fig_animation,
                            id="fig-animation",
                            className="predict-animation",
                        ),
                    ],
                    className="inner-container border",
                ),
                html.Div(
                    [
                        html.Div(
                            "How many years will it take?",
                            className="subtitle",
                        ),
                        html.Div(
                            "Now that we know the attributes' behavior compared to coal, oil, and natural gas, we project the change over years in all twelve attributes.",
                            className="p",
                        ),
                        html.Div(
                            dcc.Slider(
                                0,
                                70,
                                1,
                                value=0,
                                id="predict-slider",
                                className="custom-slider",
                            ),
                            className="slider-container",
                        ),
                        html.Div(
                            divs_timeseries, className="time-series", id="time-series"
                        ),
                    ],
                    className="inner-container series border",
                ),
                html.Div(
                    [
                        html.Div(
                            "Total Greenhouse Gas Emissions in China 2088",
                            className="subtitle",
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    figure=fig4, className="overall-prediction-plot"
                                ),
                                dcc.Graph(figure=fig5, className="donut-plot"),
                            ],
                            className="overall",
                        ),
                    ],
                    className="inner-container border",
                ),
            ],
            className="outer-container",
        ),
    ]
)


@callback(
    Output("fig-animation", "figure"),
    Output("regression-function", "children"),
    Input("fig-animation-dropdown", "value"),
)
def update_output(value):
    desired_attribute = value
    value_att = df[desired_attribute][:-1]
    animate_y_desired, animate_x_desired = predicting_values(df, desired_attribute, 100)
    value_att = pd.concat([value_att, pd.Series(animate_y_desired)])

    animate_data = pd.DataFrame({
        'Year': year_value,
        'coal': value_coal,
        'oil': value_oil,
        'gas': value_gas,
        desired_attribute: value_att
    })

    data_melted = animate_data.melt(id_vars='Year', var_name='Attribute', value_name='Value')
    y_range = [0,12000]

    if value == "Energy":
        function = "$$y=1.054082x1+1.060988x2+0.930552x3+75.78041$$"
    elif value == "Fugi":
        function = "$$y=55.21474x1+55.72093x2-54.6685x3+8331.273$$"
        y_range = [0,570000]
    elif value == "FC":
        function = "$$y=0.998867x1+1.005267x2+0.98522x3+67.44913$$"
    elif value == "CO2 MARBUNK":
        function = "$$y=0.001894x1+0.009218x2+0.016915x3-0.88161$$"
    elif value == "CO2 AVBUNK":
        function = "$$y=0.001271x1+0.012471x2-0.00119x3-4.47361$$"
    elif value == "CO2-TES":
        function = "$$y=0.001716x1+0.02748x2-0.05785x3+48.04698$$"
    elif value == "CO2-GDP":
        function = "$$y=0.000085x1-0.00431x2+0.00547x3+3.442137$$"
    elif value == "CO2-GDP PPP":
        function = "$$y=0.000053x1-0.00268x2+0.0034x3+2.139604788$$"
    elif value == "CO2-POP":
        function = "$$y=0.000767x1+0.000151x2+0.0006x3+0.420289$$"


    fig_animation = px.bar(
        data_melted,
        x="Attribute",
        y="Value",
        title="Oil, Gas, Coal, and CO2/GHG Emission Over Time",
        animation_frame="Year",
        range_y=y_range,
    )
    return fig_animation, function


@callback(
    Output("line-plot", "figure"),
    Output("compare-plot", "figure"),
    Input("year-slider", "value"),
    Input("memory-field", "value"),
    prevent_initial_call=True,
)
def update_graph(selected_years, selected_attributes):
    start_year, end_year = selected_years
    filtered_df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]

    filtered_df_lowest = (
        df[selected_attributes]
        .loc[df["Year"] == start_year]
        .melt(var_name="Attribute", value_name="Value")
    )
    filtered_df_highest = (
        df[selected_attributes]
        .loc[df["Year"] == end_year]
        .melt(var_name="Attribute", value_name="Value")
    )

    updated_fig = go.Figure()
    updated_fig2 = go.Figure()

    for col in selected_attributes:
        updated_fig.add_trace(
            go.Scatter(
                x=list(filtered_df["Year"]),
                y=list(filtered_df[col]),
                name=col,
                line=dict(color=colors[attributes.index(col) % len(colors)]),
                marker=dict(color=colors[attributes.index(col) % len(colors)]),
            )
        )

    updated_fig.update_layout(plot_bgcolor="white")
    updated_fig.update_xaxes(
        mirror=True,
        ticks="outside",
        showline=True,
        linecolor="black",
        gridcolor="lightgrey",
    )
    updated_fig.update_yaxes(
        mirror=True,
        ticks="outside",
        showline=True,
        linecolor="black",
        gridcolor="lightgrey",
    )
    updated_fig.update_layout(hovermode="x unified")
    updated_fig.update_layout(title=dict(text="Actual Greenhouse Emissions in China"))

    updated_fig2.add_trace(
        go.Bar(
            x=filtered_df_lowest["Attribute"],
            y=filtered_df_lowest["Value"],
            name=start_year,
        )
    )

    updated_fig2.add_trace(
        go.Bar(
            x=filtered_df_highest["Attribute"],
            y=filtered_df_highest["Value"],
            name=end_year,
        )
    )
    updated_fig2.update_layout(plot_bgcolor="white", width=500)
    updated_fig2.update_xaxes(
        mirror=True,
        ticks="outside",
        showline=True,
        linecolor="black",
        gridcolor="white",
    )
    updated_fig2.update_yaxes(
        mirror=True,
        ticks="outside",
        showline=True,
        linecolor="black",
        gridcolor="lightgrey",
    )
    updated_fig2.update_layout(title=dict(text="Emissions Growth Over The Years"))

    return updated_fig, updated_fig2


@app.callback(
    Output("time-series", "children"),
    Input("predict-slider", "value"),
)
def update_charts(selected_year):
    chart_divs = []

    for attribute in attributes:
        chart_divs.append(
            html.Div(create_combined_timeseries_chart(df, attribute, selected_year))
        )

    return chart_divs


if __name__ == "__main__":
    app.run(debug=True)
