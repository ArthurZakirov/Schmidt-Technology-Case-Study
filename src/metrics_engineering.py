import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


# Create a copy of the DataFrame for transformation
def engineer_metrics(df):
    metrics_df = df.copy()

    # Manually scale and invert `human_rights_index` and `environmental_risk`
    metrics_df['social_score'] = metrics_df['human_rights_index'].astype(int)
    metrics_df['environmental_score'] = metrics_df['environmental_risk'].astype(int)

    # Use MinMaxScaler for `sum_of_order_volume` and `total_company_revenue`
    boundaries = [0, 100]
    scaler_direct = MinMaxScaler(feature_range=(boundaries[0], boundaries[1]))
    
    metrics_df['financial_score'] = scaler_direct.fit_transform(np.log10(metrics_df[['total_company_revenue']] + 1)).astype(int)

    # Convert `certificates_valid` and `status` to binary with inversion
    metrics_df['regulatory_score'] = metrics_df['certificates_valid'].apply(lambda x: boundaries[1] if x == 'Yes' else boundaries[0])
    metrics_df['operational_score'] = metrics_df['status'].apply(lambda x: boundaries[1] if x == 'Active' else boundaries[0])

    metrics_df['independance_score'] = boundaries[1] - scaler_direct.fit_transform(metrics_df[['sum_of_order_volume']]).astype(int)
    # Drop original columns if you only want the transformed columns
    metrics_df = metrics_df.drop(columns=[
        'human_rights_index', 
        'environmental_risk',
        'sum_of_order_volume', 
        'total_company_revenue', 
        'certificates_valid', 
        'status'
    ])

    return metrics_df
