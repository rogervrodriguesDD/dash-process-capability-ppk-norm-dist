import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from app_config import config
from data.process_data import ProcessData

def get_bar_plot_hovertemplate(*, time_unit: str, time_unit_format: str, process_data_obj: ProcessData,
                                ppk_rep_df: pd.DataFrame, ppk_goal: float, prob_dist_name: str, circ: str) -> list:
    """
    Create the hovertemplate list for the Bar plot.
    Obs.: All arguments must be passed as kwargs.

    Args:
        time_unit (str): Time unit name used as reference of the plot.
        time_unit_format (str): Time unit format to be printed.
        process_data_obj (ProcessData): Process Data object related to the plotted report.
        ppk_rep_df (pd.DataFrame): Dataframe with calculated Ppk index.
        ppk_goal (float): Ppk goal related to the plotted report.
        prob_dist_name (str): Name of the probability distribution considered in calculation of Ppk index.
        circ (str): Circuit name related to the plotted report.

    Returns:
        hovertemplate (list): List of strings with the points informations.
    """

    hovertemplate = [
        '''<b>{}:</b> {}<br><br>
        <b>Nº samples:</b> {:.0f}<br>
        <b>PPK:</b> {:.3f}<br>
        <b>Goal PPK:</b> {:.3f}<br>
        <b>LSL:</b> {}<br>
        <b>USL:</b> {}<br>
        <b>Prob. distribution</b>: {}'''.format(
                                            time_unit,
                                            ppk_rep_df.index[i].strftime(time_unit_format),
                                           ppk_rep_df.iloc[i][(circ, 'count')],
                                           ppk_rep_df.iloc[i][(circ, 'PPK')],
                                           ppk_goal,
                                           process_data_obj.specifications_limits[circ]['LSL'],
                                           process_data_obj.specifications_limits[circ]['USL'],
                                           prob_dist_name
                                           ) for i in range(len(ppk_rep_df))]

    return hovertemplate

def get_scatter_plot_hovertemplate(*, process_data_obj: ProcessData, start_date: str, end_date: str, circ: str) -> list:
    """
    Create the hovertemplate list for the Scatter plot.
    Obs.: All arguments must be passed as kwargs.

    Args:
        process_data_obj (ProcessData): Process Data object related to the plotted report.
        start_date (str): Start date considered when filtering the data before plot.
        end_date (str): End date considered when filtering the data before plot.
        circ (str): Circuit name related to the plotted report.

    Returns:
        hovertemplate (list): List of strings with the points informations.
    """

    data_index = process_data_obj.data.loc[start_date:end_date, circ].index
    data_values = process_data_obj.data.loc[start_date:end_date, circ].values

    hovertemplate = [
        '''<b>Date:</b> {}<br><br>
        <b>{}:</b> {:.3f}<br>
        <b>LSL:</b> {}<br>
        <b>USL:</b> {}<br>'''.format(
                                            data_index[i].strftime('%d.%m.%y %H:%M'),
                                            circ,
                                            data_values[i],
                                           process_data_obj.specifications_limits[circ]['LSL'],
                                           process_data_obj.specifications_limits[circ]['USL']
                                           ) for i in range(len(data_index))]

    return hovertemplate

def get_bar_plot_colors(*, ppk_rep_df, circ, ppk_goal) -> list:
    """
    Create list with individual bar colors for the Bar plot.
    The colors considered are 'plt_markers_color' and 'plt_markers_outliers_color'
    listed in the conf.yml file (conf/base folder).
    Obs.: All arguments must be passed as kwargs.

    Args:
        ppk_rep_df (pd.DataFrame): Dataframe with calculated Ppk index.
        circ (str): Circuit name related to the plotted report.
        ppk_goal (float): Ppk goal value related to the plotted report.

    Returns:
        colors_plot (list): List with individual bar colors for the plot.
    """

    colors_plot = []
    for ppk_val in ppk_rep_df[(circ, 'PPK')].values:
        if ppk_val >= ppk_goal:
            colors_plot.append(config.layout_config.plt_markers_color)
        else:
            colors_plot.append(config.layout_config.plt_markers_outliers_color)

    return colors_plot

