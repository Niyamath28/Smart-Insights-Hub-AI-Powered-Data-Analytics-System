"""
Insights Generation Module
Automatically generates meaningful insights from the data
"""

import pandas as pd
import numpy as np
from datetime import datetime


class InsightGenerator:
    """Generate actionable insights from data"""
    
    def __init__(self, df, model_predictor=None, model_clustering=None):
        """
        Initialize insight generator
        
        Args:
            df (pd.DataFrame): Preprocessed dataset
            model_predictor: Sales prediction model (optional)
            model_clustering: Customer segmentation model (optional)
        """
        self.df = df
        self.predictor = model_predictor
        self.segmentation = model_clustering
        self.insights = []
    
    def generate_all_insights(self):
        """Generate all available insights"""
        
        print("\n" + "=" * 60)
        print("💡 GENERATING INSIGHTS")
        print("=" * 60)
        
        self._insight_highest_sales_category()
        self._insight_best_performing_month()
        self._insight_payment_method_preference()
        self._insight_discount_impact()
        self._insight_average_order_value()
        self._insight_top_customer()
        self._insight_sales_growth()
        
        if self.predictor:
            self._insight_model_performance()
        
        if self.segmentation:
            self._insight_customer_segments()
        
        self._print_all_insights()
        
        return self.insights
    
    def _insight_highest_sales_category(self):
        """Insight: Highest sales category"""
        
        sales_by_category = self.df.groupby('Category')['Final_Price(Rs.)'].sum().sort_values(ascending=False)
        top_category = sales_by_category.index[0]
        top_sales = sales_by_category.values[0]
        
        insight = {
            'title': '🏆 Highest Sales Category',
            'description': f"'{top_category}' leads with ₹{top_sales:,.2f} in total sales"
        }
        
        self.insights.append(insight)
    
    def _insight_best_performing_month(self):
        """Insight: Best performing month"""
        
        monthly_sales = self.df.groupby('Purchase_Month')['Final_Price(Rs.)'].sum().sort_values(ascending=False)
        best_month = monthly_sales.index[0]
        month_name = pd.Timestamp(year=2024, month=best_month, day=1).strftime('%B')
        best_sales = monthly_sales.values[0]
        
        insight = {
            'title': '📈 Best Performing Month',
            'description': f"{month_name} (Month {best_month}) was the best with ₹{best_sales:,.2f} in sales"
        }
        
        self.insights.append(insight)
    
    def _insight_payment_method_preference(self):
        """Insight: Payment method preference"""
        
        payment_dist = self.df['Payment_Method'].value_counts()
        top_payment = payment_dist.index[0]
        top_count = payment_dist.values[0]
        percentage = (top_count / len(self.df)) * 100
        
        insight = {
            'title': '💳 Payment Method Preference',
            'description': f"{top_payment} is the most preferred payment method ({percentage:.1f}% of transactions)"
        }
        
        self.insights.append(insight)
    
    def _insight_discount_impact(self):
        """Insight: Discount impact on sales"""
        
        high_discount = self.df[self.df['Discount (%)'] >= 30]['Final_Price(Rs.)'].mean()
        low_discount = self.df[self.df['Discount (%)'] < 10]['Final_Price(Rs.)'].mean()
        
        insight = {
            'title': '🎁 Discount Impact',
            'description': f"High discounts (30%+) average ₹{high_discount:,.2f}, while low discounts (<10%) average ₹{low_discount:,.2f}"
        }
        
        self.insights.append(insight)
    
    def _insight_average_order_value(self):
        """Insight: Average order value"""
        
        avg_order = self.df['Final_Price(Rs.)'].mean()
        median_order = self.df['Final_Price(Rs.)'].median()
        
        insight = {
            'title': '💰 Average Order Value',
            'description': f"Average order value: ₹{avg_order:,.2f} | Median order value: ₹{median_order:,.2f}"
        }
        
        self.insights.append(insight)
    
    def _insight_top_customer(self):
        """Insight: Top customer by spending"""
        
        top_customer_spending = self.df.groupby('User_ID')['Final_Price(Rs.)'].sum().sort_values(ascending=False)
        top_customer_id = top_customer_spending.index[0]
        top_customer_amount = top_customer_spending.values[0]
        top_customer_orders = (self.df['User_ID'] == top_customer_id).sum()
        
        insight = {
            'title': '⭐ Top Customer',
            'description': f"Customer {top_customer_id} spent ₹{top_customer_amount:,.2f} across {top_customer_orders} orders"
        }
        
        self.insights.append(insight)
    
    def _insight_sales_growth(self):
        """Insight: Sales growth trend"""
        
        monthly_sales = self.df.groupby('Purchase_Month')['Final_Price(Rs.)'].sum()
        
        if len(monthly_sales) > 1:
            growth_rate = ((monthly_sales.values[-1] - monthly_sales.values[0]) / monthly_sales.values[0]) * 100
            trend = "📈 Growing" if growth_rate > 0 else "📉 Declining"
            
            insight = {
                'title': trend + ' Sales Trend',
                'description': f"Sales trend shows {abs(growth_rate):.1f}% {'growth' if growth_rate > 0 else 'decline'} over the period"
            }
        else:
            insight = {
                'title': '📊 Sales Trend',
                'description': "Insufficient data for trend analysis"
            }
        
        self.insights.append(insight)
    
    def _insight_model_performance(self):
        """Insight: Model performance"""
        
        r2_score = self.predictor.test_r2
        
        insight = {
            'title': '🤖 Prediction Model Performance',
            'description': f"Sales prediction model achieved {r2_score:.2%} accuracy on test data"
        }
        
        self.insights.append(insight)
    
    def _insight_customer_segments(self):
        """Insight: Customer segments"""
        
        seg_data = self.segmentation.features
        num_clusters = self.segmentation.n_clusters
        
        # Find highest-value segment
        avg_spending_by_cluster = seg_data.groupby('Cluster')['Total_Spending'].mean()
        best_cluster = avg_spending_by_cluster.idxmax()
        best_cluster_avg = avg_spending_by_cluster.max()
        
        insight = {
            'title': '👥 Customer Segmentation',
            'description': f"Identified {num_clusters} customer segments. Cluster {best_cluster} has highest avg spending: ₹{best_cluster_avg:,.2f}"
        }
        
        self.insights.append(insight)
    
    def _print_all_insights(self):
        """Print all insights in formatted way"""
        
        print("\n" + "-" * 60)
        print("KEY INSIGHTS & FINDINGS")
        print("-" * 60)
        
        for i, insight in enumerate(self.insights, 1):
            print(f"\n{i}. {insight['title']}")
            print(f"   {insight['description']}")
        
        print("\n" + "=" * 60)
    
    def get_insights_dataframe(self):
        """Get insights as DataFrame"""
        return pd.DataFrame(self.insights)


def generate_insights(df, model_predictor=None, model_clustering=None):
    """
    Generate insights from data
    
    Args:
        df (pd.DataFrame): Preprocessed dataset
        model_predictor: Sales prediction model (optional)
        model_clustering: Customer segmentation model (optional)
        
    Returns:
        list: List of insights
    """
    generator = InsightGenerator(df, model_predictor, model_clustering)
    insights = generator.generate_all_insights()
    
    return insights, generator


if __name__ == "__main__":
    # Test the insights module
    from data_preprocessing import preprocess_data
    from model import build_model
    
    df = preprocess_data("data/ecommerce_dataset.csv")
    predictor = build_model(df, model_type='prediction')
    segmentation = build_model(df, model_type='clustering')
    
    insights, generator = generate_insights(df, predictor, segmentation)
