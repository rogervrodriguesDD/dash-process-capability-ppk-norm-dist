import datetime
from dash import html, dcc, callback, callback_context
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from app_config import DOCS_ROOT, config

from pipeline import data_ind_park
from process_capability_index.utils import calculate_cap_index_ppk
from visualization.utils import create_figure_report, create_figure_control_chart

def banner_layout():
    """
    Creates the layout division of the upper banner.
    """
    banner_layout_div =  html.Div(
            id = 'banner',
            children = [
                html.Div(
                    html.H1("Capability Control of the Process",
                        id = 'title',
                        style = {'textAlign': 'center',
                            'color': config.layout_config.banner_txt_color,
                            'backgroundColor': config.layout_config.banner_bkg_color}
                            ),
                    style = {'display': 'inline-block', 'width': config.layout_config.banner_width}

                )
            ]
        )
    return banner_layout_div

def tab_index_report_layout():
    """
    Create the Tab component with the Ppk index complete report.
    """
    tab_index_report_layout = \
                dcc.Tab(
                    label = 'Index Report',
                    value = 'Index Report',
                    className = 'custom-tab',
                    selected_className = 'custom-tab--selected',
                    children = [
                        html.Div(html.H2('Index Report: PPK ', style = {'textAlign': 'left'})),

                        html.Div(
                            [

                            html.Div(
                                [
                                html.P('Select plant name:'),
                                dcc.Dropdown(id='plant-selector',
                                        multi=False,
                                        clearable=False,
                                        options = [{'label': p_name, 'value': p_name} for p_name in data_ind_park.list_plant_names],
                                        value = data_ind_park.list_plant_names[0]
                                        ),
                                ],
                                style = {'width': '20%'}
                            ),

                            html.Div(
                                [
                                html.P('Select month:'),
                                dcc.Dropdown(id='month-selector',
                                        multi=False,
                                        clearable=False)
                                ],
                                style = {'width': '20%'}
                            ),

                            ],
                            style = {'display' : 'flex', 'width' : '100%' }
                        ),

                        html.Div(
                            children = [
                                html.Div([dcc.Graph(id = 'fig_index_report')], style = {'display': 'inline-block'})
                            ]
                        )
                    ])

    return tab_index_report_layout

def tab_control_chart_layout():
    """
    Create the Tab component with the Control Chart report.
    """
    tab_control_chart_layout = \
                dcc.Tab(
                    label = 'Control Chart',
                    value = 'Control Chart',
                    className = 'custom-tab',
                    selected_className = 'custom-tab--selected',
                    children = [
                        html.Div(html.H2('Control Chart ', style = {'textAlign': 'left'})),
                        html.Div(
                            [

                            html.Div(
                                [
                                html.P('Select plant name:'),
                                dcc.Dropdown(id='plant-selector-cc',
                                        multi=False,
                                        clearable=False,
                                        options = [{'label': p_name, 'value': p_name} for p_name in data_ind_park.list_plant_names],
                                        value = data_ind_park.list_plant_names[0]
                                        ),
                                ], style = {'width': '20%'}
                            ),

                            html.Div(
                                [
                                html.P('Select the time range:'),
                                dcc.DatePickerRange(
                                       id='date-range-selector',
                                       clearable=False,
                                       display_format='DD.MM.YY'
                                )
                                ], style = {'width' : '40%'}
                            )

                            ], style = {'width': '100%', 'display' : 'flex'}
                        ),

                        html.Div(
                            children = [
                                html.Div([dcc.Graph(id='fig_control_chart', style = {'display': 'inline-block'})])
                            ]
                        )
                    ])

    return tab_control_chart_layout

def tab_about_layout():
    """
    Create the Tab component with the documentation file 'Basics on Capability Control'
    """

    basics_on_cap_control_path = DOCS_ROOT / config.documentation_tab_config.basics_on_cap_control_file
    with open(basics_on_cap_control_path, encoding='utf-8') as f:
        basics_on_cap_control = f.read()

    tab_about_layout = \
                dcc.Tab(
                    label = 'Basics on Ppk index',
                    value = 'Basics on Ppk index',
                    className = 'custom-tab',
                    selected_className = 'custom-tab--selected',
                    children = [
                            html.Div(
                                [dcc.Markdown(basics_on_cap_control, mathjax=True)],
                                style = {'width': config.documentation_tab_config.doc_tab_width}
                                )

                            ],
                        )

    return tab_about_layout