def get_scatter_plot_colors(*, process_data_obj: ProcessData, start_date: str, end_date: str, circ: str) -> list:
    """
    Create list with individual markers colors for the Scatter plot.
    The colors considered are 'plt_markers_color' and 'plt_markers_outliers_color'
    listed in the conf.yml file (conf/base folder).
    Obs.: All arguments must be passed as kwargs.

    Args:
        process_data_obj (ProcessData): Process Data object related to the plotted report.
        start_date (str): Start date considered when filtering the data before plot.
        end_date (str): End date considered when filtering the data before plot.
        circ (str): Circuit name related to the plotted report.

    Returns:
        colors_plot (list): List with individual bar colors for the plot.
    """

    colors_plot = []
    for value in process_data_obj.data.loc[start_date:end_date, circ].values:
        if (value >= process_data_obj.specifications_limits[circ]['LSL'] ) & (value <= process_data_obj.specifications_limits[circ]['USL']):
            colors_plot.append(config.layout_config.plt_markers_color)
        else:
            colors_plot.append(config.layout_config.plt_markers_outliers_color)
    return colors_plot

def calculate_normal_distribution(samples: np.array):
    """
    Create a pair of arrays (x_dist_plot, y_dist_plot) for the normal probability curve
    fitted on the given samples.

    Args:
        samples (np.array): Sample values

    Returns:
        x_dist_plot (np.array): X coordinates of the fitted curve.
        y_dist_plot (np.array): Y coodinates of the fitted curve.
    """

    mu = np.mean(samples)
    sigma = np.std(samples)

    x_dist_plot = np.linspace(0.9 * np.min(samples), 1.1 * np.max(samples), 100)
    y_dist_plot = 1/sigma/np.sqrt(2*np.pi)*np.exp(-((x_dist_plot-mu)/(2*sigma))**2)

    return x_dist_plot, y_dist_plot

