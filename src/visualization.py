import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import seaborn as sns
from IPython.display import HTML
import ipywidgets as widgets
from IPython.display import display, HTML

def create_risk_sliders(risk_categories, boundaries=[0, 100], step_size=5, bar_color='black'):
    """
    Creates sliders for each risk category, validates the sum to ensure it equals 100%, 
    and displays the sliders. Also returns a dictionary of sliders for direct value access.
    
    Parameters:
        risk_categories (list): List of risk category names.
        boundaries (list): Min and max values for the sliders.
        step_size (int): Step increment for the sliders.
        bar_color (str): Color for the slider bar.
        
    Returns:
        tuple: (widgets.VBox, dict) - A VBox containing all sliders and the validation output, 
                                      and a dictionary of slider widgets for direct access.
    """
    # Create sliders for each risk category with configured properties
    sliders = {
        risk_category: widgets.FloatSlider(
            value=boundaries[1] / len(risk_categories),
            min=boundaries[0],
            max=boundaries[1],
            step=step_size,
            description=f'Importance of {risk_category}',
            style={'description_width': '300px', 'bar_color': bar_color},
            layout={'width': '1000px'}
        ) for risk_category in risk_categories
    }

    # Function to validate that the sum of slider values equals 100
    def validate_sum(change=None):
        total = sum(slider.value for slider in sliders.values())
        output.clear_output()
        if total == 100:
            with output:
                display(HTML(f"<p style='color:green;'>Total: {total}% - Valid!</p>"))
        else:
            with output:
                display(HTML(f"<p style='color:red;'>Total: {total}% - Must equal 100%!</p>"))

    # Observe changes in each slider to trigger validation
    for slider in sliders.values():
        slider.observe(validate_sum, names='value')

    # Display the sliders and the validation message
    output = widgets.Output()
    slider_container = widgets.VBox(list(sliders.values()) + [output])
    validate_sum()  # Initial validation check

    return slider_container, sliders  # Return both the widget container and the sliders dictionary



def plot_order_volume_by_category(df, category_col, volume_col):
    """
    Plots a horizontal bar chart for order volume by a specified category.

    Parameters:
    - df (DataFrame): The DataFrame containing the data to plot.
    - category_col (str): The name of the column representing categories (e.g., 'Industry', 'Article').
    - volume_col (str): The name of the column representing order volumes.
                      
    Returns:
    - None: Displays a horizontal bar plot.
    """
    plt.figure(figsize=(10, 3))
    
    # Create the bar plot
    bars = plt.barh(df[category_col], df[volume_col], color='skyblue')

    # Adding labels to each bar
    for bar in bars:
        plt.text(
            bar.get_width() + 50000,  # Adding some padding to the text
            bar.get_y() + bar.get_height() / 2,
            f'${bar.get_width():,.2f}',
            va='center'
        )

    # Formatting the plot
    plt.xlabel('Order Volume')
    plt.title(f'{category_col} Order Volumes')
    plt.gca().invert_yaxis()  # Invert y-axis to keep the DataFrame's order
    plt.xticks(
        rotation=0,
        ticks=range(0, int(df[volume_col].max() * 1.1), 2000000),
        labels=[f'${x:,.0f}' for x in range(0, int(df[volume_col].max() * 1.1), 2000000)]
    )
    plt.tight_layout()

    # Display the plot
    plt.show()


def plot_volume_distribution_by_category(df, category_col, subcategory_col, volume_col, top_n=5):
    """
    Plots a pie chart for the distribution of order volume by subcategory within each category.

    Parameters:
    - df (DataFrame): The DataFrame containing the data to plot.
    - category_col (str): The name of the column representing the main category (e.g., product, region).
    - subcategory_col (str): The name of the column representing the subcategory (e.g., supplier, sub-region).
    - volume_col (str): The name of the column representing order volumes.
    - top_n (int): The number of top subcategories to display. Additional subcategories are grouped as 'Other'.
                      
    Returns:
    - None: Displays pie charts for each category's volume distribution.
    """
    # Group data by the main category column and iterate through each group
    for category, group in df.groupby(category_col):
        # Sort the group by volume in descending order and get the top subcategories
        top_subcategories = group.nlargest(top_n, volume_col)
        others = group[~group[subcategory_col].isin(top_subcategories[subcategory_col])]

        # Calculate 'Other' if there are more than top_n subcategories
        if not others.empty:
            other_volume = others[volume_col].sum()
            other_row = pd.DataFrame({subcategory_col: ['Other'], volume_col: [other_volume]})
            top_subcategories = pd.concat([top_subcategories, other_row], ignore_index=True)

        # Plotting the pie chart
        plt.figure(figsize=(10, 3))
        plt.pie(
            top_subcategories[volume_col],
            labels=None,  # Hide labels on the pie chart itself
            autopct='%1.1f%%',
            startangle=140
        )
        plt.title(f'{subcategory_col} Volume Distribution for {category}')

        # Adding a legend to the right with absolute values
        legend_labels = [
            f"{row[subcategory_col]} - ${row[volume_col]:,.2f}" for _, row in top_subcategories.iterrows()
        ]
        plt.legend(legend_labels, title=subcategory_col, loc="center left", bbox_to_anchor=(1, 0.5))
        
        plt.tight_layout()
        plt.show()


