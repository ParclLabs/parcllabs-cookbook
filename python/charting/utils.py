import os
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go


labs_logo_lookup = {
    'blue': 'https://parcllabs-assets.s3.amazonaws.com/powered-by-parcllabs-api.png',
    'white': 'https://parcllabs-assets.s3.amazonaws.com/powered-by-parcllabs-api-logo-white+(1).svg'
}

# Set charting constants
labs_logo_dict = dict(
    source=labs_logo_lookup['white'],
    xref="paper",
    yref="paper",
    x=0.5,  # Centering the logo below the title
    y=1.04,  # Adjust this value to position the logo just below the title
    sizex=0.15, 
    sizey=0.15,
    xanchor="center",
    yanchor="bottom",
)


def build_line_chart(
        data: pd.DataFrame,
        title: str=None,
        x_axis_title: str=None,
        y_axis_title: str=None,
        save_path: str=None,
        value_name: str=None
    ):

    HEIGHT = 900
    WIDTH = 1600
    
    # Calculate median price_feed
    median_value = data[value_name].median()
    
    fig = go.Figure()

    # Split data into continuous segments based on median
    segments = []
    current_segment = []
    current_color = None

    for i in range(len(data)):
        if current_color is None:
            current_color = '#FFFFFF' if data.iloc[i][value_name] >= median_value else '#57A3FF'
            current_segment.append(data.iloc[i])
        elif (data.iloc[i][value_name] >= median_value and current_color == '#FFFFFF') or (data.iloc[i][value_name] < median_value and current_color == '#57A3FF'):
            current_segment.append(data.iloc[i])
        else:
            segments.append((current_segment, current_color))
            current_color = '#FFFFFF' if data.iloc[i][value_name] >= median_value else '#57A3FF'
            current_segment = [data.iloc[i]]
    
    if current_segment:
        segments.append((current_segment, current_color))

    for segment, color in segments:
        segment_df = pd.DataFrame(segment)
        fig.add_trace(go.Scatter(
            x=segment_df['date'],
            y=segment_df[value_name],
            mode='lines',
            line=dict(width=2, color=color),  # Reduced line width for thinner lines
            showlegend=False
        ))

    # Add horizontal line for median price feed value
    fig.add_shape(
        type="line",
        x0=data['date'].min(),
        y0=median_value,
        x1=data['date'].max(),
        y1=median_value,
        line=dict(
            color="#FFFFFF",
            width=1,
            dash="dot",  # Small dots for the median line
        ),
        opacity=1  # Set the opacity to 0.7
    )
    
    fig.add_layout_image(labs_logo_dict)
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=110, b=0),
        height=HEIGHT,
        width=WIDTH,
        title={
            'text': title,
            'y': 0.99,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=28, color='#FFFFFF'),
        },
        plot_bgcolor='#000000',  # Dark background for better contrast
        paper_bgcolor='#000000',  # Dark background for the paper
        font=dict(color='#FFFFFF'),
        xaxis=dict(
            title_text=x_axis_title,
            showgrid=False,  # Disable vertical grid lines
            tickangle=-45,
            tickfont=dict(size=14),
            linecolor='rgba(255, 255, 255, 0.7)',  # Axis line color with opacity
            linewidth=1  # Axis line width
        ),
        yaxis=dict(
            title_text=y_axis_title,
            showgrid=True,
            gridwidth=0.5,  # Horizontal grid line width
            gridcolor='rgba(255, 255, 255, 0.2)',  # Horizontal grid line color with opacity
            tickfont=dict(size=14),
            tickprefix='$',  # Add dollar sign to y-axis labels
            zeroline=False,
            linecolor='rgba(255, 255, 255, 0.7)',  # Axis line color with opacity
            linewidth=1  # Axis line width
        ),
        hovermode='x unified',  # Unified hover mode for better interactivity
        hoverlabel=dict(
            bgcolor='#1F1F1F',
            font_size=14,
            font_family="Rockwell"
        )
    )


    if save_path:
        fig.write_image(save_path, width=WIDTH, height=HEIGHT)
    
    # Show the plot
    fig.show()
