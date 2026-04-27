"""
Smart Insights Hub: AI-Powered Data Analytics System
Main Execution File

This script orchestrates the entire pipeline:
1. Data Preprocessing
2. Exploratory Data Analysis
3. Machine Learning Model Training
4. Insights Generation
"""

import sys
import os
from data_preprocessing import preprocess_data
from eda import perform_eda
from model import build_model
from insights import generate_insights


def print_header():
    """Print project header"""
    header = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║         🚀 SMART INSIGHTS HUB 🚀                            ║
    ║      AI-Powered Data Analytics System                       ║
    ║                                                              ║
    ║   End-to-End ML Pipeline: Data → Analysis → Insights        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(header)


def print_footer():
    """Print project footer"""
    footer = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              ✅ ANALYSIS COMPLETE ✅                         ║
    ║                                                              ║
    ║  Next Steps:                                                 ║
    ║  1. Review the insights above                               ║
    ║  2. Run 'streamlit run app.py' for interactive dashboard    ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(footer)


def main():
    """Main execution function"""
    
    print_header()
    
    # Verify data file exists
    data_path = "data/ecommerce_dataset.csv"
    if not os.path.exists(data_path):
        print(f"❌ ERROR: Dataset not found at {data_path}")
        print("Please ensure the CSV file is in the 'data' folder.")
        sys.exit(1)
    
    # Step 1: Data Preprocessing
    print("\n" + "=" * 70)
    print("STEP 1: DATA PREPROCESSING")
    print("=" * 70)
    try:
        df = preprocess_data(data_path)
        print("✅ Data preprocessing completed successfully!")
    except Exception as e:
        print(f"❌ Error in data preprocessing: {e}")
        sys.exit(1)
    
    # Step 2: Exploratory Data Analysis (EDA)
    print("\n" + "=" * 70)
    print("STEP 2: EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 70)
    try:
        perform_eda(df)
        print("✅ EDA completed successfully!")
    except Exception as e:
        print(f"❌ Error in EDA: {e}")
        sys.exit(1)
    
    # Step 3: Machine Learning Models
    print("\n" + "=" * 70)
    print("STEP 3: MACHINE LEARNING MODEL TRAINING")
    print("=" * 70)
    try:
        # Train sales prediction model
        print("\n🔹 Building Sales Prediction Model...")
        predictor = build_model(df, model_type='prediction')
        print("✅ Sales prediction model trained successfully!")
        
        # Train customer segmentation model
        print("\n🔹 Building Customer Segmentation Model...")
        segmentation = build_model(df, model_type='clustering')
        print("✅ Customer segmentation model trained successfully!")
        
    except Exception as e:
        print(f"❌ Error in model training: {e}")
        sys.exit(1)
    
    # Step 4: Insights Generation
    print("\n" + "=" * 70)
    print("STEP 4: INSIGHTS GENERATION")
    print("=" * 70)
    try:
        insights, generator = generate_insights(df, predictor, segmentation)
        print("✅ Insights generated successfully!")
    except Exception as e:
        print(f"❌ Error in insights generation: {e}")
        sys.exit(1)
    
    # Print footer
    print_footer()
    
    # Save dataframe for use in Streamlit app
    print("\n💾 Saving processed data for dashboard...")
    df.to_csv('data/processed_data.csv', index=False)
    print("✓ Data saved to 'data/processed_data.csv'")
    
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"Total Records Processed: {len(df)}")
    print(f"Total Features Analyzed: {df.shape[1]}")
    print(f"Unique Categories: {df['Category'].nunique()}")
    print(f"Date Range: {df['Purchase_Date'].min().date()} to {df['Purchase_Date'].max().date()}")
    print(f"Total Sales: ₹{df['Final_Price(Rs.)'].sum():,.2f}")
    print("=" * 70)
    
    print("\n🎉 Smart Insights Hub execution completed successfully!")
    print("\n📌 To view the interactive dashboard, run:")
    print("   streamlit run app.py")


if __name__ == "__main__":
    main()