def plot_choropleth_subplots(df, country_col, human_rights_col, environmental_risk_col):
    """
    Creates a figure with two choropleth maps as subplots: one for human rights index and one for environmental risk.

    Parameters:
    - df (DataFrame): The DataFrame containing the data for the maps.
    - country_col (str): The name of the column representing country identifiers.
    - human_rights_col (str): The name of the column representing the human rights index.
    - environmental_risk_col (str): The name of the column representing the environmental risk.

    Returns:
    - fig (Figure): Plotly Figure with two choropleth maps as subplots.
    """
    # Create the figure with 1 row and 2 columns for subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Human Rights Index", "Environmental Risk"),
        specs=[[{"type": "choropleth"}, {"type": "choropleth"}]]
    )

    # First choropleth map for human rights index
    fig_human_rights = px.choropleth(
        df, locations=country_col, color=human_rights_col,
        hover_name=country_col, color_continuous_scale='RdYlGn'
    )
    fig_human_rights.update_geos(showcoastlines=True)
    
    # Second choropleth map for environmental risk
    fig_environmental_risk = px.choropleth(
        df, locations=country_col, color=environmental_risk_col,
        hover_name=country_col, color_continuous_scale='RdYlGn'
    )
    fig_environmental_risk.update_geos(showcoastlines=True)

    # Add the traces from each map to the subplots
    fig.add_trace(fig_human_rights.data[0], row=1, col=1)
    fig.add_trace(fig_environmental_risk.data[0], row=1, col=2)

    # Update layout for better appearance
    fig.update_layout(
        coloraxis_colorbar=dict(title="Index Value"),
        showlegend=False,
        title_text="Human Rights Index and Environmental Risk by Country",
        coloraxis=dict(colorscale='RdYlGn')
    )
    
    return fig


def style_dataframe(df):
    cmap = sns.color_palette("RdYlGn", as_cmap=True)

    ignore_cols = ['supplier_id', 'sum_of_order_volume', 'country', 'Industry']

    # Style the DataFrame with a consistent range for all columns
    styled_df = df.style.background_gradient(
        cmap=cmap, subset=[col for col in df.columns if not col in ignore_cols], vmin=0, vmax=100
    ).set_properties(**{
        'text-align': 'center',
        'width': '30px'  # Narrower width for each cell
    }).set_table_styles([
        {
            'selector': 'th.col_heading',
            'props': [
                ('transform', 'rotate(270deg)'),       # Rotate header text 270 degrees
                ('transform-origin', 'center'),        # Center the rotation to minimize offsets
                ('position', 'relative'),              # Use relative positioning for fine-tuning
                ('top', '70px'),                      # Move headers upwards to reduce gap
                ('line-height', '1'),                  # Compact line-height
                ('padding', '0px'),                    # Remove extra padding
                ('height', '250px'),                   # Set height for header cells
                ('width', '60px'),                     # Narrow width for header columns
            ]
        }
    ])

    # Convert styled DataFrame to HTML and wrap it in a unique <div> with ID
    html = styled_df.to_html()
    full_html = f"""
        <div id="unique_dataframe_style">
            <style>
                #unique_dataframe_style table {{ width: auto !important; }}
                #unique_dataframe_style th, #unique_dataframe_style td {{ width: 60px !important; max-width: 60px !important; }}
            </style>
            {html}
        </div>
    """
    return HTML(full_html)