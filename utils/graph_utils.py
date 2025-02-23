import plotly.express as px

def apply_common_styles(fig, title=None, legend_title=None, x_rangeslider=True, hover_template=None):
    """
    Apply consistent styling and interactivity to a Plotly figure.
    
    Parameters:
        fig: Plotly figure object.
        title (str): Optional title for the figure.
        legend_title (str): Optional legend title.
        x_rangeslider (bool): Whether to enable the x-axis range slider.
        hover_template (str): Custom hover template to apply to all traces.
        
    Returns:
        fig: The updated Plotly figure.
    """
    if title:
        fig.update_layout(title=title)
    
    if legend_title:
        fig.update_layout(legend_title_text=legend_title)
    
    # Add range slider to the x-axis if applicable
    if x_rangeslider:
        fig.update_xaxes(rangeslider_visible=True)
    
    # Apply a common hover template if provided
    if hover_template:
        fig.update_traces(hovertemplate=hover_template)
    
    # Use a professional, clean template and adjust margins
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig
