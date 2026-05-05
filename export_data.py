"""
Data Export Module for Power BI Integration
Exports processed data, predictions, and customer segments in Power BI-ready format
"""

import pandas as pd
import numpy as np
from datetime import datetime


def export_processed_data(df, output_path='data/processed_data.csv'):
    """
    Export processed data with Power BI-friendly column names and formatting
    
    Args:
        df (pd.DataFrame): Preprocessed dataset
        output_path (str): Path to save the CSV file
        
    Returns:
        pd.DataFrame: Processed dataset ready for Power BI
    """
    print("\n📊 Exporting processed data for Power BI...")
    
    # Create a copy to avoid modifying original
    export_df = df.copy()
    
    # Standardize column names to snake_case
    column_mapping = {
        'User_ID': 'user_id',
        'Product_ID': 'product_id',
        'Category': 'category',
        'Price (Rs.)': 'original_price',
        'Discount (%)': 'discount_percentage',
        'Final_Price(Rs.)': 'final_price',
        'Payment_Method': 'payment_method',
        'Purchase_Date': 'purchase_date',
        'Purchase_Month': 'month',
        'Purchase_Year': 'year',
        'Purchase_Day': 'day',
        'Discount_Amount': 'discount_amount',
        'Discount_Level': 'discount_level'
    }
    
    export_df = export_df.rename(columns=column_mapping)
    
    # Add calculated columns for Power BI
    export_df['revenue'] = export_df['final_price']
    export_df['month_name'] = pd.to_datetime(export_df['purchase_date']).dt.strftime('%B')
    export_df['quarter'] = pd.to_datetime(export_df['purchase_date']).dt.quarter
    export_df['week_of_year'] = pd.to_datetime(export_df['purchase_date']).dt.isocalendar().week
    export_df['day_of_week'] = pd.to_datetime(export_df['purchase_date']).dt.day_name()
    
    # Round numeric columns to 2 decimal places
    numeric_cols = ['original_price', 'discount_percentage', 'final_price', 'revenue', 
                    'discount_amount']
    for col in numeric_cols:
        if col in export_df.columns:
            export_df[col] = export_df[col].round(2)
    
    # Select and order columns for Power BI
    columns_order = [
        'user_id', 'product_id', 'category', 'original_price', 'discount_percentage',
        'final_price', 'revenue', 'payment_method', 'purchase_date', 'year', 'month', 'day',
        'month_name', 'quarter', 'week_of_year', 'day_of_week', 'discount_amount', 'discount_level'
    ]
    
    export_df = export_df[columns_order]
    
    # Save to CSV without index
    export_df.to_csv(output_path, index=False)
    
    print(f"✅ Processed data exported!")
    print(f"   File: {output_path}")
    print(f"   Rows: {len(export_df):,}")
    print(f"   Columns: {len(export_df.columns)}")
    print(f"   Date Range: {export_df['purchase_date'].min()} to {export_df['purchase_date'].max()}")
    
    return export_df


def export_predictions(predictor, df, output_path='data/predictions.csv'):
    """
    Export sales predictions for Power BI
    
    Args:
        predictor: Trained SalesPredictor model
        df (pd.DataFrame): Original dataset (with engineered features)
        output_path (str): Path to save the CSV file
        
    Returns:
        pd.DataFrame: Predictions dataset
    """
    print("\n🤖 Exporting ML predictions for Power BI...")
    
    # Prepare features same way as training
    X = df[['Price (Rs.)', 'Discount (%)', 'Purchase_Month', 
             'Purchase_Year', 'Purchase_Day']].copy()
    
    # Encode categorical variables (same as in training)
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    X['Category_Encoded'] = le.fit_transform(df['Category'])
    X['Payment_Encoded'] = le.fit_transform(df['Payment_Method'])
    
    # Make predictions
    y_actual = df['Final_Price(Rs.)'].values
    y_predicted = predictor.predict(X)
    
    # Calculate error
    error = y_actual - y_predicted
    error_percentage = (error / y_actual * 100).round(2)
    
    # Create predictions dataframe
    predictions_df = pd.DataFrame({
        'product_id': df['Product_ID'].values,
        'user_id': df['User_ID'].values,
        'category': df['Category'].values,
        'actual_price': y_actual.round(2),
        'predicted_price': y_predicted.round(2),
        'error': error.round(2),
        'error_percentage': error_percentage,
        'purchase_date': df['Purchase_Date'].values
    })
    
    # Sort by error magnitude (largest errors first)
    predictions_df['abs_error'] = predictions_df['error'].abs()
    predictions_df = predictions_df.sort_values('abs_error', ascending=False).drop('abs_error', axis=1)
    
    # Save to CSV
    predictions_df.to_csv(output_path, index=False)
    
    print(f"✅ Predictions exported!")
    print(f"   File: {output_path}")
    print(f"   Rows: {len(predictions_df):,}")
    print(f"   Mean Absolute Error: ₹{predictions_df['error'].abs().mean():.2f}")
    print(f"   RMSE: ₹{(predictions_df['error'] ** 2).mean() ** 0.5:.2f}")
    
    return predictions_df


