"""
Machine Learning Model Module
Implements sales prediction and customer segmentation
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


class SalesPredictor:
    """Sales Prediction Model using Linear Regression"""
    
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.train_r2 = None
        self.test_r2 = None
        self.mae = None
        self.rmse = None
    
    def prepare_features(self, df):
        """
        Prepare features for sales prediction
        
        Args:
            df (pd.DataFrame): Input dataset
            
        Returns:
            tuple: Features (X) and target (y)
        """
        print("\n🔧 Preparing features for sales prediction...")
        
        # Create feature set
        X = df[['Price (Rs.)', 'Discount (%)', 'Purchase_Month', 
                 'Purchase_Year', 'Purchase_Day']].copy()
        
        # Encode categorical variables
        le = LabelEncoder()
        X['Category_Encoded'] = le.fit_transform(df['Category'])
        X['Payment_Encoded'] = le.fit_transform(df['Payment_Method'])
        
        # Target variable
        y = df['Final_Price(Rs.)'].copy()
        
        print(f"✓ Features prepared: {X.shape[1]} features, {len(X)} samples")
        
        return X, y
    
    def train(self, df, test_size=0.2, random_state=42):
        """
        Train the sales prediction model
        
        Args:
            df (pd.DataFrame): Input dataset
            test_size (float): Test set size ratio
            random_state (int): Random state for reproducibility
        """
        print("\n" + "=" * 60)
        print("🤖 TRAINING SALES PREDICTION MODEL")
        print("=" * 60)
        
        # Prepare features
        X, y = self.prepare_features(df)
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        print(f"\n📊 Data Split:")
        print(f"   Training set: {len(self.X_train)} samples ({100*(1-test_size):.0f}%)")
        print(f"   Testing set: {len(self.X_test)} samples ({100*test_size:.0f}%)")
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        # Train model
        print("\n🚀 Training Linear Regression model...")
        self.model.fit(self.X_train_scaled, self.y_train)
        
        # Evaluate
        self.train_r2 = self.model.score(self.X_train_scaled, self.y_train)
        self.test_r2 = self.model.score(self.X_test_scaled, self.y_test)
        
        y_pred = self.model.predict(self.X_test_scaled)
        self.mae = mean_absolute_error(self.y_test, y_pred)
        self.rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
        
        print("\n" + "-" * 60)
        print("📈 MODEL PERFORMANCE")
        print("-" * 60)
        print(f"Training R² Score: {self.train_r2:.4f}")
        print(f"Testing R² Score: {self.test_r2:.4f}")
        print(f"Mean Absolute Error (MAE): ₹{self.mae:.2f}")
        print(f"Root Mean Squared Error (RMSE): ₹{self.rmse:.2f}")
        print("-" * 60)
        
        if self.test_r2 > 0.8:
            print("✅ Model Performance: EXCELLENT")
        elif self.test_r2 > 0.6:
            print("✅ Model Performance: GOOD")
        else:
            print("⚠️  Model Performance: FAIR (may need improvement)")
        
        return self
    
    def predict(self, X):
        """
        Make predictions
        
        Args:
            X (pd.DataFrame): Feature set
            
        Returns:
            np.array: Predicted values
        """
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def get_feature_importance(self, feature_names):
        """
        Get feature importance from model coefficients
        
        Args:
            feature_names (list): Names of features
            
        Returns:
            pd.DataFrame: Feature importance
        """
        importance = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': self.model.coef_,
            'Abs_Coefficient': np.abs(self.model.coef_)
        }).sort_values('Abs_Coefficient', ascending=False)
        
        return importance


class CustomerSegmentation:
    """Customer Segmentation using K-Means Clustering"""
    
    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.model = None
        self.scaler = StandardScaler()
        self.features = None
        self.labels = None
    
    def prepare_features(self, df):
        """
        Prepare features for clustering
        
        Args:
            df (pd.DataFrame): Input dataset
            
        Returns:
            pd.DataFrame: Prepared features
        """
        print("\n🔧 Preparing features for customer segmentation...")
        
        # Create customer-level features
        customer_data = df.groupby('User_ID').agg({
            'Final_Price(Rs.)': 'sum',  # Total spending
            'Product_ID': 'count',       # Purchase frequency
            'Discount (%)': 'mean'       # Average discount used
        }).rename(columns={
            'Final_Price(Rs.)': 'Total_Spending',
            'Product_ID': 'Purchase_Frequency',
            'Discount (%)': 'Avg_Discount'
        }).reset_index()
        
        print(f"✓ Features prepared for {len(customer_data)} unique customers")
        
        return customer_data
    
    def train(self, df):
        """
        Train customer segmentation model
        
        Args:
            df (pd.DataFrame): Input dataset
        """
        print("\n" + "=" * 60)
        print("🤖 TRAINING CUSTOMER SEGMENTATION MODEL")
        print("=" * 60)
        
        # Prepare features
        customer_data = self.prepare_features(df)
        
        # Extract features
        features = customer_data[['Total_Spending', 'Purchase_Frequency', 'Avg_Discount']]
        self.features = customer_data
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Train K-Means
        print(f"\n🚀 Training K-Means clustering with {self.n_clusters} clusters...")
        self.model = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        self.labels = self.model.fit_predict(features_scaled)
        
        # Add cluster labels
        self.features['Cluster'] = self.labels
        
        print("\n" + "-" * 60)
        print("📊 CLUSTER DISTRIBUTION")
        print("-" * 60)
        
        for cluster in range(self.n_clusters):
            count = (self.labels == cluster).sum()
            percentage = (count / len(self.labels)) * 100
            print(f"Cluster {cluster}: {count} customers ({percentage:.1f}%)")
        
        print("-" * 60)
        
        # Show cluster characteristics
        self._show_cluster_characteristics()
        
        return self
    
    def _show_cluster_characteristics(self):
        """Show characteristics of each cluster"""
        
        print("\n" + "-" * 60)
        print("📈 CLUSTER CHARACTERISTICS")
        print("-" * 60)
        
        cluster_summary = self.features.groupby('Cluster').agg({
            'Total_Spending': ['mean', 'min', 'max'],
            'Purchase_Frequency': ['mean', 'min', 'max'],
            'Avg_Discount': ['mean', 'min', 'max']
        }).round(2)
        
        for cluster in range(self.n_clusters):
            cluster_data = self.features[self.features['Cluster'] == cluster]
            print(f"\n🔹 Cluster {cluster}:")
            print(f"   Avg Spending: ₹{cluster_data['Total_Spending'].mean():,.2f}")
            print(f"   Avg Purchase Frequency: {cluster_data['Purchase_Frequency'].mean():.1f}")
            print(f"   Avg Discount Used: {cluster_data['Avg_Discount'].mean():.1f}%")
    
    def visualize_clusters(self, save_path=None):
        """
        Visualize clusters
        
        Args:
            save_path (str): Path to save the figure
        """
        print("\n📊 Creating cluster visualization...")
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Total Spending vs Purchase Frequency
        colors = ['red', 'blue', 'green', 'purple']
        for cluster in range(self.n_clusters):
            mask = self.features['Cluster'] == cluster
            axes[0].scatter(
                self.features[mask]['Total_Spending'],
                self.features[mask]['Purchase_Frequency'],
                c=colors[cluster % len(colors)],
                label=f'Cluster {cluster}',
                s=100,
                alpha=0.6,
                edgecolors='black'
            )
        
        axes[0].set_xlabel('Total Spending (Rs.)', fontsize=11, fontweight='bold')
        axes[0].set_ylabel('Purchase Frequency', fontsize=11, fontweight='bold')
        axes[0].set_title('Customer Segments: Spending vs Frequency', fontsize=12, fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Purchase Frequency vs Avg Discount
        for cluster in range(self.n_clusters):
            mask = self.features['Cluster'] == cluster
            axes[1].scatter(
                self.features[mask]['Purchase_Frequency'],
                self.features[mask]['Avg_Discount'],
                c=colors[cluster % len(colors)],
                label=f'Cluster {cluster}',
                s=100,
                alpha=0.6,
                edgecolors='black'
            )
        
        axes[1].set_xlabel('Purchase Frequency', fontsize=11, fontweight='bold')
        axes[1].set_ylabel('Average Discount (%)', fontsize=11, fontweight='bold')
        axes[1].set_title('Customer Segments: Frequency vs Discount', fontsize=12, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Visualization created")


def build_model(df, model_type='prediction'):
    """
    Main model building function
    
    Args:
        df (pd.DataFrame): Preprocessed dataset
        model_type (str): 'prediction' or 'clustering'
        
    Returns:
        Model object
    """
    if model_type == 'prediction':
        predictor = SalesPredictor()
        predictor.train(df)
        return predictor
    
    elif model_type == 'clustering':
        segmentation = CustomerSegmentation(n_clusters=4)
        segmentation.train(df)
        segmentation.visualize_clusters()
        return segmentation
    
    else:
        raise ValueError("model_type must be 'prediction' or 'clustering'")


if __name__ == "__main__":
    # Test the model module
    from data_preprocessing import preprocess_data
    df = preprocess_data("data/ecommerce_dataset.csv")
    
    # Train prediction model
    predictor = build_model(df, model_type='prediction')
    
    # Train clustering model
    segmentation = build_model(df, model_type='clustering')