def set_tabs_layout():
    """
    Create the layout division component that contains all Tab components of the application.
    """
    set_tabs_layout = \
        html.Div([
            dcc.Tabs(
            id = 'tabs',
            parent_className = 'custom-tabs',
            className = 'custom-tabs-container',
            value = 'Index Report',
            children = [
                tab_index_report_layout(),
                tab_control_chart_layout(),
                tab_about_layout()
                ]
            )
        ])
    return set_tabs_layout

app_layout = html.Div(children=
    [
        banner_layout(),
        set_tabs_layout(),
    ]
)

@callback(
    [Output('month-selector', 'options'),
    Output('month-selector', 'value')],
    Input('plant-selector', 'value')
)
def get_month_selector_options_callback(selected_plant_name):
    """
    Callback to return the options for the 'month-selector' given the selected plant name.
    """

    data_selected_plant_months = data_ind_park[selected_plant_name].data.resample('BMS').count().index
    month_selector_options = [{'label': item.strftime('%B'), 'value': item.month} for item in data_selected_plant_months]
    month_selector_value = data_selected_plant_months[-1].month

    return month_selector_options, month_selector_value

@callback(
    [Output('date-range-selector', 'min_date_allowed'),
    Output('date-range-selector', 'max_date_allowed'),
    Output('date-range-selector', 'start_date'),
    Output('date-range-selector', 'end_date')],
    Input('plant-selector-cc', 'value')
)
def get_date_range_selector_options_callback(selected_plant_name):
    """
    Callback to return the options for the 'date-range-selector' given the selected plant name.
    """

    data_selected_plant = data_ind_park[selected_plant_name]
    min_date_allowed=data_selected_plant.data.index.min()
    max_date_allowed=data_selected_plant.data.index.max()
    start_date=data_selected_plant.data.index.max() - datetime.timedelta(days=30)
    end_date=data_selected_plant.data.index.max()

    return min_date_allowed, max_date_allowed, start_date, end_date


@callback(
    [Output('plant-selector', 'value'),
    Output('plant-selector-cc', 'value')],
    [Input('plant-selector', 'value'),
    Input('plant-selector-cc', 'value')]
)
def sync_plant_selectors_dropdown_callback(selected_plant_rep, selected_plant_cc):
    """
    Callback to synchronize the Dropdown components 'plant-selector' (full report) and 'plant-selector-cc' (control chart)
    """
    ctx = callback_context
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'plant-selector':
        return selected_plant_rep, selected_plant_rep
    else:
        return selected_plant_cc, selected_plant_cc

@callback(
    Output('fig_index_report', 'figure'),
    [Input('plant-selector', 'value'),
    Input('month-selector', 'value')]
)
def create_figure_report_callback(selected_plant_name, selected_month):
    """
    Callback to create and return the figure of the Ppk index full report.
    """

    data_selected_plant = data_ind_park[selected_plant_name]

    ppk_rep_monthly = calculate_cap_index_ppk(data_selected_plant, freq='BMS')
    ppk_rep_daily = calculate_cap_index_ppk(data_selected_plant, freq='D')

    ppk_rep_daily_sel_month = ppk_rep_daily.loc[ppk_rep_daily.index.month == selected_month]
    process_data_sel_month = data_selected_plant.data.loc[data_selected_plant.data.index.month == selected_month]

    fig_index_report = create_figure_report(data_selected_plant, ppk_rep_monthly, ppk_rep_daily_sel_month, process_data_sel_month)

    return fig_index_report

@callback(
    Output('fig_control_chart', 'figure'),
    [Input('plant-selector-cc', 'value'),
    Input('date-range-selector', 'start_date'),
    Input('date-range-selector', 'end_date')]
)
def create_figure_control_chart_callback(selected_plant_name_cc, start_date, end_date):
    """
    Callback to create and return the figure of the Control Chart.
    """
    data_selected_plant_cc = data_ind_park[selected_plant_name_cc]
    fig_control_chart = create_figure_control_chart(data_selected_plant_cc, start_date, end_date)

    return fig_control_chart
