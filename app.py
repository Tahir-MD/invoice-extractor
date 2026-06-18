"""
Invoice Data Extractor - Main Application
A complete invoice analysis tool with Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import sys
import os

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="Invoice Data Extractor - Tahir Mahmood",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 12px;
            padding: 4px 8px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 Invoice Data Extractor & Analyzer</h1>
    <p>Upload CSV/Excel and get instant business insights</p>
    <p style="font-size: 14px;">Created by Tahir Mahmood | © 2026</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("📁 Data Source")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your invoice data file"
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                try:
                    df = pd.read_csv(uploaded_file)
                except pd.errors.ParserError:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, on_bad_lines='skip')
                except Exception:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, engine='python')
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl')

            # ============================================================
            # ⭐ FIX: Ensure amount is numeric
            # ============================================================
            if 'amount' in df.columns:
                df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
                df = df.dropna(subset=['amount'])

            # Convert date columns
            if 'invoice_date' in df.columns:
                df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')

            st.session_state.df = df
            st.session_state.filtered_df = df
            st.session_state.data_loaded = True
            st.success(f"✅ Loaded {len(df)} invoices")

            st.info(f"""
            📄 **File Info:**
            - Name: {uploaded_file.name}
            - Rows: {len(df):,}
            - Columns: {len(df.columns)}
            """)

        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.session_state.data_loaded = False

    st.markdown("---")

    # Sample data button
    if st.button("📝 Load Sample Data", use_container_width=True):
        sample_path = 'data/sample_invoices.csv'
        if os.path.exists(sample_path):
            try:
                df = pd.read_csv(sample_path)

                # Ensure amount is numeric
                if 'amount' in df.columns:
                    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
                    df = df.dropna(subset=['amount'])

                if 'invoice_date' in df.columns:
                    df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')

                st.session_state.df = df
                st.session_state.filtered_df = df
                st.session_state.data_loaded = True
                st.success("✅ Sample data loaded!")
                st.rerun()
            except Exception as e:
                st.error(f"Error loading sample data: {e}")
        else:
            st.error("Sample data file not found!")

    # ============================================================
    # FILTERS (Only if data loaded)
    # ============================================================
    if st.session_state.data_loaded and st.session_state.df is not None:
        st.markdown("---")
        st.header("🔍 Filters")

        df = st.session_state.df

        # Date filter
        if 'invoice_date' in df.columns:
            df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
            min_date = df['invoice_date'].min()
            max_date = df['invoice_date'].max()

            if pd.notnull(min_date) and pd.notnull(max_date):
                date_range = st.date_input(
                    "Date Range",
                    value=[min_date.date(), max_date.date()],
                    min_value=min_date.date(),
                    max_value=max_date.date()
                )

                if len(date_range) == 2:
                    mask = (df['invoice_date'].dt.date >= date_range[0]) & \
                           (df['invoice_date'].dt.date <= date_range[1])
                    filtered_df = df[mask]
                    st.session_state.filtered_df = filtered_df
                    st.info(f"Showing {len(filtered_df)} records")

        # ============================================================
        # ⭐ FIXED: Amount filter with proper numeric handling
        # ============================================================
        if 'amount' in df.columns:
            # Ensure amount is numeric (already done, but double-check)
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            df = df.dropna(subset=['amount'])

            min_amount = float(df['amount'].min())
            max_amount = float(df['amount'].max())

            amount_range = st.slider(
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

# ============================================================
# MAIN CONTENT
# ============================================================
if st.session_state.data_loaded and st.session_state.df is not None:
    df = st.session_state.filtered_df if st.session_state.filtered_df is not None else st.session_state.df

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Dashboard", "📋 Data Explorer", "📊 Statistics", "💡 Insights"
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
            st.metric(
                label="💰 Total Revenue",
                value=f"${total_revenue:,.2f}",
                delta=f"{len(df)} invoices"
            )

        with col2:
            avg_invoice = df['amount'].mean() if 'amount' in df.columns else 0
            st.metric(
                label="📊 Average Invoice",
                value=f"${avg_invoice:,.2f}"
            )

        with col3:
            unique_customers = df['email'].nunique() if 'email' in df.columns else len(df)
            st.metric(
                label="👥 Unique Customers",
                value=f"{unique_customers:,}"
            )

        with col4:
            total_quantity = df['qty'].sum() if 'qty' in df.columns else 0
            st.metric(
                label="📦 Total Items Sold",
                value=f"{total_quantity:,}"
            )

        st.markdown("---")

        # Charts row 1
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏆 Top Products by Revenue")
            if 'product_id' in df.columns:
                product_revenue = df.groupby('product_id')['amount'].sum().sort_values(ascending=False).head(10)
                fig = px.bar(
                    x=product_revenue.values,
                    y=product_revenue.index.astype(str),
                    orientation='h',
                    title='Top 10 Products',
                    labels={'x': 'Revenue ($)', 'y': 'Product ID'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig.update_layout(height=400, margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No product data available")

        with col2:
            st.subheader("📍 Revenue by City")
            if 'city' in df.columns:
                city_revenue = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
                fig = px.pie(
                    values=city_revenue.values,
                    names=city_revenue.index,
                    title='Top 10 Cities',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No city data available")

        # Charts row 2
        st.subheader("📈 Revenue Trends")

        col1, col2 = st.columns(2)

        with col1:
            if 'invoice_date' in df.columns:
                df['invoice_date'] = pd.to_datetime(df['invoice_date'])
                daily_revenue = df.groupby(df['invoice_date'].dt.date)['amount'].sum().reset_index()
                daily_revenue.columns = ['Date', 'Revenue']

                fig = px.line(
                    daily_revenue,
                    x='Date',
                    y='Revenue',
                    title='Daily Revenue Trend',
                    markers=True
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if 'job' in df.columns:
                job_revenue = df.groupby('job')['amount'].sum().sort_values(ascending=False).head(10)
                fig = px.bar(
                    x=job_revenue.values,
                    y=job_revenue.index,
                    orientation='h',
                    title='Revenue by Profession',
                    labels={'x': 'Revenue ($)', 'y': 'Profession'},
                    color_discrete_sequence=['#2ca02c']
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

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
            mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
            display_df = df[mask]
            st.info(f"Found {len(display_df)} matching records")
        else:
            display_df = df

        # Select columns to display
        if not show_all:
            important_cols = ['first_name', 'last_name', 'email', 'amount', 'invoice_date',
                              'product_id', 'qty', 'city', 'job']
            available_cols = [col for col in important_cols if col in display_df.columns]
            display_df = display_df[available_cols]

        # Display dataframe
        st.dataframe(display_df, use_container_width=True, height=500)

        # Export options
        st.markdown("---")
        st.subheader("📥 Export Data")

        col1, col2 = st.columns(2)

        with col1:
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name=f'invoice_data_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv',
                use_container_width=True
            )

        with col2:
            try:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Invoices', index=False)
                    # Add summary sheet
                    if 'amount' in df.columns:
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
                excel_data = output.getvalue()
                st.download_button(
                    label="📥 Download as Excel",
                    data=excel_data,
                    file_name=f'invoice_data_{datetime.now().strftime("%Y%m%d")}.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    use_container_width=True
                )
            except Exception as e:
                st.warning("Excel export not available")

    # ============================================================
    # TAB 3: STATISTICS
    # ============================================================
    with tab3:
        st.header("Statistical Analysis")

        if 'amount' in df.columns:
            # Summary statistics
            st.subheader("📊 Descriptive Statistics")
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)

            # Revenue distribution
            st.subheader("💰 Revenue Distribution")
            fig = px.histogram(
                df,
                x='amount',
                nbins=50,
                title='Invoice Amount Distribution',
                labels={'amount': 'Invoice Amount ($)', 'count': 'Number of Invoices'},
                color_discrete_sequence=['#1f77b4']
            )
            fig.add_vline(x=df['amount'].mean(), line_dash="dash", line_color="red",
                          annotation_text=f"Mean: ${df['amount'].mean():.2f}")
            fig.add_vline(x=df['amount'].median(), line_dash="dash", line_color="green",
                          annotation_text=f"Median: ${df['amount'].median():.2f}")
            st.plotly_chart(fig, use_container_width=True)

        # Missing values
        st.subheader("🔍 Missing Values Analysis")
        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0]

        if len(missing_data) > 0:
            missing_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing Count': missing_data.values,
                'Missing Percentage': (missing_data.values / len(df) * 100).round(2)
            })
            st.dataframe(missing_df, use_container_width=True)
        else:
            st.success("✅ No missing values found in the dataset!")

    # ============================================================
    # TAB 4: INSIGHTS
    # ============================================================
    with tab4:
        st.header("Business Insights")

        if 'amount' in df.columns:
            total_revenue = df['amount'].sum()
            avg_invoice = df['amount'].mean()
            total_invoices = len(df)
            unique_customers = df['email'].nunique() if 'email' in df.columns else len(df)

            insights = [
                f"💰 **Total Revenue**: ${total_revenue:,.2f} from {total_invoices:,} invoices",
                f"📊 **Average Invoice**: ${avg_invoice:.2f}",
                f"👥 **Customer Base**: {unique_customers:,} unique customers"
            ]

            if 'product_id' in df.columns:
                top_product = df.groupby('product_id')['amount'].sum().idxmax()
                top_revenue = df.groupby('product_id')['amount'].sum().max()
                insights.append(f"🏆 **Best Product**: Product {top_product} generates ${top_revenue:,.2f}")

            if 'city' in df.columns:
                top_city = df.groupby('city')['amount'].sum().idxmax()
                top_city_revenue = df.groupby('city')['amount'].sum().max()
                insights.append(f"📍 **Top Market**: {top_city} generates ${top_city_revenue:,.2f}")

            st.success("📌 Key Insights:")
            for insight in insights:
                st.markdown(f"- {insight}")

        st.markdown("---")

        # Recommendations
        st.subheader("💡 Recommendations")
        recommendations = [
            "📌 **Focus on top products**: Invest marketing budget in best-selling items",
            "📌 **Customer retention**: Implement loyalty programs for repeat customers",
            "📌 **Geographic expansion**: Consider expanding to high-revenue cities",
            "📌 **Seasonal planning**: Prepare inventory for peak months",
            "📌 **Price optimization**: Review pricing strategy for products"
        ]
        for rec in recommendations:
            st.markdown(f"- {rec}")

else:
    # Welcome screen
    st.info("👋 Welcome to Invoice Data Extractor!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 📌 Getting Started
        1. Upload your invoice file
        2. Explore the dashboard
        3. Export reports

        **Supported formats:** CSV, Excel
        """)

    with col2:
        st.markdown("""
        ### 📊 Features
        - Interactive dashboard
        - Revenue analytics
        - Customer insights
        - Export to Excel/CSV
        """)

    with col3:
        st.markdown("""
        ### 📁 Sample Data
        Click "Load Sample Data" 
        to try the app with 
        example invoices
        """)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Invoice Data Extractor | Created by Tahir Mahmood | © 2026</p>",
    unsafe_allow_html=True
)