def export_customer_segments(segmentation, output_path='data/customer_segments.csv'):
    """
    Export customer segmentation results for Power BI
    
    Args:
        segmentation: Trained CustomerSegmentation model
        output_path (str): Path to save the CSV file
        
    Returns:
        pd.DataFrame: Customer segments dataset
    """
    print("\n👥 Exporting customer segments for Power BI...")
    
    # Get segments data from model
    segments_df = segmentation.features.copy()
    
    # Standardize column names to snake_case
    column_mapping = {
        'User_ID': 'user_id',
        'Total_Spending': 'total_spending',
        'Purchase_Frequency': 'purchase_frequency',
        'Avg_Discount': 'avg_discount',
        'Cluster': 'cluster'
    }
    
    segments_df = segments_df.rename(columns=column_mapping)
    
    # Add cluster descriptions for Power BI
    cluster_descriptions = {
        0: 'Low Value',
        1: 'VIP Customers',
        2: 'Regular Customers',
        3: 'Discount Hunters'
    }
    
    segments_df['cluster_name'] = segments_df['cluster'].map(cluster_descriptions)
    
    # Add customer value tier
    def get_value_tier(spending):
        if spending > segments_df['total_spending'].quantile(0.75):
            return 'High Value'
        elif spending > segments_df['total_spending'].quantile(0.50):
            return 'Medium Value'
        else:
            return 'Low Value'
    
    segments_df['customer_tier'] = segments_df['total_spending'].apply(get_value_tier)
    
    # Round numeric columns
    segments_df['total_spending'] = segments_df['total_spending'].round(2)
    segments_df['avg_discount'] = segments_df['avg_discount'].round(2)
    
    # Reorder columns
    columns_order = [
        'user_id', 'cluster', 'cluster_name', 'customer_tier',
        'total_spending', 'purchase_frequency', 'avg_discount'
    ]
    
    segments_df = segments_df[columns_order]
    
    # Save to CSV
    segments_df.to_csv(output_path, index=False)
    
    # Print summary statistics
    print(f"✅ Customer segments exported!")
    print(f"   File: {output_path}")
    print(f"   Customers: {len(segments_df):,}")
    print(f"\n   Cluster Distribution:")
    
    for cluster in sorted(segments_df['cluster'].unique()):
        cluster_data = segments_df[segments_df['cluster'] == cluster]
        percentage = (len(cluster_data) / len(segments_df) * 100)
        avg_spending = cluster_data['total_spending'].mean()
        print(f"   • {cluster_data['cluster_name'].iloc[0]}: {len(cluster_data):,} customers ({percentage:.1f}%) - Avg Spending: ₹{avg_spending:,.2f}")
    
    return segments_df


def export_all_powerbi_data(df, predictor, segmentation):
    """
    Main export function - exports all datasets for Power BI
    
    Args:
        df (pd.DataFrame): Preprocessed dataset
        predictor: Trained SalesPredictor model
        segmentation: Trained CustomerSegmentation model
    """
    print("\n" + "=" * 70)
    print("💾 EXPORTING DATA FOR POWER BI INTEGRATION")
    print("=" * 70)
    
    try:
        # Export processed data
        processed_df = export_processed_data(df)
        
        # Export predictions
        predictions_df = export_predictions(predictor, df)
        
        # Export customer segments
        segments_df = export_customer_segments(segmentation)
        
        print("\n" + "=" * 70)
        print("✅ ALL DATA EXPORTED SUCCESSFULLY!")
        print("=" * 70)
        print("\n📂 Power BI ready CSV files created:")
        print("   1. data/processed_data.csv")
        print("   2. data/predictions.csv")
        print("   3. data/customer_segments.csv")
        print("\n🔗 Next step: Connect these files to Power BI Desktop")
        
        return processed_df, predictions_df, segments_df
        
    except Exception as e:
        print(f"❌ Error during export: {e}")
        raise


if __name__ == "__main__":
    # Test the export module
    from data_preprocessing import preprocess_data
    from model import build_model
    
    print("Testing export module...")
    df = preprocess_data("data/ecommerce_dataset.csv")
    predictor = build_model(df, model_type='prediction')
    segmentation = build_model(df, model_type='clustering')
    
    export_all_powerbi_data(df, predictor, segmentation)