def create_figure_report(process_data_obj: ProcessData, ppk_rep_monthly: pd.DataFrame,
                    ppk_rep_daily: pd.DataFrame, process_data_selected_month: int) -> go.Figure:
    """
    Create figure of the full report.

    Args:
        process_data_obj (ProcessData): Process Data object related to the plotted report.
        ppk_rep_monthly (pd.DataFrame): Dataframe with calculated Ppk index using a monthly window.
        ppk_rep_daily (pd.DataFrame): Dataframe with calculated Ppk index using a daily window.
        process_data_selected_month (int): Selected month related to the daily report.

    Returns:
        fig_report (go.Figure): Figure of the Ppk index full report.
    """

    nrows = len(process_data_obj.circuit_names)

    fig_report = make_subplots(
        rows=nrows,
        cols=3,
        subplot_titles=['Monthly', 'Daily', 'Histogram (Selected month)'] * nrows,
        row_titles = process_data_obj.circuit_names
        )

    for i, circ in enumerate(process_data_obj.circuit_names):

        ppk_goal = process_data_obj.ppk_goals[circ]

        colors_month = get_bar_plot_colors(ppk_rep_df=ppk_rep_monthly, circ=circ, ppk_goal=ppk_goal)
        hovertemplate_monthly = get_bar_plot_hovertemplate(time_unit='Month',
                                                        time_unit_format='%b',
                                                        process_data_obj=process_data_obj,
                                                        ppk_rep_df=ppk_rep_monthly,
                                                        ppk_goal=ppk_goal,
                                                        prob_dist_name='Normal',
                                                        circ=circ)

        fig_report.add_trace(go.Bar(
            x = ppk_rep_monthly.index,
            y = ppk_rep_monthly[(circ, 'PPK')],
            marker_color = colors_month,
            hovertemplate=hovertemplate_monthly,
            text=['{:.3f}'.format(ppk) for ppk in ppk_rep_monthly[(circ, 'PPK')]],
            ),
            row=i+1, col=1
        )

        colors_daily= get_bar_plot_colors(ppk_rep_df=ppk_rep_daily, circ=circ, ppk_goal=ppk_goal)
        hovertemplate_daily = get_bar_plot_hovertemplate(time_unit='Date',
                                                        time_unit_format='%d.%m',
                                                        process_data_obj=process_data_obj,
                                                        ppk_rep_df=ppk_rep_daily,
                                                        ppk_goal=ppk_goal,
                                                        prob_dist_name='Normal',
                                                        circ=circ)

        fig_report.add_trace(go.Bar(
            x = ppk_rep_daily.index,
            y = ppk_rep_daily[(circ, 'PPK')],
            marker_color = colors_daily,
            hovertemplate = hovertemplate_daily,
            text=['{:.3f}'.format(ppk) for ppk in ppk_rep_daily[(circ, 'PPK')]],
            ),
            row=i+1, col=2
        )

        # Adding the goal lines in the Bar plots
        for c, (delta_x, ppk_rep_df) in enumerate(zip([15, 1], [ppk_rep_monthly, ppk_rep_daily])):

            x0 = min(ppk_rep_df.index) - datetime.timedelta(days=delta_x)
            x1 = max(ppk_rep_df.index) + datetime.timedelta(days=delta_x)

            fig_report.add_shape(
                go.layout.Shape(
                    type='line',
                    xref='paper',
                    yref='paper',
                    y0=ppk_goal,
                    y1=ppk_goal,
                    x0=x0,
                    x1=x1,
                    line = dict(
                            color=config.layout_config.plt_lim_line_color,
                            width=3
                            )
                ),
                row=i+1, col=c+1
            )

        # Histogram plot
        fig_report.add_trace(go.Histogram(
            x=process_data_selected_month[circ].values,
            histnorm='probability density',
            hoverinfo='skip',
            opacity=0.8,
            marker = dict(color = config.layout_config.plt_markers_color)
        ), row = i+1, col = 3)

        # Ploting the fitted normal distribution curve
        x_dist_plot, y_dist_plot = calculate_normal_distribution(process_data_selected_month[circ].dropna().values)

        fig_report.add_trace(go.Scatter(
            x = x_dist_plot,
            y = y_dist_plot,
            mode = 'lines',
            marker = dict(color = config.layout_config.plt_line_color),
            hoverinfo='skip',
        ), row = i+1, col = 3)

        # Plotting the specification limits
        for lim in process_data_obj.specifications_limits[circ].values():
            if lim is not None:
                fig_report.add_shape(
                    dict(
                        x0=lim,
                        x1=lim,
                        y0=0.0,
                        y1=1.5 * np.max(y_dist_plot),
                        line=dict(
                            color=config.layout_config.plt_lim_line_color,
                            dash=config.layout_config.plt_lim_line_dash,
                            width=3
                        )
                    ),
                    row=i+1, col=3
                )

    for i in range(nrows):
        for c in [1, 2]:
            fig_report.update_yaxes(title_text='ppk', row=i+1, col=c)
            fig_report.update_xaxes(title_text='date', row=i+1, col=c)

        # Removing yaxes for the histogram
        fig_report.update_xaxes(title_text='controlled variable', visible=True, row=i+1, col=3)
        fig_report.update_yaxes(title_text='prob. density', visible=True, row=i+1, col=3)

    fig_report.update_layout(
        template = config.layout_config.plt_template_name,
        hovermode = 'x',
        width = config.layout_config.plt_full_report_width,
        height = config.layout_config.plt_full_report_height * nrows,
        showlegend = False
    )

    return fig_report

