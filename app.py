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

from utils.data_processor import InvoiceProcessor

# Page configuration
st.set_page_config(
    page_title="Invoice Data Extractor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state
if 'processor' not in st.session_state:
    st.session_state.processor = InvoiceProcessor()
if 'df' not in st.session_state:
    st.session_state.df = None
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# Title
st.title("📊 Invoice Data Extractor & Analyzer")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📁 Data Source")

    # File upload
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload your invoice data file"
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.session_state.df = df
            st.session_state.data_loaded = True
            st.session_state.processor.load_data(df)
            st.success(f"✅ Loaded {len(df)} invoices")

            # Show file info
            st.info(f"""
            📄 **File Info:**
            - Name: {uploaded_file.name}
            - Rows: {len(df):,}
            - Columns: {len(df.columns)}
            """)

        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.session_state.data_loaded = False

    # Sample data button
    st.markdown("---")
    if st.button("📝 Load Sample Data", use_container_width=True):
        sample_path = 'data/sample_invoices.csv'
        if os.path.exists(sample_path):
            df = pd.read_csv(sample_path)
            st.session_state.df = df
            st.session_state.data_loaded = True
            st.session_state.processor.load_data(df)
            st.success("✅ Sample data loaded!")
            st.rerun()
        else:
            st.error("Sample data file not found!")

    # Filters (only if data loaded)
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
                    st.session_state.processor.filtered_df = filtered_df
                    st.info(f"Showing {len(filtered_df)} records")

        # Amount filter
        if 'amount' in df.columns:
            min_amount = float(df['amount'].min())
            max_amount = float(df['amount'].max())

            amount_range = st.slider(
                "Amount Range ($)",
                min_value=min_amount,
                max_value=max_amount,
                value=(min_amount, max_amount)
            )

            filtered_df = st.session_state.processor.filtered_df if hasattr(st.session_state.processor,
                                                                            'filtered_df') else df
            filtered_df = filtered_df[
                (filtered_df['amount'] >= amount_range[0]) &
                (filtered_df['amount'] <= amount_range[1])
                ]
            st.session_state.processor.filtered_df = filtered_df

# Main content
if st.session_state.data_loaded and st.session_state.df is not None:
    processor = st.session_state.processor
    df = processor.filtered_df if hasattr(processor, 'filtered_df') else processor.df

    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Dashboard", "📋 Data Explorer", "📊 Statistics",
        "📉 Analytics", "💡 Insights"
    ])

    # ==================== TAB 1: DASHBOARD ====================
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

    # ==================== TAB 2: DATA EXPLORER ====================
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
            # Show only important columns
            important_cols = ['first_name', 'last_name', 'email', 'amount', 'invoice_date',
                              'product_id', 'qty', 'city', 'job']
            available_cols = [col for col in important_cols if col in display_df.columns]
            display_df = display_df[available_cols]

        # Display dataframe
        st.dataframe(display_df, use_container_width=True, height=500)

        # Export options
        st.markdown("---")
        st.subheader("📥 Export Data")

        col1, col2, col3 = st.columns(3)

        with col1:
            # Export to CSV
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name=f'invoice_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv',
                use_container_width=True
            )

        with col2:
            # Export to Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Invoices', index=False)
                # Add summary sheet
                summary = pd.DataFrame({
                    'Metric': ['Total Revenue', 'Average Invoice', 'Total Invoices', 'Unique Customers'],
                    'Value': [df['amount'].sum(), df['amount'].mean(), len(df), df['email'].nunique()]
                })
                summary.to_excel(writer, sheet_name='Summary', index=False)

            excel_data = output.getvalue()
            st.download_button(
                label="📥 Download as Excel",
                data=excel_data,
                file_name=f'invoice_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )

        with col3:
            # Export filtered data
            if search_term:
                filtered_csv = display_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Filtered Data",
                    data=filtered_csv,
                    file_name=f'filtered_invoices.csv',
                    mime='text/csv',
                    use_container_width=True
                )

    # ==================== TAB 3: STATISTICS ====================
    with tab3:
        st.header("Statistical Analysis")

        # Summary statistics
        st.subheader("📊 Descriptive Statistics")

        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)

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

        # Column information
        st.subheader("📋 Column Information")
        col_info = pd.DataFrame({
            'Column Name': df.columns,
            'Data Type': df.dtypes.values,
            'Unique Values': [df[col].nunique() for col in df.columns],
            'Sample Value': [str(df[col].iloc[0])[:50] if len(df) > 0 else '' for col in df.columns]
        })
        st.dataframe(col_info, use_container_width=True)

        # Correlation matrix
        if len(numeric_cols) >= 2:
            st.subheader("📈 Correlation Matrix")
            correlation = df[numeric_cols].corr()
            fig = px.imshow(
                correlation,
                text_auto=True,
                aspect="auto",
                title="Feature Correlations",
                color_continuous_scale='RdBu'
            )
            st.plotly_chart(fig, use_container_width=True)

    # ==================== TAB 4: ANALYTICS ====================
    with tab4:
        st.header("Advanced Analytics")

        # Revenue distribution
        st.subheader("💰 Revenue Distribution")
        if 'amount' in df.columns:
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

        # Time series decomposition
        if 'invoice_date' in df.columns and 'amount' in df.columns:
            st.subheader("📅 Time Series Analysis")

            df['invoice_date'] = pd.to_datetime(df['invoice_date'])
            df['year_month'] = df['invoice_date'].dt.to_period('M').astype(str)
            monthly_revenue = df.groupby('year_month')['amount'].sum().reset_index()

            fig = px.line(
                monthly_revenue,
                x='year_month',
                y='amount',
                title='Monthly Revenue Trend',
                labels={'year_month': 'Month', 'amount': 'Revenue ($)'},
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

            # Seasonality
            col1, col2 = st.columns(2)

            with col1:
                df['month'] = df['invoice_date'].dt.month_name()
                monthly_avg = df.groupby('month')['amount'].mean().sort_index()
                fig = px.bar(
                    x=monthly_avg.index,
                    y=monthly_avg.values,
                    title='Average Revenue by Month',
                    labels={'x': 'Month', 'y': 'Average Revenue ($)'}
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                df['day_of_week'] = df['invoice_date'].dt.day_name()
                daily_avg = df.groupby('day_of_week')['amount'].mean()
                # Order days
                days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                daily_avg = daily_avg.reindex([d for d in days_order if d in daily_avg.index])

                fig = px.bar(
                    x=daily_avg.index,
                    y=daily_avg.values,
                    title='Average Revenue by Day of Week',
                    labels={'x': 'Day', 'y': 'Average Revenue ($)'}
                )
                st.plotly_chart(fig, use_container_width=True)

        # Customer segmentation
        if 'email' in df.columns and 'amount' in df.columns:
            st.subheader("👥 Customer Segmentation")

            customer_value = df.groupby('email')['amount'].sum().sort_values(ascending=False)

            # Create segments
            segments = pd.cut(
                customer_value,
                bins=[0, 100, 500, 1000, float('inf')],
                labels=['Bronze (<$100)', 'Silver ($100-$500)', 'Gold ($500-$1000)', 'Platinum ($1000+)']
            )

            segment_counts = segments.value_counts()
            fig = px.pie(
                values=segment_counts.values,
                names=segment_counts.index,
                title='Customer Segmentation by Spending',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig, use_container_width=True)

            # Show top customers
            st.subheader("🏆 Top 10 Customers")
            top_customers = df.groupby(['first_name', 'last_name', 'email']).agg({
                'amount': ['sum', 'mean', 'count'],
                'qty': 'sum' if 'qty' in df.columns else 'count'
            }).round(2)
            top_customers.columns = ['Total Spent', 'Average Order', 'Order Count', 'Total Items']
            top_customers = top_customers.sort_values('Total Spent', ascending=False).head(10)
            st.dataframe(top_customers, use_container_width=True)

    # ==================== TAB 5: INSIGHTS ====================
    with tab5:
        st.header("Business Insights & Recommendations")

        # Generate insights
        insights = processor.generate_insights()

        for insight in insights:
            st.info(insight)

        st.markdown("---")

        # Recommendations
        st.subheader("💡 Recommendations")

        recommendations = [
            "📌 **Focus on Top Products**: Invest marketing budget in top 20% of products",
            "📌 **Customer Retention**: Implement loyalty program for Platinum and Gold customers",
            "📌 **Geographic Expansion**: Consider expanding to cities with highest revenue growth",
            "📌 **Seasonal Planning**: Prepare inventory for peak months identified in analysis",
            "📌 **Price Optimization**: Review pricing strategy for low-margin products"
        ]

        for rec in recommendations:
            st.markdown(rec)

        st.markdown("---")

        # Export report
        st.subheader("📄 Generate Report")

        if st.button("Generate PDF Report", use_container_width=True):
            st.info("PDF report generation - Coming soon!")

        # Share insights
        st.subheader("🔗 Share Analysis")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📊 Dashboard Link:**")
            st.code("https://your-streamlit-app-url.com", language="text")

        with col2:
            st.markdown("**📁 Data Export:**")
            st.markdown("Use the export buttons in Data Explorer tab")

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
        - Advanced analytics
        - Customer segmentation
        - Export to Excel/CSV
        """)

    with col3:
        st.markdown("""
        ### 📁 Sample Data
        Click "Load Sample Data" 
        to try the app with 
        example invoices
        """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Invoice Data Extractor | Built with Streamlit | Tahir Mahmood | AI Enginner</p>",
    unsafe_allow_html=True
)