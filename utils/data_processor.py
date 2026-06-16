"""
Data processing utilities for invoice analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime


class InvoiceProcessor:
    """Main processor for invoice data"""

    def __init__(self):
        self.df = None
        self.filtered_df = None
        self.summary_stats = {}

    def load_data(self, df):
        """Load and validate dataframe"""
        self.df = df.copy()
        self.filtered_df = self.df.copy()
        self._validate_columns()
        self._preprocess_data()
        self._calculate_summary()

    def _validate_columns(self):
        """Validate required columns"""
        required = ['amount']
        for col in required:
            if col not in self.df.columns:
                print(f"Warning: {col} column not found")

    def _preprocess_data(self):
        """Clean and preprocess data"""
        # Convert amount to numeric
        if 'amount' in self.df.columns:
            self.df['amount'] = pd.to_numeric(self.df['amount'], errors='coerce')

        # Convert date columns
        date_cols = [col for col in self.df.columns if 'date' in col.lower()]
        for col in date_cols:
            self.df[col] = pd.to_datetime(self.df[col], errors='coerce')

        # Remove duplicates
        self.df = self.df.drop_duplicates()

    def _calculate_summary(self):
        """Calculate summary statistics"""
        if self.df is not None and 'amount' in self.df.columns:
            self.summary_stats = {
                'total_revenue': self.df['amount'].sum(),
                'avg_invoice': self.df['amount'].mean(),
                'median_invoice': self.df['amount'].median(),
                'total_invoices': len(self.df),
                'min_amount': self.df['amount'].min(),
                'max_amount': self.df['amount'].max()
            }

    def get_top_products(self, n=10):
        """Get top products by revenue"""
        if 'product_id' in self.df.columns and 'amount' in self.df.columns:
            return self.df.groupby('product_id')['amount'].sum().sort_values(ascending=False).head(n)
        return pd.Series()

    def get_top_customers(self, n=10):
        """Get top customers by spending"""
        if 'email' in self.df.columns and 'amount' in self.df.columns:
            if 'first_name' in self.df.columns and 'last_name' in self.df.columns:
                self.df['customer_name'] = self.df['first_name'] + ' ' + self.df['last_name']
                return self.df.groupby(['customer_name', 'email'])['amount'].sum().sort_values(ascending=False).head(n)
            return self.df.groupby('email')['amount'].sum().sort_values(ascending=False).head(n)
        return pd.Series()

    def get_revenue_by_city(self):
        """Get revenue grouped by city"""
        if 'city' in self.df.columns and 'amount' in self.df.columns:
            return self.df.groupby('city')['amount'].sum().sort_values(ascending=False)
        return pd.Series()

    def get_monthly_trend(self):
        """Get monthly revenue trend"""
        if 'invoice_date' in self.df.columns and 'amount' in self.df.columns:
            self.df['month'] = self.df['invoice_date'].dt.to_period('M')
            return self.df.groupby('month')['amount'].sum()
        return pd.Series()

    def generate_insights(self):
        """Generate business insights"""
        insights = []

        if self.summary_stats:
            insights.append(
                f"💰 **Total Revenue**: ${self.summary_stats['total_revenue']:,.2f} from {self.summary_stats['total_invoices']:,} invoices")
            insights.append(f"📊 **Average Invoice**: ${self.summary_stats['avg_invoice']:.2f}")

        top_products = self.get_top_products(3)
        if len(top_products) > 0:
            insights.append(
                f"🏆 **Top Products**: Product {top_products.index[0]} generates the most revenue (${top_products.iloc[0]:,.2f})")

        top_customers = self.get_top_customers(3)
        if len(top_customers) > 0:
            if isinstance(top_customers.index[0], tuple):
                insights.append(
                    f"👥 **Top Customer**: {top_customers.index[0][0]} spends the most (${top_customers.iloc[0]:,.2f})")
            else:
                insights.append(
                    f"👥 **Top Customer**: {top_customers.index[0]} spends the most (${top_customers.iloc[0]:,.2f})")

        city_revenue = self.get_revenue_by_city()
        if len(city_revenue) > 0:
            insights.append(
                f"📍 **Top Location**: {city_revenue.index[0]} generates the most revenue (${city_revenue.iloc[0]:,.2f})")

        monthly_trend = self.get_monthly_trend()
        if len(monthly_trend) > 0:
            best_month = monthly_trend.idxmax()
            insights.append(f"📅 **Best Month**: {best_month} is the highest revenue month")

        return insights