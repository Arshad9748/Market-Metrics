import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# Set style for better visuals
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Create output directory if it doesn't exist
os.makedirs('reports', exist_ok=True)

def load_and_preprocess_data():
    """
    Load and preprocess the sales data from CSV files
    """
    try:
        # Load the datasets
        base_dir = os.path.dirname(os.path.abspath(__file__))
        sales_data = pd.read_csv(os.path.join(base_dir, '../datasets/annex2.csv'))
        items_data = pd.read_csv(os.path.join(base_dir, '../datasets/annex1.csv'))
        wholesale_prices = pd.read_csv(os.path.join(base_dir, '../datasets/annex3.csv'))
        loss_rates = pd.read_csv(os.path.join(base_dir, '../datasets/annex4.csv'))
        
        sales_data['datetime'] = pd.to_datetime(
            sales_data['Date'] + ' ' + sales_data['Time'],
            format='mixed',
            errors='coerce'
        )
        
        # Extract date from datetime for merging
        sales_data['Date'] = sales_data['datetime'].dt.date
        
        # Convert wholesale prices date
        wholesale_prices['Date'] = pd.to_datetime(wholesale_prices['Date']).dt.date
        
        # Merge sales data with items data to get item names and categories
        sales_data = sales_data.merge(items_data[['Item Code', 'Item Name', 'Category Name']], 
                                    on='Item Code', how='left')
        
        # Merge with loss rates
        sales_data = sales_data.merge(loss_rates[['Item Code', 'Loss Rate (%)']], 
                                    on='Item Code', how='left')
        
        # Calculate net quantity (adjusting for losses)
        sales_data['Net Quantity'] = sales_data['Quantity Sold (kilo)'] * (1 - sales_data['Loss Rate (%)'] / 100)
        
        # Merge with wholesale prices
        sales_data = sales_data.merge(wholesale_prices[['Date', 'Item Code', 'Wholesale Price (RMB/kg)']], 
                                    on=['Date', 'Item Code'], how='left')
        
        # Calculate margins
        sales_data['Margin'] = sales_data['Unit Selling Price (RMB/kg)'] - sales_data['Wholesale Price (RMB/kg)']
        sales_data['Revenue'] = sales_data['Quantity Sold (kilo)'] * sales_data['Unit Selling Price (RMB/kg)']
        sales_data['Profit'] = sales_data['Quantity Sold (kilo)'] * sales_data['Margin']
        
        # Drop rows with invalid datetime
        invalid_dates = sales_data['datetime'].isna().sum()
        if invalid_dates > 0:
            print(f"Warning: Found {invalid_dates} rows with invalid dates that will be removed")
        
        sales_data = sales_data.dropna(subset=['datetime'])
        
        # Convert Date back to datetime for Prophet
        sales_data['Date'] = pd.to_datetime(sales_data['Date'])
        
        print(f"Successfully processed {len(sales_data)} sales records")
        print(f"Date range: {sales_data['datetime'].min()} to {sales_data['datetime'].max()}")
        
        return sales_data, items_data, wholesale_prices, loss_rates
    
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise

def prepare_data_for_prophet(df, item_name=None, category=None, metric='quantity'):
    """
    Prepare data for Prophet model
    """
    # Filter data if item_name or category is specified
    if item_name:
        df = df[df['Item Name'] == item_name]
    elif category:
        df = df[df['Category Name'] == category]
    
    # Calculate the metric to forecast
    if metric == 'revenue':
        df['value'] = df['Revenue']
    elif metric == 'margin':
        df['value'] = df['Profit']
    else:  # quantity
        df['value'] = df['Quantity Sold (kilo)']
    
    # Group by date and sum the values
    daily_data = df.groupby('Date')['value'].sum().reset_index()
    
    # Rename columns to Prophet requirements
    daily_data = daily_data.rename(columns={'Date': 'ds', 'value': 'y'})
    
    return daily_data

def train_prophet_model(data, periods=30, seasonality_mode='multiplicative'):
    """
    Train Prophet model and make predictions
    """
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,  # Disable daily seasonality for cleaner results
        seasonality_mode=seasonality_mode,
        interval_width=0.8  # 80% confidence interval
    )
    
    model.fit(data)
    
    # Create future dates for forecasting
    future_dates = model.make_future_dataframe(periods=periods)
    
    # Make predictions
    forecast = model.predict(future_dates)
    
    return model, forecast

