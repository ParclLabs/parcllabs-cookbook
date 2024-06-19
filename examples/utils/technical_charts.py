import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .utils import create_labs_logo_dict


# config logo
labs_logo_dict = create_labs_logo_dict(
    src='labs',
    y=1.07,
    x=1,
    xanchor='right',
    yanchor='top',
    sizex=0.15,
    sizey=0.15,
)

def calculate_stats(
    mf: pd.DataFrame
):
    # Calculate 52-week high and low
    last_date = mf['date'].max()
    one_year_ago = last_date - pd.DateOffset(weeks=52)

    # Filter data for the past 52 weeks
    last_52_weeks_data = mf[mf['date'] >= one_year_ago]

    # 52-week high
    high_52w = last_52_weeks_data['price_feed'].max()

    # 52-week low
    low_52w = last_52_weeks_data['price_feed'].min()

    # Last value
    last_value = mf['price_feed'].iloc[-1]

    # Year-over-Year (YoY) Change
    one_year_ago_value = mf.loc[mf['date'] == one_year_ago, 'price_feed'].values
    if len(one_year_ago_value) == 0:
        # If there's no exact match for the date, get the closest date before
        one_year_ago_value = mf[mf['date'] < one_year_ago]['price_feed'].iloc[-1]
    else:
        one_year_ago_value = one_year_ago_value[0]

    yoy_change_pct = (last_value - one_year_ago_value) / one_year_ago_value
    yoy_change_delta = last_value - one_year_ago_value
    yoy_sign = '' if yoy_change_delta >= 0 else '-'
    return high_52w, low_52w, last_value, yoy_change_delta, yoy_change_pct, yoy_sign


