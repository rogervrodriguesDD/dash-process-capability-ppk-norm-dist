from dash import html, dcc, callback
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from app_config import DOCS_ROOT, config

from pipeline import data_A_c1, df_A_c1_month
from process_capability_index.utils import calculate_cap_index_ppk
from visualization.utils import create_figure_report, create_figure_control_chart

def banner_layout():
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
                            html.P('Select month:'),
                            dcc.Dropdown(id='month-selector',
                                    multi=False,
                                    clearable=False,
                                    options = [{'label': item.strftime('%b'), 'value': item.month} for item in df_A_c1_month.index],
                                    value = df_A_c1_month.index[-1].month
                                    )
                            ],
                            style = {'width': '20%'}
                        ),
                        html.Div(
                            children = [
                                html.Div([dcc.Graph(id = 'fig_index_report')], style = {'display': 'inline-block'})
                            ]
                        )
                    ])

    return tab_index_report_layout

def tab_control_chart_layout():
    tab_control_chart_layout = \
                dcc.Tab(
                    label = 'Control Chart',
                    value = 'Control Chart',
                    className = 'custom-tab',
                    selected_className = 'custom-tab--selected',
                    children = [
                        html.Div(
                            [
                            html.Div(html.H2('Control Chart ', style = {'textAlign': 'left'})),
                            html.P('Select the time range:'),
                            dcc.DatePickerRange(
                                   id='date-range-selector',
                                   min_date_allowed=data_A_c1.data.index.min(),
                                   max_date_allowed=data_A_c1.data.index.max(),
                                   start_date=data_A_c1.data.index.min(),
                                   end_date=data_A_c1.data.index.max(),
                                   clearable=False,
                                   display_format='DD.MM.YY'
                                    )
                            ],
                            style = {'width': '40%'}
                        ),
                        html.Div(
                            children = [
                                html.Div([dcc.Graph(id='fig_control_chart', style = {'display': 'inline-block'})])
                            ]
                        )
                    ])

    return tab_control_chart_layout

def tab_about_layout():

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
    Output('fig_index_report', 'figure'),
    [Input('month-selector', 'value')]
)
def create_figure_report_callback(selected_month):

    df_A_c1_filtered = data_A_c1.data.loc[data_A_c1.data.index.month == selected_month]

    ppk_rep_monthly = calculate_cap_index_ppk(data_A_c1, freq='BMS')
    ppk_rep_daily = calculate_cap_index_ppk(data_A_c1, freq='D')

    ppk_rep_daily_sel_month = ppk_rep_daily.loc[ppk_rep_daily.index.month == selected_month]
    process_data_sel_month = data_A_c1.data.loc[data_A_c1.data.index.month == selected_month]

    fig_index_report = create_figure_report(data_A_c1, ppk_rep_monthly, ppk_rep_daily_sel_month, process_data_sel_month)

    return fig_index_report

@callback(
    Output('fig_control_chart', 'figure'),
    [Input('date-range-selector', 'start_date'),
    Input('date-range-selector', 'end_date')]
)
def create_figure_control_chart_callback(start_date, end_date):

    fig_control_chart = create_figure_control_chart(data_A_c1, start_date, end_date)

    return fig_control_chart