def create_improved_forecast_plot(model, forecast, actual_data, title="Sales Forecast", output_dir='reports'):
    """
    Create improved forecast visualization with Plotly
    """
    # Create subplot figure
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=[f'{title} - Main Forecast', 'Forecast Components'],
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3]
    )
    
    # Main forecast plot
    fig.add_trace(
        go.Scatter(
            x=actual_data['ds'],
            y=actual_data['y'],
            mode='lines+markers',
            name='Actual',
            line=dict(color='blue', width=2),
            marker=dict(size=4)
        ),
        row=1, col=1
    )
    
    # Forecast line
    fig.add_trace(
        go.Scatter(
            x=forecast['ds'],
            y=forecast['yhat'],
            mode='lines',
            name='Forecast',
            line=dict(color='red', width=2, dash='dash')
        ),
        row=1, col=1
    )
    
    # Confidence interval
    fig.add_trace(
        go.Scatter(
            x=list(forecast['ds']) + list(forecast['ds'][::-1]),
            y=list(forecast['yhat_upper']) + list(forecast['yhat_lower'][::-1]),
            fill='toself',
            fillcolor='rgba(255,0,0,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Confidence Interval',
            showlegend=True
        ),
        row=1, col=1
    )
    
    # Trend component
    fig.add_trace(
        go.Scatter(
            x=forecast['ds'],
            y=forecast['trend'],
            mode='lines',
            name='Trend',
            line=dict(color='green', width=2)
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        title=title,
        height=800,
        showlegend=True,
        template='plotly_white'
    )
    
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Value", row=1, col=1)
    fig.update_yaxes(title_text="Trend", row=2, col=1)
    
    fig.write_html(os.path.join(output_dir, f'{title.lower().replace(" ", "_")}_forecast.html'))
    return fig

def analyze_sales_patterns(sales_data, output_dir='reports'):
    """
    Create improved analysis with better visualizations
    """
    try:
        # 1. Daily sales trend with moving average
        daily_sales = sales_data.groupby('Date').agg({
            'Quantity Sold (kilo)': 'sum',
            'Revenue': 'sum',
            'Profit': 'sum'
        }).reset_index()
        
        # Calculate 7-day moving average
        daily_sales['MA_7'] = daily_sales['Quantity Sold (kilo)'].rolling(window=7).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_sales['Date'],
            y=daily_sales['Quantity Sold (kilo)'],
            mode='lines',
            name='Daily Sales',
            line=dict(color='lightblue', width=1),
            opacity=0.7
        ))
        fig.add_trace(go.Scatter(
            x=daily_sales['Date'],
            y=daily_sales['MA_7'],
            mode='lines',
            name='7-Day Moving Average',
            line=dict(color='red', width=3)
        ))
        fig.update_layout(
            title='Daily Sales Pattern with Moving Average',
            xaxis_title='Date',
            yaxis_title='Quantity Sold (kg)',
            template='plotly_white'
        )
        fig.write_html(os.path.join(output_dir, 'daily_sales_trend.html'))
        
        # 2. Top categories analysis (limit to top 10)
        category_sales = sales_data.groupby('Category Name').agg({
            'Quantity Sold (kilo)': 'sum',
            'Revenue': 'sum',
            'Unit Selling Price (RMB/kg)': 'mean',
            'Margin': 'mean'
        }).reset_index()
        
        top_categories = category_sales.nlargest(10, 'Quantity Sold (kilo)')
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Sales Volume', 'Revenue', 'Avg Price', 'Avg Margin'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Sales volume
        fig.add_trace(
            go.Bar(x=top_categories['Category Name'], 
                   y=top_categories['Quantity Sold (kilo)'],
                   name='Volume',
                   marker_color='lightblue'),
            row=1, col=1
        )
        
        # Revenue
        fig.add_trace(
            go.Bar(x=top_categories['Category Name'], 
                   y=top_categories['Revenue'],
                   name='Revenue',
                   marker_color='lightgreen'),
            row=1, col=2
        )
        
        # Average price
        fig.add_trace(
            go.Bar(x=top_categories['Category Name'], 
                   y=top_categories['Unit Selling Price (RMB/kg)'],
                   name='Avg Price',
                   marker_color='orange'),
            row=2, col=1
        )
        
        # Average margin
        fig.add_trace(
            go.Bar(x=top_categories['Category Name'], 
                   y=top_categories['Margin'],
                   name='Avg Margin',
                   marker_color='red'),
            row=2, col=2
        )
        
        fig.update_layout(
            title='Top 10 Categories Analysis',
            height=800,
            showlegend=False,
            template='plotly_white'
        )
        
        # Rotate x-axis labels for better readability
        fig.update_xaxes(tickangle=45)
        
        fig.write_html(os.path.join(output_dir, 'top_categories_analysis.html'))
        
        # 3. Product performance matrix (top 20 products only)
        product_performance = sales_data.groupby('Item Name').agg({
            'Quantity Sold (kilo)': 'sum',
            'Revenue': 'sum',
            'Margin': 'mean',
            'Loss Rate (%)': 'first',
            'Unit Selling Price (RMB/kg)': 'mean'
        }).reset_index()
        
        # Select top 20 products by revenue
        top_products = product_performance.nlargest(20, 'Revenue')
        
        fig = px.scatter(
            top_products,
            x='Margin',
            y='Revenue',
            size='Quantity Sold (kilo)',
            color='Loss Rate (%)',
            hover_name='Item Name',
            hover_data=['Unit Selling Price (RMB/kg)'],
            title='Product Performance Matrix (Top 20 by Revenue)',
            labels={
                'Margin': 'Average Margin (RMB/kg)',
                'Revenue': 'Total Revenue (RMB)',
                'Loss Rate (%)': 'Loss Rate (%)'
            },
            color_continuous_scale='RdYlBu_r'
        )
        
        fig.update_layout(
            template='plotly_white',
            height=600
        )
        
        fig.write_html(os.path.join(output_dir, 'product_performance_matrix.html'))
        
        # 4. Loss rate impact analysis (top 15 items with highest losses)
        loss_impact = sales_data.groupby('Item Name').agg({
            'Loss Rate (%)': 'first',
            'Quantity Sold (kilo)': 'sum',
            'Revenue': 'sum'
        }).reset_index()
        
        loss_impact['Total Loss (kg)'] = loss_impact['Quantity Sold (kilo)'] * loss_impact['Loss Rate (%)'] / 100
        loss_impact['Loss Value (RMB)'] = loss_impact['Total Loss (kg)'] * (loss_impact['Revenue'] / loss_impact['Quantity Sold (kilo)'])
        
        top_losses = loss_impact.nlargest(15, 'Loss Value (RMB)')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_losses['Item Name'],
            y=top_losses['Loss Value (RMB)'],
            name='Loss Value',
            marker_color='red',
            text=top_losses['Loss Rate (%)'].round(1).astype(str) + '%',
            textposition='auto'
        ))
        
        fig.update_layout(
            title='Top 15 Products by Loss Value Impact',
            xaxis_title='Product Name',
            yaxis_title='Loss Value (RMB)',
            xaxis_tickangle=45,
            template='plotly_white',
            height=600
        )
        
        fig.write_html(os.path.join(output_dir, 'loss_impact_analysis.html'))
        
        # 5. Time-based sales heatmap
        sales_data['Hour'] = sales_data['datetime'].dt.hour
        sales_data['DayOfWeek'] = sales_data['datetime'].dt.day_name()
        
        hourly_pattern = sales_data.groupby(['DayOfWeek', 'Hour'])['Quantity Sold (kilo)'].sum().reset_index()
        hourly_pivot = hourly_pattern.pivot(index='DayOfWeek', columns='Hour', values='Quantity Sold (kilo)').fillna(0)
        
        # Reorder days of week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hourly_pivot = hourly_pivot.reindex(day_order, fill_value=0)
        
        fig = px.imshow(
            hourly_pivot.values,
            x=hourly_pivot.columns,
            y=hourly_pivot.index,
            color_continuous_scale='Blues',
            title='Sales Heatmap by Day and Hour',
            labels={'x': 'Hour of Day', 'y': 'Day of Week', 'color': 'Quantity Sold (kg)'}
        )
        
        fig.update_layout(
            template='plotly_white',
            height=500
        )
        
        fig.write_html(os.path.join(output_dir, 'sales_heatmap.html'))
        
        # 6. Summary dashboard
        create_summary_dashboard(sales_data, output_dir)
        
        print("Successfully generated all improved analysis plots")
        
    except Exception as e:
        print(f"Error in analyze_sales_patterns: {str(e)}")
        raise