# technical chart definition
def technical_pricefeed_charts(
    data_main: pd.DataFrame,
    data_secondary: pd.DataFrame,
    save_path: str = None,
    value_name_main: str = None,
    value_name_secondary: str = None,
    ticker_msg: str = None,
    volume_msg: str = None,
    pricefeed_msg: str = None,
    last_pf_date: str = None,
    msg: str = None
):
    HEIGHT_MAIN = 500
    HEIGHT_SECONDARY = 200
    TOTAL_HEIGHT = HEIGHT_MAIN + HEIGHT_SECONDARY
    WIDTH = 1200

    data_main['date'] = pd.to_datetime(data_main['date'])
    data_secondary['date'] = pd.to_datetime(data_secondary['date'])
    # data_third['date'] = pd.to_datetime(data_third['date'])

    # Get the date range for the x-axis
    date_range = [min(data_main['date'].min(), data_secondary['date'].min()), max(data_main['date'].max(), data_secondary['date'].max())]

    # Create subplots: 2 rows, 1 column
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=False,
        row_heights=[0.8, 0.2],
        vertical_spacing=0.05  # Increased vertical spacing
    )

    # Add traces for positive and negative segments based on daily_return
    for i in range(1, len(data_main)):
        color = 'green' if data_main['daily_return'].iloc[i] >= 0 else 'red'
        fig.add_trace(
            go.Scatter(
                x=[data_main['date'].iloc[i-1], data_main['date'].iloc[i]],
                y=[data_main[value_name_main].iloc[i-1], data_main[value_name_main].iloc[i]],
                mode='lines',
                line=dict(width=3, color=color),
                showlegend=False
            ),
            row=1, col=1
        )

    # Plot the secondary data as a bar chart
    fig.add_trace(
        go.Bar(
            x=data_secondary['date'],
            y=data_secondary[value_name_secondary],
            name='Sales Volume',
            marker=dict(color=data_secondary['volColor'])  # Use volColor for the bar chart colors
        ),
        row=2, col=1
    )
    # Add the 6-month moving average line
    data_secondary['sales_ma'] = data_secondary[value_name_secondary].rolling(window=6).mean()
    ma_last = data_secondary['sales_ma'].iloc[-1]
    fig.add_trace(
        go.Scatter(
            x=data_secondary['date'],
            y=data_secondary['sales_ma'],
            mode='lines',
            name='6-Month Moving Average',
            line=dict(width=2, color='#FFA500'),  # Orange for the moving average line
            showlegend=False
        ),
        row=2, col=1
    )

    # Update layout
    fig.update_layout(
        height=TOTAL_HEIGHT,
        width=WIDTH,
        plot_bgcolor='#000000',  # Dark background for better contrast
        paper_bgcolor='#000000',  # Dark background for the paper
        font=dict(color='#FFFFFF'),
        xaxis=dict(
            title_text='',
            showgrid=True,  # Disable vertical grid lines
            gridcolor='rgba(255, 255, 255, 0.2)',  # Vertical grid line color with opacity
            tickangle=0,
            tickfont=dict(size=14),
            linecolor='rgba(255, 255, 255, 0.7)',  # Axis line color with opacity
            linewidth=1,  # Axis line width
            tickformat='`%y',
            range=date_range,
        ),
        xaxis2=dict(
            title_text='',
            showgrid=True,  # Disable vertical grid lines
            gridcolor='rgba(255, 255, 255, 0.2)',  # Horizontal grid line color with opacity
            tickangle=0,
            tickfont=dict(size=14),
            linecolor='rgba(255, 255, 255, 0.7)',  # Axis line color with opacity
            linewidth=1,  # Axis line width
            tickformat='`%y',
            range=date_range,
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=0.5,  # Horizontal grid line width
            gridcolor='rgba(255, 255, 255, 0.2)',  # Horizontal grid line color with opacity
            tickfont=dict(size=14),
            ticksuffix='',  # Remove dollar sign suffix
            zeroline=False,
            linecolor='rgba(255, 255, 255, 0.7)',  # Axis line color with opacity
            linewidth=1,  # Axis line width
            side='right',
            ticks='outside',
            rangemode='normal',
            range=[data_main[value_name_main].min(), data_main[value_name_main].max() + 10]
        ),
        yaxis2=dict(
            showgrid=True,
            gridwidth=0.5,  # Horizontal grid line width
            gridcolor='rgba(255, 255, 255, 0.2)',  # Horizontal grid line color with opacity
            tickfont=dict(size=14),
            ticksuffix='',  # Remove dollar sign suffix
            zeroline=False,
            linecolor='rgba(255, 255, 255, 0.7)',  # Axis line color with opacity
            linewidth=1,  # Axis line width
            side='right',
            ticks='outside',
            rangemode='normal',
            range=[data_secondary[value_name_secondary].min(), data_secondary[value_name_secondary].max() + 10]
        ),
        hovermode='x unified',  # Unified hover mode for better interactivity
        hoverlabel=dict(
            bgcolor='#1F1F1F',
            font_size=14,
            font_family="Rockwell"
        ),
        showlegend=False,  # Show the legend to include the moving average line
    )

    # Add stats annotation
    fig.add_annotation(
        dict(
            text=msg,
            x=1,
            y=1.04,
            xref='paper',
            yref='paper',
            xanchor='right',
            yanchor='top',
            showarrow=False,
            font=dict(size=14, color='#FFFFFF')
        )
    )

    # Add placeholder text in the top left of each chart
    fig.add_annotation(
        dict(
            text=pricefeed_msg,
            x=0.003,
            y=0.99,
            xref='paper',
            yref='paper',
            xanchor='left',
            showarrow=False,
            font=dict(size=14, color='#FFFFFF')
        )
    )

    fig.add_annotation(
        dict(
            text=volume_msg,
            x=0.003,
            y=0.15,
            xref='paper',
            yref='paper',
            xanchor='left',
            showarrow=False,
            font=dict(size=14, color='#FFFFFF')
        )
    )

    fig.add_annotation(
        dict(
            text=f'--- MA(6) {ma_last:,.2f}',
            x=0.003,
            y=0.12,
            xref='paper',
            yref='paper',
            xanchor='left',
            showarrow=False,
            font=dict(size=14, color='#FFFFFF')
        )
    )

    fig.add_annotation(
        dict(
            text=last_pf_date,
            x=0,
            y=1.04,
            xref='paper',
            yref='paper',
            xanchor='left',
            yanchor='top',
            showarrow=False,
            font=dict(size=14, color='#FFFFFF')
        )
    )

    # Add ticker message
    fig.add_annotation(
        dict(
            text=ticker_msg,
            x=0,
            y=1.07,
            xref='paper',
            yref='paper',
            xanchor='left',
            yanchor='top',
            showarrow=False,
            font=dict(size=14, color='#FFFFFF')
        )
    )

    # Add borders and hover effect for both charts
    fig.update_xaxes(
        showline=True,
        linewidth=2,
        linecolor='#FFFFFF',
        mirror=True
    )
    fig.update_yaxes(
        showline=True,
        linewidth=2,
        linecolor='#FFFFFF',
        mirror=True,
        ticks="outside"
    )

    fig.update_layout(
    margin=dict(
        l=10,  # Left margin
        r=10,  # Right margin
        b=10,  # Bottom margin
        t=50   # Top margin
    )
)

    # Add Parcl Labs logo
    fig.add_layout_image(
        labs_logo_dict
    )

    if save_path:
        fig.write_image(save_path, width=WIDTH, height=TOTAL_HEIGHT)
    
    # Show the plot
    fig.show()
