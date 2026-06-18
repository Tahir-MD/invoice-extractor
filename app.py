"""
Invoice Data Extractor - Professional Edition
Created by: Tahir Mahmood
Year: 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import sys
import os
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Professional Invoice Analyzer - Tahir Mahmood",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS - Professional Styling
# ============================================================
st.markdown("""
<style>
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .main-header h1 {
        font-size: 36px;
        margin: 0;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .main-header p {
        margin: 8px 0 0 0;
        opacity: 0.9;
        font-size: 16px;
    }
    .main-header .subtitle {
        font-size: 13px;
        opacity: 0.7;
        margin-top: 10px;
    }

    /* Professional Metric Cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 4px solid #1a1a2e;
        transition: all 0.3s;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #1a1a2e;
    }
    .metric-label {
        font-size: 13px;
        color: #666;
        margin-top: 5px;
        font-weight: 500;
    }
    .metric-delta {
        font-size: 12px;
        margin-top: 3px;
        font-weight: 500;
    }
    .metric-positive { color: #2ecc71; }
    .metric-negative { color: #e74c3c; }
    .metric-neutral { color: #f39c12; }

    /* Recommendation Cards */
    .rec-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin: 12px 0;
        border-left: 5px solid #1a1a2e;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s;
    }
    .rec-card:hover {
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transform: translateX(5px);
    }
    .rec-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }
    .rec-title {
        font-size: 16px;
        font-weight: 600;
        color: #1a1a2e;
    }
    .rec-icon {
        font-size: 22px;
        margin-right: 10px;
    }
    .rec-description {
        color: #444;
        font-size: 14px;
        margin: 10px 0 8px 0;
        line-height: 1.6;
        white-space: pre-line;
    }
    .rec-action {
        font-size: 13px;
        color: #0f3460;
        font-weight: 600;
        margin-top: 8px;
        padding: 8px 15px;
        background: #f0f4ff;
        border-radius: 8px;
        display: inline-block;
    }
    .rec-priority-high {
        border-left-color: #e74c3c;
    }
    .rec-priority-medium {
        border-left-color: #f39c12;
    }
    .rec-priority-low {
        border-left-color: #2ecc71;
    }
    
    /* Priority Badges */
    .priority-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
    }
    .priority-high {
        background: #fde8e8;
        color: #e74c3c;
    }
    .priority-medium {
        background: #fef3e2;
        color: #f39c12;
    }
    .priority-low {
        background: #e8f8ed;
        color: #2ecc71;
    }

    /* Category Tags */
    .category-tag {
        padding: 2px 10px;
        border-radius: 15px;
        font-size: 11px;
        font-weight: 500;
        background: #eef2f7;
        color: #555;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .main-header h1 { font-size: 24px; }
        .metric-value { font-size: 22px; }
        .stTabs [data-baseweb="tab"] {
            font-size: 12px;
            padding: 4px 8px;
        }
        .rec-title { font-size: 14px; }
        .rec-header { flex-direction: column; align-items: flex-start; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>📊 Professional Invoice Analyzer</h1>
    <p>Data-Driven Insights for Business Growth</p>
    <div class="subtitle">Created by Tahir Mahmood | © 2026 | v3.0</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []

# ============================================================
# RECOMMENDATION ENGINE
# ============================================================
def generate_business_recommendations(df):
    """
    Generate comprehensive business recommendations
    based on invoice data analysis
    """
    recommendations = []

    # Calculate key metrics
    total_revenue = df['amount'].sum()
    avg_invoice = df['amount'].mean()
    total_invoices = len(df)

    # ============================================================
    # 1. REVENUE & SALES OPTIMIZATION
    # ============================================================

    if 'email' in df.columns:
        revenue_per_customer = df.groupby('email')['amount'].sum()
        unique_customers = len(revenue_per_customer)
        avg_revenue_per_customer = revenue_per_customer.mean()
        top_customers = revenue_per_customer.nlargest(10)
        top_customer_share = top_customers.sum() / total_revenue * 100 if total_revenue > 0 else 0

        if top_customer_share > 50:
            recommendations.append({
                'category': '💰 Revenue Optimization',
                'title': 'High Customer Concentration Risk',
                'description': f'Top 10 customers contribute {top_customer_share:.1f}% of total revenue (${top_customers.sum():,.2f}). This creates dependency risk. Diversify your customer base through targeted acquisition campaigns.',
                'priority': 'high',
                'action': 'Implement customer acquisition strategy',
                'icon': '🎯'
            })
        else:
            recommendations.append({
                'category': '💰 Revenue Optimization',
                'title': 'Healthy Customer Distribution',
                'description': f'Revenue is well-distributed across {unique_customers} customers. Average revenue per customer is ${avg_revenue_per_customer:.2f}. Consider upselling to mid-tier customers to increase this metric.',
                'priority': 'medium',
                'action': 'Launch upsell campaigns',
                'icon': '📈'
            })

    # ============================================================
    # 2. PRODUCT PERFORMANCE
    # ============================================================

    if 'product_id' in df.columns:
        product_revenue = df.groupby('product_id')['amount'].sum()
        top_products = product_revenue.nlargest(5)
        bottom_products = product_revenue.nsmallest(5)
        top_product_share = top_products.sum() / total_revenue * 100 if total_revenue > 0 else 0
        unique_products = len(product_revenue)

        if len(top_products) > 0:
            recommendations.append({
                'category': '🏷️ Product Strategy',
                'title': 'Star Products Identification',
                'description': f'Top 5 products generate {top_product_share:.1f}% of revenue (${top_products.sum():,.2f}). These are your star performers. Increase inventory and marketing for these products.',
                'priority': 'high',
                'action': 'Invest in star products',
                'icon': '⭐'
            })

        if len(bottom_products) > 0 and bottom_products.sum() > 0:
            recommendations.append({
                'category': '🏷️ Product Strategy',
                'title': 'Underperforming Products Review',
                'description': f'Bottom 5 products generate only ${bottom_products.sum():.2f} in revenue. Consider discontinuation, rebranding, or bundle offers with top products.',
                'priority': 'medium',
                'action': 'Review underperforming products',
                'icon': '📉'
            })

        if unique_products >= 3:
            recommendations.append({
                'category': '🏷️ Product Strategy',
                'title': 'Product Bundling Opportunity',
                'description': f'With {unique_products} products in your portfolio, create strategic bundles combining popular products with complementary items. This can increase average order value by 15-30%.',
                'priority': 'medium',
                'action': 'Create product bundles',
                'icon': '📦'
            })

    # ============================================================
    # 3. CUSTOMER INSIGHTS
    # ============================================================

    if 'email' in df.columns:
        customer_spending = df.groupby('email')['amount'].sum()
        unique_customers = len(customer_spending)

        if unique_customers > 0:
            segments = pd.cut(
                customer_spending,
                bins=[0, 100, 500, 1000, float('inf')],
                labels=['Bronze (<$100)', 'Silver ($100-$500)',
                       'Gold ($500-$1000)', 'Platinum ($1000+)']
            )
            segment_counts = segments.value_counts()

            seg_text = []
            for seg, count in segment_counts.items():
                emoji = {'Bronze (<$100)': '🥉', 'Silver ($100-$500)': '🥈',
                        'Gold ($500-$1000)': '🥇', 'Platinum ($1000+)': '💎'}.get(seg, '📊')
                seg_text.append(f"{emoji} {seg}: {count} customers")

            recommendations.append({
                'category': '👥 Customer Segmentation',
                'title': 'Customer Value Distribution',
                'description': '\n'.join(seg_text) + f'\n\n**Action:** Create targeted marketing campaigns for each segment. Focus on moving Silver to Gold and Gold to Platinum.',
                'priority': 'high',
                'action': 'Implement segment-specific marketing',
                'icon': '👥'
            })

        # Loyalty program
        gold_platinum = segment_counts.get('Gold ($500-$1000)', 0) + segment_counts.get('Platinum ($1000+)', 0)
        if gold_platinum > 0:
            recommendations.append({
                'category': '👥 Customer Retention',
                'title': 'Loyalty Program Implementation',
                'description': f'You have {gold_platinum} high-value customers (Gold + Platinum). Implement a tiered loyalty program with exclusive benefits to retain these valuable customers.',
                'priority': 'high',
                'action': 'Launch loyalty program',
                'icon': '💎'
            })

        # Repeat customer analysis
        order_counts = df.groupby('email').size()
        repeat_customers = (order_counts > 1).sum()
        repeat_rate = repeat_customers / unique_customers * 100 if unique_customers > 0 else 0

        if repeat_rate < 30:
            recommendations.append({
                'category': '👥 Customer Retention',
                'title': 'Low Repeat Customer Rate',
                'description': f'Only {repeat_rate:.1f}% of customers are repeat buyers. Implement post-purchase email campaigns, subscription options, and referral programs.',
                'priority': 'high',
                'action': 'Improve customer retention',
                'icon': '🔄'
            })
        else:
            recommendations.append({
                'category': '👥 Customer Retention',
                'title': 'Good Customer Retention Rate',
                'description': f'{repeat_rate:.1f}% of customers return for repeat purchases. Continue nurturing these relationships with personalized offers.',
                'priority': 'low',
                'action': 'Maintain retention programs',
                'icon': '✅'
            })

    # ============================================================
    # 4. GEOGRAPHIC EXPANSION
    # ============================================================

    if 'city' in df.columns:
        city_revenue = df.groupby('city')['amount'].sum().sort_values(ascending=False)
        top_cities = city_revenue.head(5)
        top_city_share = top_cities.sum() / total_revenue * 100 if total_revenue > 0 else 0
        unique_cities = len(city_revenue)

        if len(top_cities) > 0:
            recommendations.append({
                'category': '📍 Geographic Strategy',
                'title': 'Top Performing Markets',
                'description': f'Top 5 cities generate {top_city_share:.1f}% of revenue (${top_cities.sum():,.2f}). Invest in local marketing and establish partnerships in these areas.',
                'priority': 'medium',
                'action': 'Expand in top cities',
                'icon': '🏙️'
            })

        if unique_cities > 0:
            recommendations.append({
                'category': '📍 Geographic Strategy',
                'title': 'Market Expansion Opportunities',
                'description': f'You currently operate in {unique_cities} cities. Consider expanding to cities with similar demographics to your top performers.',
                'priority': 'medium',
                'action': 'Explore new markets',
                'icon': '🌍'
            })

    # ============================================================
    # 5. SEASONAL & TIME-BASED INSIGHTS
    # ============================================================

    if 'invoice_date' in df.columns:
        df_copy = df.copy()
        df_copy['month'] = df_copy['invoice_date'].dt.month
        df_copy['quarter'] = df_copy['invoice_date'].dt.quarter
        df_copy['day_of_week'] = df_copy['invoice_date'].dt.day_name()

        # Monthly analysis
        monthly_revenue = df_copy.groupby('month')['amount'].sum()
        if len(monthly_revenue) > 0:
            best_month = monthly_revenue.idxmax()
            best_month_revenue = monthly_revenue.max()
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            recommendations.append({
                'category': '📅 Seasonal Planning',
                'title': 'Peak Season Identified',
                'description': f'**{month_names[best_month-1]}** is your peak month with ${best_month_revenue:,.2f} in revenue. Plan inventory, staffing, and marketing campaigns around this period.',
                'priority': 'high',
                'action': 'Prepare for peak season',
                'icon': '📊'
            })

        # Day of week analysis
        daily_revenue = df_copy.groupby('day_of_week')['amount'].mean()
        if len(daily_revenue) > 0:
            best_day = daily_revenue.idxmax()
            best_day_revenue = daily_revenue.max()

            recommendations.append({
                'category': '📅 Seasonal Planning',
                'title': 'Optimal Sales Day',
                'description': f'**{best_day}** has the highest average revenue (${best_day_revenue:.2f}). Consider running targeted promotions on this day.',
                'priority': 'medium',
                'action': 'Optimize for best days',
                'icon': '📆'
            })

        # Quarterly analysis
        quarterly_revenue = df_copy.groupby('quarter')['amount'].sum()
        if len(quarterly_revenue) > 0:
            best_quarter = quarterly_revenue.idxmax()
            best_quarter_revenue = quarterly_revenue.max()

            recommendations.append({
                'category': '📅 Seasonal Planning',
                'title': 'Quarterly Performance',
                'description': f'Q{best_quarter} is your strongest quarter with ${best_quarter_revenue:,.2f} in revenue. Plan major initiatives around this period.',
                'priority': 'medium',
                'action': 'Align strategy with quarterly trends',
                'icon': '📈'
            })

    # ============================================================
    # 6. PRICING & MARGIN OPTIMIZATION
    # ============================================================

    if 'amount' in df.columns and 'qty' in df.columns:
        df_copy = df.copy()
        df_copy['unit_price'] = df_copy['amount'] / df_copy['qty']
        avg_unit_price = df_copy['unit_price'].mean()
        min_unit_price = df_copy['unit_price'].min()
        max_unit_price = df_copy['unit_price'].max()
        std_unit_price = df_copy['unit_price'].std()

        recommendations.append({
            'category': '💲 Pricing Strategy',
            'title': 'Price Range Analysis',
            'description': f'''
**Pricing Overview:**
- Average Unit Price: ${avg_unit_price:.2f}
- Price Range: ${min_unit_price:.2f} - ${max_unit_price:.2f}
- Standard Deviation: ${std_unit_price:.2f}

**Recommendation:** Products at the lower price range may have room for increase. Test premium pricing for top-performing products.
            ''',
            'priority': 'medium',
            'action': 'Optimize pricing strategy',
            'icon': '💲'
        })

    # ============================================================
    # 7. OPERATIONAL EFFICIENCY
    # ============================================================

    if 'qty' in df.columns:
        avg_qty = df['qty'].mean()
        max_qty = df['qty'].max()

        recommendations.append({
            'category': '⚙️ Operational Efficiency',
            'title': 'Order Size Optimization',
            'description': f'Average order quantity is {avg_qty:.1f} units (max: {max_qty}). Encourage larger orders through free shipping thresholds and volume discounts.',
            'priority': 'low',
            'action': 'Optimize order sizes',
            'icon': '📦'
        })

    # ============================================================
    # 8. DIGITAL MARKETING
    # ============================================================

    if 'email' in df.columns:
        unique_customers = df['email'].nunique()

        recommendations.append({
            'category': '📢 Digital Marketing',
            'title': 'Email Marketing Strategy',
            'description': f'You have {unique_customers} customer emails. Create a segmented email marketing strategy with personalized product recommendations.',
            'priority': 'medium',
            'action': 'Launch email campaigns',
            'icon': '📧'
        })

    # ============================================================
    # 9. CUSTOMER SERVICE
    # ============================================================

    if 'amount' in df.columns:
        small_orders = df[df['amount'] < df['amount'].quantile(0.1)]
        if len(small_orders) > 0:
            recommendations.append({
                'category': '🛠️ Customer Service',
                'title': 'Small Order Analysis',
                'description': f'{len(small_orders)} orders ({len(small_orders)/len(df)*100:.1f}%) are below the 10th percentile. Consider free shipping thresholds or minimum order values.',
                'priority': 'medium',
                'action': 'Optimize small orders',
                'icon': '🛍️'
            })

    # ============================================================
    # 10. INVENTORY & SUPPLY CHAIN
    # ============================================================

    if 'product_id' in df.columns and 'qty' in df.columns:
        top_products_qty = df.groupby('product_id')['qty'].sum().nlargest(5)

        if len(top_products_qty) > 0:
            recommendations.append({
                'category': '📦 Inventory Management',
                'title': 'Inventory Planning',
                'description': f'Maintain optimal stock levels for top-selling products. Implement demand forecasting to prevent stockouts and overstock.',
                'priority': 'high',
                'action': 'Optimize inventory levels',
                'icon': '📦'
            })

    # ============================================================
    # 11. FINANCIAL INSIGHTS
    # ============================================================

    if 'amount' in df.columns:
        recommendations.append({
            'category': '💰 Financial Insights',
            'title': 'Revenue Growth Strategy',
            'description': f'Current revenue: ${total_revenue:,.2f} from {total_invoices} transactions. Average invoice: ${avg_invoice:.2f}. Focus on increasing average order value.',
            'priority': 'medium',
            'action': 'Implement growth strategies',
            'icon': '📊'
        })

    # ============================================================
    # 12. COMPETITIVE ADVANTAGE
    # ============================================================

    if 'email' in df.columns:
        unique_customers = df['email'].nunique()
        avg_transactions_per_customer = total_invoices / unique_customers if unique_customers > 0 else 0

        recommendations.append({
            'category': '🏆 Competitive Advantage',
            'title': 'Customer Experience Enhancement',
            'description': f'With {unique_customers} customers averaging {avg_transactions_per_customer:.1f} transactions each, focus on enhancing customer experience through personalization and faster delivery.',
            'priority': 'low',
            'action': 'Improve customer experience',
            'icon': '🏆'
        })

    return recommendations

# ============================================================
# SIDEBAR - Complete Updated Version
# ============================================================
with st.sidebar:
    st.markdown("### 📁 Data Source")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your invoice data file"
    )

    if uploaded_file is not None:
        try:
            # ---------- LOAD FILE ----------
            if uploaded_file.name.endswith('.csv'):
                try:
                    # Read with low_memory=False to handle mixed types
                    df = pd.read_csv(uploaded_file, low_memory=False)
                except pd.errors.ParserError:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, on_bad_lines='skip', low_memory=False)
                except Exception:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, engine='python', low_memory=False)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl')

            # ---------- CLEAN DATA ----------

            # Clean column names
            df.columns = df.columns.str.strip()

            # Convert 'amount' to numeric
            if 'amount' in df.columns:
                df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
                df['amount'] = df['amount'].replace([np.inf, -np.inf], np.nan)
                df = df.dropna(subset=['amount'])
            else:
                st.error("❌ No 'amount' column found! Please check your file format.")
                st.stop()

            # Convert 'qty' to numeric
            if 'qty' in df.columns:
                df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
                df['qty'] = df['qty'].fillna(0).astype(int)

            # Convert 'invoice_date' to datetime
            if 'invoice_date' in df.columns:
                df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
                df = df.dropna(subset=['invoice_date'])
            else:
                # Create dummy date if not exists
                df['invoice_date'] = pd.Timestamp.now()
                st.warning("⚠️ No 'invoice_date' column found. Using current date.")

            # Convert all other columns to string
            for col in df.columns:
                if col not in ['amount', 'qty', 'invoice_date']:
                    try:
                        df[col] = df[col].astype(str)
                    except:
                        pass

            # Create customer name if not exists
            if 'customer_name' not in df.columns:
                if 'first_name' in df.columns and 'last_name' in df.columns:
                    df['customer_name'] = df['first_name'].astype(str) + ' ' + df['last_name'].astype(str)
                elif 'name' in df.columns:
                    df['customer_name'] = df['name'].astype(str)
                elif 'email' in df.columns:
                    df['customer_name'] = df['email'].astype(str)
                else:
                    df['customer_name'] = df.index.astype(str)
                    st.warning("⚠️ No customer name column found. Using row numbers.")

            # Check if any data remains
            if len(df) == 0:
                st.error("❌ No valid data found after cleaning. Please check your file format.")
                st.stop()

            # ---------- STORE IN SESSION ----------
            st.session_state.df = df
            st.session_state.filtered_df = df
            st.session_state.data_loaded = True

            # Generate recommendations
            st.session_state.recommendations = generate_business_recommendations(df)

            st.success(f"✅ Loaded {len(df)} invoices")

            st.info(f"""
            📄 **File Info:**
            - Name: {uploaded_file.name}
            - Rows: {len(df):,}
            - Columns: {len(df.columns)}
            - Total Revenue: ${df['amount'].sum():,.2f}
            """)

        except Exception as e:
            st.error(f"Error loading file: {e}")
            import traceback
            st.code(traceback.format_exc())
            st.session_state.data_loaded = False

    st.markdown("---")

    # ---------- SAMPLE DATA ----------
    if st.button("📝 Load Sample Data", use_container_width=True):
        sample_path = 'data/sample_invoices.csv'
        if os.path.exists(sample_path):
            try:
                df = pd.read_csv(sample_path, low_memory=False)

                # Clean sample data
                if 'amount' in df.columns:
                    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
                    df = df.dropna(subset=['amount'])

                if 'invoice_date' in df.columns:
                    df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
                    df = df.dropna(subset=['invoice_date'])

                if 'qty' in df.columns:
                    df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
                    df['qty'] = df['qty'].fillna(0).astype(int)

                if 'customer_name' not in df.columns:
                    if 'first_name' in df.columns and 'last_name' in df.columns:
                        df['customer_name'] = df['first_name'] + ' ' + df['last_name']
                    else:
                        df['customer_name'] = df.index.astype(str)

                st.session_state.df = df
                st.session_state.filtered_df = df
                st.session_state.data_loaded = True
                st.session_state.recommendations = generate_business_recommendations(df)
                st.success(f"✅ Sample data loaded! ({len(df)} invoices)")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading sample data: {e}")
        else:
            st.error("Sample data file not found!")

    st.markdown("---")

    # ---------- QUICK STATS ----------
    if st.session_state.data_loaded and st.session_state.df is not None:
        df = st.session_state.df
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Revenue", f"${df['amount'].sum():,.2f}")
        st.metric("Total Invoices", len(df))

        if 'email' in df.columns:
            st.metric("Unique Customers", df['email'].nunique())

        if 'product_id' in df.columns:
            st.metric("Unique Products", df['product_id'].nunique())

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 11px; color: #999; text-align: center;">
        <b>Professional Invoice Analyzer</b><br>
        Built with ❤️ by Tahir Mahmood
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FILTERS
# ============================================================
if st.session_state.data_loaded and st.session_state.df is not None:
    df = st.session_state.df

    # Date filter
    if 'invoice_date' in df.columns and len(df) > 0:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔍 Filters")

        min_date = df['invoice_date'].min()
        max_date = df['invoice_date'].max()

        if pd.notnull(min_date) and pd.notnull(max_date):
            try:
                date_range = st.sidebar.date_input(
                    "Date Range",
                    value=[min_date.date(), max_date.date()],
                    min_value=min_date.date(),
                    max_value=max_date.date()
                )

                if len(date_range) == 2:
                    mask = (df['invoice_date'].dt.date >= date_range[0]) & \
                           (df['invoice_date'].dt.date <= date_range[1])
                    st.session_state.filtered_df = df[mask]
            except:
                pass

    # Amount filter
    if 'amount' in df.columns and len(df) > 0:
        try:
            min_amount = float(df['amount'].min())
            max_amount = float(df['amount'].max())

            if min_amount < max_amount:
                amount_range = st.sidebar.slider(
                    "Amount Range ($)",
                    min_value=min_amount,
                    max_value=max_amount,
                    value=(min_amount, max_amount)
                )

                filtered_df = st.session_state.filtered_df if st.session_state.filtered_df is not None else df
                filtered_df = filtered_df[
                    (filtered_df['amount'] >= amount_range[0]) &
                    (filtered_df['amount'] <= amount_range[1])
                ]
                st.session_state.filtered_df = filtered_df
        except:
            pass