def create_summary_dashboard(sales_data, output_dir='reports'):
    """
    Create a comprehensive summary dashboard
    """
    # Calculate key metrics
    total_revenue = sales_data['Revenue'].sum()
    total_quantity = sales_data['Quantity Sold (kilo)'].sum()
    avg_margin = sales_data['Margin'].mean()
    total_products = sales_data['Item Name'].nunique()
    total_categories = sales_data['Category Name'].nunique()
    
    # Create dashboard
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=[
            'Revenue Trend', 'Top 5 Categories by Revenue',
            'Daily Sales Distribution', 'Margin Distribution',
            'Loss Rate vs Sales Volume', 'Key Metrics'
        ],
        specs=[[{"colspan": 1}, {"colspan": 1}],
               [{"colspan": 1}, {"colspan": 1}],
               [{"colspan": 1}, {"type": "table", "colspan": 1}]]
    )
    
    # Revenue trend
    daily_revenue = sales_data.groupby('Date')['Revenue'].sum().reset_index()
    fig.add_trace(
        go.Scatter(x=daily_revenue['Date'], y=daily_revenue['Revenue'],
                  mode='lines', name='Daily Revenue', line=dict(color='green')),
        row=1, col=1
    )
    
    # Top categories
    top_cat_revenue = sales_data.groupby('Category Name')['Revenue'].sum().nlargest(5).reset_index()
    fig.add_trace(
        go.Bar(x=top_cat_revenue['Category Name'], y=top_cat_revenue['Revenue'],
               name='Top Categories', marker_color='lightblue'),
        row=1, col=2
    )
    
    # Daily sales distribution
    daily_quantity = sales_data.groupby('Date')['Quantity Sold (kilo)'].sum()
    fig.add_trace(
        go.Histogram(x=daily_quantity.values, name='Daily Sales Dist',
                    marker_color='orange', nbinsx=20),
        row=2, col=1
    )
    
    # Margin distribution
    fig.add_trace(
        go.Histogram(x=sales_data['Margin'].values, name='Margin Dist',
                    marker_color='red', nbinsx=30),
        row=2, col=2
    )
    
    # Loss rate vs sales
    loss_vs_sales = sales_data.groupby('Item Name').agg({
        'Loss Rate (%)': 'first',
        'Quantity Sold (kilo)': 'sum'
    }).reset_index().head(20)
    
    fig.add_trace(
        go.Scatter(x=loss_vs_sales['Loss Rate (%)'], y=loss_vs_sales['Quantity Sold (kilo)'],
                  mode='markers', name='Loss vs Sales', marker=dict(color='purple')),
        row=3, col=1
    )
    
    # Key metrics table
    metrics_data = [
        ['Total Revenue (RMB)', f'{total_revenue:,.2f}'],
        ['Total Quantity Sold (kg)', f'{total_quantity:,.2f}'],
        ['Average Margin (RMB/kg)', f'{avg_margin:.2f}'],
        ['Number of Products', f'{total_products}'],
        ['Number of Categories', f'{total_categories}'],
        ['Date Range', f"{sales_data['Date'].min().strftime('%Y-%m-%d')} to {sales_data['Date'].max().strftime('%Y-%m-%d')}"]
    ]
    
    fig.add_trace(
        go.Table(
            header=dict(values=['Metric', 'Value'], fill_color='lightblue'),
            cells=dict(values=list(zip(*metrics_data)), fill_color='white')
        ),
        row=3, col=2
    )
    
    fig.update_layout(
        title='Sales Analytics Dashboard',
        height=1200,
        showlegend=False,
        template='plotly_white'
    )
    
    fig.write_html(os.path.join(output_dir, 'sales_dashboard.html'))