def create_figure_control_chart(process_data_obj: ProcessData, start_date: str, end_date: str) -> go.Figure:
    """
    Create figure of the Control Chart.

    Args:
        process_data_obj (ProcessData): Process Data object related to the plotted report.
        start_date (str): Start date considered when filtering the data before plot.
        end_date (str): End date considered when filtering the data before plot.

    Returns:
        fig_control_chart (go.Figure): Figure of the Control Chart plot.
    """


    nrows = len(process_data_obj.circuit_names)

    fig_control_chart = make_subplots(
        rows=nrows,
        cols=2,
        column_widths = [0.85, 0.15],
        subplot_titles=['Control Chart', 'Violin Plot'] * nrows,
        row_titles = process_data_obj.circuit_names,
        shared_yaxes=True,
        vertical_spacing=0.15,
        horizontal_spacing=0.03
        )

    for i, circ in enumerate(process_data_obj.circuit_names):

        hovertemplate_control_chart = get_scatter_plot_hovertemplate(process_data_obj=process_data_obj,
                                                                    start_date=start_date,
                                                                    end_date=end_date,
                                                                    circ=circ)

        colors_control_chart = get_scatter_plot_colors(process_data_obj=process_data_obj,
                                                    start_date=start_date,
                                                    end_date=end_date,
                                                    circ=circ)

        fig_control_chart.add_trace(
            go.Scatter(
                x = process_data_obj.data.loc[start_date:end_date, circ].index,
                y = process_data_obj.data.loc[start_date:end_date, circ].values,
                mode = 'markers',
                marker = dict(color = colors_control_chart),
                line=dict(color = config.layout_config.plt_markers_color),
                name = circ,
                hovertemplate = hovertemplate_control_chart
                ),
                row=i+1, col=1
        )

        # Adding specification limits lines
        for lim_text, lim in process_data_obj.specifications_limits[circ].items():
            if lim is not None:
                fig_control_chart.add_shape(
                    dict(
                        x0=start_date,
                        x1=end_date,
                        y0=lim,
                        y1=lim,
                        line=dict(
                            color=config.layout_config.plt_lim_line_color,
                            width=2,
                            dash=config.layout_config.plt_lim_line_dash
                        )
                    ),
                    row=i+1, col=1
                )

                # Adding text with names of the limits
                fig_control_chart.add_annotation(
                    go.layout.Annotation(
                        text=f"<b>{lim_text}</b>",
                        xref='paper',
                        yref='paper',
                        x=(pd.to_datetime(start_date, format='%Y-%m-%dT%H:%M:%S') - datetime.timedelta(days=1)),
                        y=lim,
                        showarrow=False,
                        font = dict(color=config.layout_config.plt_lim_line_color)
                    ),
                    row=i+1, col=1
                )

        # Adding average line
        average=process_data_obj.data.loc[start_date:end_date, circ].mean()
        fig_control_chart.add_shape(
            dict(
                x0=start_date,
                x1=end_date,
                y0=average,
                y1=average,
                line=dict(
                    color=config.layout_config.plt_average_line,
                    width=3,
                    dash=config.layout_config.plt_average_line_dash
                )
            ),
            row=i+1, col=1
        )

        fig_control_chart.add_annotation(
            go.layout.Annotation(
                text="<b>Average</b>",
                xref='paper',
                yref='paper',
                x=(pd.to_datetime(start_date, format='%Y-%m-%dT%H:%M:%S') - datetime.timedelta(days=1)),
                y=average,
                showarrow=False,
                font = dict(color=config.layout_config.plt_average_line)
            ),
            row=i+1, col=1
        )


        fig_control_chart.add_trace(
            go.Violin(
                y = process_data_obj.data.loc[start_date:end_date, circ].values,
                name=circ,
                box_visible=False,
                points='all',
                meanline_visible=True,
                fillcolor=config.layout_config.plt_markers_color,
                marker=dict(color=config.layout_config.plt_markers_color),
                line_color='black',
                opacity=0.6,
                hoverinfo='skip'
            ),
            row = i+1, col=2
        )


    for i in range(nrows):
        fig_control_chart.update_yaxes(title_text='process variable', row=i+1, col=1)
        fig_control_chart.update_xaxes(title_text='date', row=i+1, col=1)
        fig_control_chart.update_xaxes(title_text='', row=i+1, col=2)

    fig_control_chart.update_layout(
                template = config.layout_config.plt_template_name,
                hovermode = 'x',
                width = config.layout_config.plt_control_chart_width,
                height = config.layout_config.plt_control_chart_height * nrows,
                showlegend = False
    )

    return fig_control_chart
