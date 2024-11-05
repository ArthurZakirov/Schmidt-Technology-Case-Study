import pandas as pd
from ipywidgets import Dropdown, interact
from IPython.display import display
from abc import ABC, abstractmethod

# Define an abstract base class for the scoring strategy
class RiskScoringStrategy(ABC):
    @abstractmethod
    def calculate(self, row, **kwargs):
        pass

# Implement the WeightedSumStrategy subclass
class WeightedSumStrategy(RiskScoringStrategy):
    def calculate(self, row, **kwargs):
        """
        Dynamic weighted sum method using kwargs to pass weights and corresponding column names.
        
        Args:
            row (dict or Series): Row of data containing risk values.
            kwargs: Dictionary of weights where the key is the column name in `row` and 
                    the value is the weight for that column.
                    
        Returns:
            float: Calculated risk score.
        """
        score = sum(weight * row[column] for column, weight in kwargs.items())
        return score

# Implement the ThresholdCountStrategy subclass
class ThresholdCountStrategy(RiskScoringStrategy):
    def calculate(self, row, **kwargs):
        """
        Dynamic threshold-based scoring method where each risk factor is checked against a specified threshold.
        Returns the count of risk factors that exceed their threshold.
        
        Args:
            row (dict or Series): Row of data containing risk values.
            kwargs: Dictionary where the key is the column name in `row` and the value is the threshold for that column.
                    
        Returns:
            int: Count of high-risk factors.
        """
        risk_factors = [row[column] > threshold for column, threshold in kwargs.items()]
        return sum(risk_factors)  # Counts the number of high-risk factors
    
class WeightedGeometricMeanStrategy(RiskScoringStrategy):
    def calculate(self, row, **kwargs):
        """
        Weighted geometric mean method using kwargs to pass weights and corresponding column names.
        
        Args:
            row (dict or Series): Row of data containing risk values.
            kwargs: Dictionary of weights where the key is the column name in `row` and 
                    the value is the weight for that column.
                    
        Returns:
            float: Calculated risk score scaled to range [0, 100].
        """
        # Normalize each value to [0, 1], raise to weight, multiply results
        score_product = 1
        for column, weight in kwargs.items():
            normalized_value = row[column] / 100  # Scale each value to [0, 1]
            if normalized_value == 0:
                return 0  # If any value is 0, the geometric mean should be 0
            score_product *= normalized_value ** weight

        # Rescale back to [0, 100]
        return score_product * 100

# Wrapper function to compute quantitative risk score using the selected strategy
def calculate_quantitative_risk_score(df, **kwargs):
    """
    Wrapper function to calculate the quantitative risk score using a specified strategy object.
    
    Parameters:
    - df (DataFrame): The DataFrame containing the relevant columns.
    - strategy (RiskScoringStrategy): An instance of a subclass of RiskScoringStrategy.
    - **kwargs: Additional configuration parameters for the specific strategy.
    
    Returns:
    - DataFrame: A DataFrame with the 'quantitative_risk_score' column.
    """
    if selected_strategy is None:
        print("Please select a strategy first.")
        return
    
    # Apply the strategy to each row
    score_series = df.apply(lambda row: selected_strategy.calculate(row, **kwargs), axis=1).astype(int)
    
    # Convert the Series to DataFrame with column name
    return pd.DataFrame({'quantitative_risk_score': score_series})

selected_strategy = None

# Define the function to get the strategy selection widget
def get_strategy_selector_widget():
    global selected_strategy

    # Create the dropdown widget
    strategy_selector = Dropdown(
        options={
            'Weighted Sum': WeightedSumStrategy(),
            'Weighted Geometric Mean': WeightedGeometricMeanStrategy()
        },
        description='Select Strategy:',
        style={'description_width': 'initial'}
    )

    # Update the global `selected_strategy` variable when selection changes
    def on_strategy_change(change):
        global selected_strategy
        selected_strategy = change.new
        print(f"Selected strategy: {type(selected_strategy).__name__}")

    # Attach the event handler to capture selection changes
    strategy_selector.observe(on_strategy_change, names='value')
    
    # Display the widget
    display(strategy_selector)