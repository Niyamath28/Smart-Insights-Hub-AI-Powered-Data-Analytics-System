"""
Streamlit Dashboard for Smart Insights Hub
Interactive visualization and analysis dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from data_preprocessing import preprocess_data
from eda import plot_sales_by_category, plot_monthly_sales_trend, plot_top_products
from model import SalesPredictor, CustomerSegmentation
from insights import generate_insights


# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Smart Insights Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        h1 {
            color: #1f77b4;
            border-bottom: 3px solid #1f77b4;
            padding-bottom: 0.5rem;
        }
        h2 {
            color: #ff7f0e;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)


# ==================== SIDEBAR CONFIGURATION ====================
st.sidebar.title("🎛️ Navigation")
page = st.sidebar.radio(
    "Select Page:",
    ["🏠 Home", "📊 Dashboard", "🔍 Data Analysis", "🤖 Model Insights", "💡 Auto-Generated Insights"]
)

# Load data function
@st.cache_data
def load_processed_data():
    """Load preprocessed data"""
    if os.path.exists('data/processed_data.csv'):
        return pd.read_csv('data/processed_data.csv')
    else:
        # If processed data doesn't exist, run preprocessing
        return preprocess_data('data/ecommerce_dataset.csv')


# ==================== PAGE: HOME ====================
if page == "🏠 Home":
    st.markdown("""
    # 🚀 Smart Insights Hub
    ## AI-Powered Data Analytics System
    
    Welcome to **Smart Insights Hub** - a comprehensive end-to-end machine learning and data analytics system!
    
    ### 📌 What This System Does:
    - **📂 Data Loading**: Loads e-commerce datasets efficiently
    - **🧹 Data Preprocessing**: Cleans, transforms, and engineers features
    - **📊 Exploratory Analysis**: Generates comprehensive visualizations
    - **🤖 Machine Learning**: Implements prediction and clustering models
    - **💡 Insights**: Automatically generates actionable business insights
    - **📈 Dashboard**: Interactive Streamlit dashboard for exploration
    
    ### 🎯 Key Features:
    ✅ Sales Prediction using Linear Regression  
    ✅ Customer Segmentation using K-Means Clustering  
    ✅ Automatic Business Insights Generation  
    ✅ Interactive Charts and Visualizations  
    ✅ Real-time Data Analysis  
    
    ### 🚀 Quick Start:
    1. Navigate to **📊 Dashboard** to see overall metrics
    2. Check **🔍 Data Analysis** for detailed visualizations
    3. Review **🤖 Model Insights** for ML model performance
    4. Read **💡 Auto-Generated Insights** for business recommendations
    
    ---
    
    **Created as a demonstration of professional data science practices.**
    """)
    
    st.info("👉 Use the sidebar to navigate through different sections of the analysis!")


# ==================== PAGE: DASHBOARD ====================
elif page == "📊 Dashboard":
    st.title("📊 Smart Insights Hub - Main Dashboard")
    
    # Load data
    df = load_processed_data()
    df['Purchase_Date'] = pd.to_datetime(df['Purchase_Date'])
    
    # KPI Section
    st.subheader("📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Sales",
            value=f"₹{df['Final_Price(Rs.)'].sum():,.0f}"
        )
    
    with col2:
        st.metric(
            label="📦 Total Orders",
            value=f"{len(df):,}"
        )
    
    with col3:
        st.metric(
            label="👥 Unique Customers",
            value=f"{df['User_ID'].nunique():,}"
        )
    
    with col4:
        st.metric(
            label="💵 Average Order Value",
            value=f"₹{df['Final_Price(Rs.)'].mean():,.0f}"
        )
    
    # Additional metrics
    st.subheader("📊 Additional Metrics")
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            label="📂 Categories",
            value=f"{df['Category'].nunique()}"
        )
    
    with col6:
        st.metric(
            label="🛒 Product Variety",
            value=f"{df['Product_ID'].nunique():,}"
        )
    
    with col7:
        st.metric(
            label="💳 Payment Methods",
            value=f"{df['Payment_Method'].nunique()}"
        )
    
    with col8:
        st.metric(
            label="📅 Date Range",
            value=f"{(df['Purchase_Date'].max() - df['Purchase_Date'].min()).days} days"
        )
    
    # Dataset preview
    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)


# ==================== PAGE: DATA ANALYSIS ====================
elif page == "🔍 Data Analysis":
    st.title("🔍 Exploratory Data Analysis")
    
    # Load data
    df = load_processed_data()
    df['Purchase_Date'] = pd.to_datetime(df['Purchase_Date'])
    
    # Summary statistics
    st.subheader("📊 Summary Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Numerical Features**")
        st.dataframe(
            df[['Price (Rs.)', 'Discount (%)', 'Final_Price(Rs.)']].describe().round(2),
            use_container_width=True
        )
    
    with col2:
        st.write("**Categorical Features**")
        st.write(f"**Categories**: {df['Category'].nunique()}")
        st.write(f"**Payment Methods**: {df['Payment_Method'].nunique()}")
        st.write(f"**Unique Products**: {df['Product_ID'].nunique()}")
        st.write(f"**Unique Customers**: {df['User_ID'].nunique()}")
    
    # Visualizations
    st.subheader("📈 Sales by Category")
    try:
        fig, ax = plt.subplots(figsize=(12, 6))
        sales_by_category = df.groupby('Category')['Final_Price(Rs.)'].sum().sort_values(ascending=False)
        ax.bar(sales_by_category.index, sales_by_category.values, color='steelblue', edgecolor='black')
        ax.set_title('Total Sales by Category', fontsize=14, fontweight='bold')
        ax.set_xlabel('Category', fontweight='bold')
        ax.set_ylabel('Sales (Rs.)', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error creating chart: {e}")
    
    st.subheader("📅 Monthly Sales Trend")
    try:
        fig, ax = plt.subplots(figsize=(14, 6))
        monthly_sales = df.groupby(df['Purchase_Date'].dt.to_period('M'))['Final_Price(Rs.)'].sum()
        monthly_sales.index = monthly_sales.index.to_timestamp()
        ax.plot(monthly_sales.index, monthly_sales.values, marker='o', linewidth=2.5, markersize=8, color='darkgreen')
        ax.set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
        ax.set_xlabel('Month', fontweight='bold')
        ax.set_ylabel('Sales (Rs.)', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error creating chart: {e}")
    
    st.subheader("🏆 Top 10 Products by Sales")
    try:
        fig, ax = plt.subplots(figsize=(12, 7))
        top_products = df.groupby('Product_ID')['Final_Price(Rs.)'].sum().sort_values(ascending=False).head(10)
        ax.barh(range(len(top_products)), top_products.values, color='coral', edgecolor='black')
        ax.set_yticks(range(len(top_products)))
        ax.set_yticklabels(top_products.index)
        ax.set_title('Top 10 Products by Total Sales', fontsize=14, fontweight='bold')
        ax.set_xlabel('Sales (Rs.)', fontweight='bold')
        ax.invert_yaxis()
        plt.grid(axis='x', alpha=0.3)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error creating chart: {e}")
    
    # Category distribution
    st.subheader("📊 Category Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**By Number of Orders**")
        category_counts = df['Category'].value_counts()
        st.bar_chart(category_counts)
    
    with col2:
        st.write("**By Total Revenue**")
        category_revenue = df.groupby('Category')['Final_Price(Rs.)'].sum()
        st.bar_chart(category_revenue)


# ==================== PAGE: MODEL INSIGHTS ====================
elif page == "🤖 Model Insights":
    st.title("🤖 Machine Learning Model Insights")
    
    # Load data
    df = load_processed_data()
    df['Purchase_Date'] = pd.to_datetime(df['Purchase_Date'])
    
    st.subheader("🔧 Model Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Sales Prediction Model**
        - Algorithm: Linear Regression
        - Features: 7 engineered features
        - Target: Final Price (Sales)
        - Train/Test Split: 80/20
        """)
    
    with col2:
        st.info("""
        **Customer Segmentation Model**
        - Algorithm: K-Means Clustering
        - Number of Clusters: 4
        - Features: Spending, Frequency, Discount
        - Objective: Identify customer groups
        """)
    
    # Train models
    st.subheader("📊 Model Performance")
    
    with st.spinner("Training models..."):
        try:
            # Train prediction model
            predictor = SalesPredictor()
            predictor.train(df)
            
            # Train segmentation model
            segmentation = CustomerSegmentation(n_clusters=4)
            segmentation.train(df)
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="📈 Test R² Score",
                    value=f"{predictor.test_r2:.4f}",
                    delta="Prediction Accuracy"
                )
            
            with col2:
                st.metric(
                    label="💵 Mean Absolute Error",
                    value=f"₹{predictor.mae:.2f}"
                )
            
            with col3:
                st.metric(
                    label="📊 RMSE",
                    value=f"₹{predictor.rmse:.2f}"
                )
            
            # Visualize clusters
            st.subheader("👥 Customer Segments Visualization")
            fig, axes = plt.subplots(1, 2, figsize=(15, 6))
            
            colors = ['red', 'blue', 'green', 'purple']
            for cluster in range(4):
                mask = segmentation.features['Cluster'] == cluster
                axes[0].scatter(
                    segmentation.features[mask]['Total_Spending'],
                    segmentation.features[mask]['Purchase_Frequency'],
                    c=colors[cluster],
                    label=f'Cluster {cluster}',
                    s=100,
                    alpha=0.6,
                    edgecolors='black'
                )
            
            axes[0].set_xlabel('Total Spending (Rs.)', fontweight='bold')
            axes[0].set_ylabel('Purchase Frequency', fontweight='bold')
            axes[0].set_title('Spending vs Frequency', fontweight='bold')
            axes[0].legend()
            axes[0].grid(True, alpha=0.3)
            
            for cluster in range(4):
                mask = segmentation.features['Cluster'] == cluster
                axes[1].scatter(
                    segmentation.features[mask]['Purchase_Frequency'],
                    segmentation.features[mask]['Avg_Discount'],
                    c=colors[cluster],
                    label=f'Cluster {cluster}',
                    s=100,
                    alpha=0.6,
                    edgecolors='black'
                )
            
            axes[1].set_xlabel('Purchase Frequency', fontweight='bold')
            axes[1].set_ylabel('Average Discount (%)', fontweight='bold')
            axes[1].set_title('Frequency vs Discount', fontweight='bold')
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error training models: {e}")