def main():
    try:
        # Load and preprocess data
        print("Loading and preprocessing data...")
        sales_data, items_data, wholesale_prices, loss_rates = load_and_preprocess_data()
        
        # Analyze overall sales patterns
        print("Analyzing sales patterns...")
        analyze_sales_patterns(sales_data)
        
        # Generate forecasts for different metrics
        metrics = [
            ('quantity', 'Quantity Sales'),
            ('revenue', 'Revenue'),
            ('margin', 'Profit Margin')
        ]
        
        for metric_key, metric_name in metrics:
            print(f"\nGenerating {metric_name} forecast...")
            forecast_data = prepare_data_for_prophet(sales_data, metric=metric_key)
            
            if len(forecast_data) > 1:  # Ensure we have enough data
                # Train model and make predictions
                model, forecast = train_prophet_model(forecast_data, periods=30)
                
                # Create improved forecast plot
                create_improved_forecast_plot(model, forecast, forecast_data, 
                                            f"{metric_name} Forecast")
            else:
                print(f"Not enough data for {metric_name} forecast")
        
        print("\n" + "="*50)
        print("IMPROVED FORECASTING COMPLETED!")
        print("="*50)
        print("\nGenerated Reports:")
        print("📊 sales_dashboard.html - Comprehensive overview dashboard")
        print("📈 daily_sales_trend.html - Daily sales with moving averages")
        print("🏆 top_categories_analysis.html - Top 10 categories breakdown")
        print("💎 product_performance_matrix.html - Top 20 products analysis")
        print("⚠️ loss_impact_analysis.html - Loss impact analysis")
        print("🕐 sales_heatmap.html - Time-based sales patterns")
        print("🔮 *_forecast.html - Prophet forecasting results")
        print(f"\n📁 All reports saved to: {os.path.abspath('reports')}/")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()