# ============================================================
# MAIN CONTENT
# ============================================================
if st.session_state.data_loaded and st.session_state.df is not None:
    df = st.session_state.filtered_df if st.session_state.filtered_df is not None else st.session_state.df

    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Dashboard", "📋 Data Explorer", "📊 Analytics",
        "💡 Recommendations", "📥 Export"
    ])

    # ============================================================
    # TAB 1: DASHBOARD
    # ============================================================
    with tab1:
        st.header("Key Performance Indicators")

        # Metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_revenue = df['amount'].sum() if 'amount' in df.columns else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">${total_revenue:,.2f}</div>
                <div class="metric-label">💰 Total Revenue</div>
                <div class="metric-delta">{len(df)} invoices</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            avg_invoice = df['amount'].mean() if 'amount' in df.columns else 0
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #2ecc71;">
                <div class="metric-value">${avg_invoice:,.2f}</div>
                <div class="metric-label">📊 Average Invoice</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            unique_customers = df['email'].nunique() if 'email' in df.columns else len(df)
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #f39c12;">
                <div class="metric-value">{unique_customers:,}</div>
                <div class="metric-label">👥 Unique Customers</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            total_quantity = df['qty'].sum() if 'qty' in df.columns else 0
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: #9b59b6;">
                <div class="metric-value">{total_quantity:,}</div>
                <div class="metric-label">📦 Total Items Sold</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Charts row 1
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏆 Top Products by Revenue")
            if 'product_id' in df.columns:
                try:
                    product_revenue = df.groupby('product_id')['amount'].sum().sort_values(ascending=False).head(10)
                    if len(product_revenue) > 0:
                        fig = px.bar(
                            x=product_revenue.values,
                            y=product_revenue.index.astype(str),
                            orientation='h',
                            title='Top 10 Products',
                            labels={'x': 'Revenue ($)', 'y': 'Product ID'},
                            color=product_revenue.values,
                            color_continuous_scale=['#1a1a2e', '#0f3460', '#667eea'],
                            text=product_revenue.values
                        )
                        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
                        fig.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No product data available")
                except:
                    st.info("No product data available")
            else:
                st.info("No product data available")

        with col2:
            st.subheader("📍 Revenue by City")
            if 'city' in df.columns:
                try:
                    city_revenue = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
                    if len(city_revenue) > 0:
                        fig = px.pie(
                            values=city_revenue.values,
                            names=city_revenue.index,
                            title='Top 10 Cities',
                            color_discrete_sequence=px.colors.qualitative.Set3,
                            hole=0.3
                        )
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No city data available")
                except:
                    st.info("No city data available")
            else:
                st.info("No city data available")

        # Charts row 2
        st.subheader("📈 Revenue Trends")

        col1, col2 = st.columns(2)

        with col1:
            if 'invoice_date' in df.columns and len(df) > 0:
                try:
                    df['invoice_date'] = pd.to_datetime(df['invoice_date'])
                    daily_revenue = df.groupby(df['invoice_date'].dt.date)['amount'].sum().reset_index()
                    daily_revenue.columns = ['Date', 'Revenue']

                    if len(daily_revenue) > 1:
                        fig = px.line(
                            daily_revenue,
                            x='Date',
                            y='Revenue',
                            title='Daily Revenue Trend',
                            markers=True,
                            line_shape='spline'
                        )
                        fig.update_layout(height=400, xaxis_title='Date', yaxis_title='Revenue ($)')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Not enough data for trend analysis")
                except:
                    st.info("Date data not available")

        with col2:
            if 'job' in df.columns and len(df) > 0:
                try:
                    job_revenue = df.groupby('job')['amount'].sum().sort_values(ascending=False).head(10)
                    if len(job_revenue) > 0:
                        fig = px.bar(
                            x=job_revenue.values,
                            y=job_revenue.index,
                            orientation='h',
                            title='Revenue by Profession',
                            labels={'x': 'Revenue ($)', 'y': 'Profession'},
                            color=job_revenue.values,
                            color_continuous_scale=['#2ca02c', '#1a1a2e']
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No profession data available")
                except:
                    st.info("No profession data available")

    # ============================================================
    # TAB 2: DATA EXPLORER
    # ============================================================
    with tab2:
        st.header("Invoice Data Explorer")

        # Search box
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            search_term = st.text_input("🔍 Search in all columns", placeholder="Type to filter...")

        with search_col2:
            st.write("")
            st.write("")
            show_all = st.checkbox("Show all columns", value=False)

        # Filter data
        if search_term:
            try:
                mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                display_df = df[mask]
                st.info(f"Found {len(display_df)} matching records")
            except:
                display_df = df
                st.info("Search not available for this data")
        else:
            display_df = df

        # Select columns to display
        if not show_all:
            important_cols = ['customer_name', 'email', 'amount', 'invoice_date',
                             'product_id', 'qty', 'city', 'job']
            available_cols = [col for col in important_cols if col in display_df.columns]
            if available_cols:
                display_df = display_df[available_cols]

        # Display dataframe
        st.dataframe(display_df, use_container_width=True, height=500)

    # ============================================================
    # TAB 3: ANALYTICS
    # ============================================================
    with tab3:
        st.header("Advanced Analytics")

        if 'amount' in df.columns and len(df) > 0:
            # Revenue Distribution
            st.subheader("💰 Revenue Distribution")
            try:
                fig = px.histogram(
                    df,
                    x='amount',
                    nbins=min(50, len(df)),
                    title='Invoice Amount Distribution',
                    labels={'amount': 'Invoice Amount ($)', 'count': 'Number of Invoices'},
                    color_discrete_sequence=['#1a1a2e']
                )
                fig.add_vline(x=df['amount'].mean(), line_dash="dash", line_color="#e74c3c",
                             annotation_text=f"Mean: ${df['amount'].mean():.2f}")
                fig.add_vline(x=df['amount'].median(), line_dash="dash", line_color="#2ecc71",
                             annotation_text=f"Median: ${df['amount'].median():.2f}")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("Revenue distribution not available")

        # Customer Analytics
        if 'email' in df.columns and 'customer_name' in df.columns and len(df) > 0:
            st.subheader("👥 Customer Analytics")
            col1, col2 = st.columns(2)

            with col1:
                # Top 10 Customers
                try:
                    customer_spending = df.groupby('customer_name')['amount'].sum().sort_values(ascending=False).head(10)
                    if len(customer_spending) > 0:
                        fig = px.bar(
                            x=customer_spending.values,
                            y=customer_spending.index,
                            orientation='h',
                            title='Top 10 Customers by Spending',
                            labels={'x': 'Amount ($)', 'y': 'Customer'},
                            color=customer_spending.values,
                            color_continuous_scale=['#1a1a2e', '#667eea']
                        )
                        fig.update_layout(height=350)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No customer data available")
                except:
                    st.info("Customer data not available")

            with col2:
                # Customer Order Frequency
                try:
                    order_freq = df.groupby('customer_name').size().sort_values(ascending=False).head(10)
                    if len(order_freq) > 0:
                        fig = px.bar(
                            x=order_freq.values,
                            y=order_freq.index,
                            orientation='h',
                            title='Most Active Customers',
                            labels={'x': 'Number of Orders', 'y': 'Customer'},
                            color=order_freq.values,
                            color_continuous_scale=['#1a1a2e', '#f39c12']
                        )
                        fig.update_layout(height=350)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No customer data available")
                except:
                    st.info("Customer data not available")

        # Missing values
        st.subheader("🔍 Data Quality Analysis")
        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0]

        if len(missing_data) > 0:
            missing_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing Count': missing_data.values,
                'Missing Percentage': (missing_data.values / len(df) * 100).round(2)
            })
            st.dataframe(missing_df, use_container_width=True)

            # Plot missing values
            try:
                fig = px.bar(
                    missing_df,
                    x='Column',
                    y='Missing Percentage',
                    title='Missing Values by Column',
                    color='Missing Percentage',
                    color_continuous_scale=['#2ecc71', '#f39c12', '#e74c3c']
                )
                st.plotly_chart(fig, use_container_width=True)
            except:
                pass
        else:
            st.success("✅ No missing values found in the dataset!")

    # ============================================================
    # TAB 4: RECOMMENDATIONS
    # ============================================================
    with tab4:
        st.header("💡 Professional Business Recommendations")
        st.markdown("*Data-driven insights to optimize your business performance*")

        if st.session_state.recommendations:
            # Filter options
            col1, col2 = st.columns(2)

            with col1:
                priority_filter = st.selectbox(
                    "Filter by Priority",
                    ["All", "High Priority", "Medium Priority", "Low Priority"]
                )

            with col2:
                categories = list(set([r['category'] for r in st.session_state.recommendations]))
                category_filter = st.selectbox(
                    "Filter by Category",
                    ["All"] + categories
                )

            # Filter recommendations
            filtered_recs = st.session_state.recommendations
            if priority_filter != "All":
                priority_map = {
                    "High Priority": "high",
                    "Medium Priority": "medium",
                    "Low Priority": "low"
                }
                filtered_recs = [r for r in filtered_recs if r['priority'] == priority_map[priority_filter]]

            if category_filter != "All":
                filtered_recs = [r for r in filtered_recs if r['category'] == category_filter]

            # Display recommendations
            if filtered_recs:
                # Summary stats
                high_count = len([r for r in filtered_recs if r['priority'] == 'high'])
                medium_count = len([r for r in filtered_recs if r['priority'] == 'medium'])
                low_count = len([r for r in filtered_recs if r['priority'] == 'low'])

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🔴 High Priority", high_count, delta="Urgent")
                with col2:
                    st.metric("🟡 Medium Priority", medium_count, delta="Important")
                with col3:
                    st.metric("🟢 Low Priority", low_count, delta="Nice to have")

                st.markdown("---")

                for rec in filtered_recs:
                    priority_class = "rec-priority-" + rec['priority']
                    priority_label = {"high": "High", "medium": "Medium", "low": "Low"}[rec['priority']]
                    priority_badge = {"high": "priority-high", "medium": "priority-medium", "low": "priority-low"}[rec['priority']]

                    st.markdown(f"""
                    <div class="rec-card {priority_class}">
                        <div class="rec-header">
                            <div>
                                <span class="rec-icon">{rec['icon']}</span>
                                <span class="rec-title">{rec['title']}</span>
                            </div>
                            <div>
                                <span class="priority-badge {priority_badge}">{priority_label}</span>
                                <span class="category-tag" style="margin-left: 8px;">{rec['category']}</span>
                            </div>
                        </div>
                        <div class="rec-description">{rec['description']}</div>
                        <div class="rec-action">🎯 {rec['action']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No recommendations match your filters")
        else:
            st.info("No recommendations available. Please upload data first.")

        # Export recommendations
        if st.session_state.recommendations:
            st.markdown("---")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("📥 Export Recommendations as CSV", use_container_width=True):
                    rec_df = pd.DataFrame(st.session_state.recommendations)
                    csv = rec_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Recommendations",
                        data=csv,
                        file_name=f'recommendations_{datetime.now().strftime("%Y%m%d")}.csv',
                        mime='text/csv'
                    )

    # ============================================================
    # TAB 5: EXPORT
    # ============================================================
    with tab5:
        st.header("📥 Export Results")

        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 15px 0;">
            <h4 style="margin: 0;">📋 Export Options</h4>
            <p style="color: #666; margin: 5px 0 0 0;">Download your analysis results in various formats</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            # Full Data CSV
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Full Data (CSV)",
                data=csv_data,
                file_name=f'invoice_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv',
                use_container_width=True
            )

        with col2:
            # Full Data Excel
            try:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Invoices', index=False)

                    # Summary Sheet
                    summary = pd.DataFrame({
                        'Metric': ['Total Revenue', 'Average Invoice', 'Total Invoices', 'Unique Customers'],
                        'Value': [
                            f"${df['amount'].sum():,.2f}",
                            f"${df['amount'].mean():,.2f}",
                            len(df),
                            df['email'].nunique() if 'email' in df.columns else len(df)
                        ]
                    })
                    summary.to_excel(writer, sheet_name='Summary', index=False)

                    # Recommendations Sheet
                    if st.session_state.recommendations:
                        rec_df = pd.DataFrame(st.session_state.recommendations)
                        rec_df.to_excel(writer, sheet_name='Recommendations', index=False)
                excel_data = output.getvalue()
                st.download_button(
                    label="📥 Full Data (Excel)",
                    data=excel_data,
                    file_name=f'invoice_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    use_container_width=True
                )
            except Exception as e:
                st.warning("Excel export requires openpyxl")

        # Recommendations Only
        if st.session_state.recommendations:
            st.markdown("---")
            st.subheader("📥 Export Recommendations")

            rec_df = pd.DataFrame(st.session_state.recommendations)
            rec_csv = rec_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Recommendations (CSV)",
                data=rec_csv,
                file_name=f'recommendations_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv',
                use_container_width=True
            )

else:
    # Welcome Screen
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ## 📊 Welcome to Professional Invoice Analyzer
        
        ### Get started by uploading your invoice data
        
        **What you can do:**
        - 📈 **Analyze** revenue trends and patterns
        - 🏷️ **Track** product and customer performance
        - 💡 **Get** AI-powered business recommendations
        - 📊 **Visualize** data with interactive charts
        - 📥 **Export** professional reports
        
        ### How it works:
        1. Upload your CSV/Excel file
        2. Explore interactive dashboard
        3. Get actionable recommendations
        4. Download professional reports
        """)

    with col2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08);">
            <h4>🚀 Key Features</h4>
            <ul style="list-style: none; padding: 0;">
                <li>✅ <b>Revenue Analytics</b><br>Track sales performance</li>
                <li>✅ <b>Product Insights</b><br>Best and worst performers</li>
                <li>✅ <b>Customer Analysis</b><br>Segmentation & retention</li>
                <li>✅ <b>Smart Recommendations</b><br>AI-powered insights</li>
                <li>✅ <b>Professional Reports</b><br>Export to CSV/Excel</li>
            </ul>
            <div style="margin-top: 15px; padding: 10px; background: #f0f4ff; border-radius: 8px; text-align: center;">
                <span style="font-size: 12px; color: #1a1a2e;">Created by Tahir Mahmood © 2026</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 12px; padding: 20px 0;">
    <b>Professional Invoice Analyzer v3.0</b> | Created by Tahir Mahmood | © 2026
    <br>Built with ❤️ using Streamlit, Python & Data Science
</div>
""", unsafe_allow_html=True)