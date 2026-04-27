"""
Data Preprocessing Module
Handles loading, cleaning, and feature engineering
"""

import pandas as pd
import numpy as np
from datetime import datetime


def load_data(filepath):
    """
    Load dataset from CSV file
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset
    """
    print("📂 Loading dataset...")
    df = pd.read_csv(filepath)
    print(f"✓ Dataset loaded successfully! Shape: {df.shape}")
    return df


def handle_missing_values(df):
    """
    Handle missing values in the dataset
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        pd.DataFrame: Dataset with missing values handled
    """
    print("\n🔍 Checking for missing values...")
    missing_counts = df.isnull().sum()
    
    if missing_counts.sum() > 0:
        print(f"Found missing values:\n{missing_counts[missing_counts > 0]}")
        # Drop rows with missing values for simplicity
        df = df.dropna()
        print(f"✓ Missing values removed. New shape: {df.shape}")
    else:
        print("✓ No missing values found!")
    
    return df


def remove_duplicates(df):
    """
    Remove duplicate records from dataset
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        pd.DataFrame: Dataset with duplicates removed
    """
    print("\n🔄 Checking for duplicates...")
    duplicates_count = df.duplicated().sum()
    
    if duplicates_count > 0:
        print(f"Found {duplicates_count} duplicate records")
        df = df.drop_duplicates()
        print(f"✓ Duplicates removed. New shape: {df.shape}")
    else:
        print("✓ No duplicates found!")
    
    return df


def convert_date_columns(df):
    """
    Convert date string to datetime format
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        pd.DataFrame: Dataset with converted date columns
    """
    print("\n📅 Converting date columns...")
    df['Purchase_Date'] = pd.to_datetime(df['Purchase_Date'], format='%d-%m-%Y')
    print("✓ Date column converted successfully!")
    
    return df


def feature_engineering(df):
    """
    Create new features from existing columns
    
    Args:
        df (pd.DataFrame): Input dataset
        
    Returns:
        pd.DataFrame: Dataset with engineered features
    """
    print("\n🔧 Performing feature engineering...")
    
    # Extract month from date
    df['Purchase_Month'] = df['Purchase_Date'].dt.month
    df['Purchase_Year'] = df['Purchase_Date'].dt.year
    df['Purchase_Day'] = df['Purchase_Date'].dt.day
    
    # Calculate discount amount
    df['Discount_Amount'] = df['Price (Rs.)'] - df['Final_Price(Rs.)']
    
    # Categorize discount level
    df['Discount_Level'] = pd.cut(df['Discount (%)'], 
                                   bins=[-1, 0, 15, 35, 51], 
                                   labels=['None', 'Low', 'Medium', 'High'])
    
    print("✓ Features created: Purchase_Month, Purchase_Year, Purchase_Day,")
    print("  Discount_Amount, Discount_Level")
    
    return df


def preprocess_data(filepath):
    """
    Main preprocessing pipeline
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Cleaned and preprocessed dataset
    """
    print("=" * 60)
    print("🚀 STARTING DATA PREPROCESSING PIPELINE")
    print("=" * 60)
    
    # Execute preprocessing steps
    df = load_data(filepath)
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = convert_date_columns(df)
    df = feature_engineering(df)
    
    print("\n" + "=" * 60)
    print("✅ PREPROCESSING COMPLETED SUCCESSFULLY")
    print("=" * 60)
    
    return df


if __name__ == "__main__":
    # Test the preprocessing module
    df = preprocess_data("data/ecommerce_dataset.csv")
    print("\nDataset Info:")
    print(df.info())
    print("\nFirst few rows:")
    print(df.head())
