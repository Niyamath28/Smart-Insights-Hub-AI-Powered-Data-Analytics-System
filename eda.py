"""
Exploratory Data Analysis (EDA) Module
Generates visualizations and statistical summaries
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt


def show_summary_statistics(df):
    """
    Display summary statistics of the dataset
    
    Args:
        df (pd.DataFrame): Input dataset
    """
    print("\n" + "=" * 60)
    print("📊 DATASET SUMMARY STATISTICS")
    print("=" * 60)
    
    print(f"\nDataset Shape: {df.shape}")
    print(f"Total Records: {df.shape[0]}")
    print(f"Total Features: {df.shape[1]}")
    
    print("\n" + "-" * 60)
    print("Numerical Statistics:")
    print("-" * 60)
    print(df[['Price (Rs.)', 'Discount (%)', 'Final_Price(Rs.)']].describe().round(2))
    
    print("\n" + "-" * 60)
    print("Categorical Overview:")
    print("-" * 60)
    print(f"Unique Categories: {df['Category'].nunique()}")
    print(f"\nCategory Distribution:\n{df['Category'].value_counts()}")
    
    print(f"\n\nPayment Methods: {df['Payment_Method'].nunique()}")
    print(f"\nPayment Method Distribution:\n{df['Payment_Method'].value_counts()}")


def plot_sales_by_category(df, save_path=None):
    """
    Create bar chart of sales by category
    
    Args:
        df (pd.DataFrame): Input dataset
        save_path (str): Path to save the figure
    """
    print("\n📊 Creating: Sales by Category...")
    
    # Calculate total sales per category
    sales_by_category = df.groupby('Category')['Final_Price(Rs.)'].sum().sort_values(ascending=False)
    
    # Create figure
    plt.figure(figsize=(12, 6))
    bars = plt.bar(sales_by_category.index, sales_by_category.values, color='steelblue', edgecolor='black')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'₹{height:,.0f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.title('Total Sales by Category', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Category', fontsize=12, fontweight='bold')
    plt.ylabel('Sales (Rs.)', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Chart saved")


def plot_monthly_sales_trend(df, save_path=None):
    """
    Create line chart of monthly sales trend
    
    Args:
        df (pd.DataFrame): Input dataset
        save_path (str): Path to save the figure
    """
    print("📊 Creating: Monthly Sales Trend...")
    
    # Group by month and sum sales
    monthly_sales = df.groupby(df['Purchase_Date'].dt.to_period('M'))['Final_Price(Rs.)'].sum()
    monthly_sales.index = monthly_sales.index.to_timestamp()
    
    # Create figure
    plt.figure(figsize=(14, 6))
    plt.plot(monthly_sales.index, monthly_sales.values, marker='o', 
             linewidth=2.5, markersize=8, color='darkgreen', label='Sales')
    
    # Add value labels
    for x, y in zip(monthly_sales.index, monthly_sales.values):
        plt.text(x, y, f'₹{y:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.title('Monthly Sales Trend', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Month', fontsize=12, fontweight='bold')
    plt.ylabel('Sales (Rs.)', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xticks(rotation=45, ha='right')
    plt.legend(fontsize=11)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Chart saved")


def plot_top_products(df, top_n=10, save_path=None):
    """
    Create bar chart of top N products by sales
    
    Args:
        df (pd.DataFrame): Input dataset
        top_n (int): Number of top products to display
        save_path (str): Path to save the figure
    """
    print(f"📊 Creating: Top {top_n} Products by Sales...")
    
    # Calculate top products
    top_products = df.groupby('Product_ID')['Final_Price(Rs.)'].sum().sort_values(ascending=False).head(top_n)
    
    # Create figure
    plt.figure(figsize=(12, 7))
    bars = plt.barh(range(len(top_products)), top_products.values, color='coral', edgecolor='black')
    plt.yticks(range(len(top_products)), top_products.index)
    
    # Add value labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f'₹{width:,.0f}',
                ha='left', va='center', fontsize=10, fontweight='bold', style='italic')
    
    plt.title(f'Top {top_n} Products by Total Sales', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Sales (Rs.)', fontsize=12, fontweight='bold')
    plt.ylabel('Product ID', fontsize=12, fontweight='bold')
    plt.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Chart saved")


def perform_eda(df):
    """
    Execute complete EDA pipeline
    
    Args:
        df (pd.DataFrame): Input dataset
    """
    print("\n" + "=" * 60)
    print("📈 STARTING EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 60)
    
    # Show statistics
    show_summary_statistics(df)
    
    # Create visualizations
    plot_sales_by_category(df)
    plot_monthly_sales_trend(df)
    plot_top_products(df, top_n=10)
    
    print("\n" + "=" * 60)
    print("✅ EDA COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    # Test the EDA module
    from data_preprocessing import preprocess_data
    df = preprocess_data("data/ecommerce_dataset.csv")
    perform_eda(df)