# ==================== PAGE: AUTO-GENERATED INSIGHTS ====================
elif page == "💡 Auto-Generated Insights":
    st.title("💡 Auto-Generated Business Insights")
    
    # Load data
    df = load_processed_data()
    df['Purchase_Date'] = pd.to_datetime(df['Purchase_Date'])
    
    st.subheader("🔍 Key Findings")
    
    with st.spinner("Generating insights..."):
        try:
            # Train models
            predictor = SalesPredictor()
            predictor.train(df)
            
            segmentation = CustomerSegmentation(n_clusters=4)
            segmentation.train(df)
            
            # Generate insights
            insights, generator = generate_insights(df, predictor, segmentation)
            
            # Display insights
            for i, insight in enumerate(insights, 1):
                with st.container():
                    st.markdown(f"### {i}. {insight['title']}")
                    st.write(insight['description'])
                    st.divider()
            
        except Exception as e:
            st.error(f"Error generating insights: {e}")
    
    # Additional recommendations
    st.subheader("💼 Business Recommendations")
    
    recommendations = """
    1. **Focus on High-Performing Categories**: Allocate more marketing budget to top-selling categories
    
    2. **Optimize Discount Strategy**: Analyze the impact of different discount levels on sales volume
    
    3. **Target High-Value Customers**: Implement loyalty programs for top spending customers
    
    4. **Payment Method Enhancement**: Streamline and promote the most preferred payment methods
    
    5. **Seasonal Planning**: Plan inventory based on monthly sales patterns
    
    6. **Customer Segmentation**: Tailor marketing strategies for each customer segment
    
    7. **Product Recommendations**: Use clustering insights for personalized recommendations
    """
    
    st.info(recommendations)


# ==================== FOOTER ====================
st.sidebar.markdown("---")
st.sidebar.markdown("""
    ### 📊 Smart Insights Hub
    *AI-Powered Data Analytics System*
    
    **Technologies Used:**
    - Python, Pandas, NumPy
    - Scikit-Learn (ML)
    - Matplotlib (Visualization)
    - Streamlit (Dashboard)
    
    **Version:** 1.0  
    **Status:** ✅ Active
""")
