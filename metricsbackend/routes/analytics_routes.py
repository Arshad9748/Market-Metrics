from flask import jsonify, request
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly
from datetime import datetime
import os
import traceback
import json
from routes.auth_routes import token_required
from predictors.sales_forecasting import analyze_sales_patterns, create_improved_forecast_plot
from predictors.price_prediction import PricePredictionModel
from predictors.quantity_prediction import QuantityPredictionModel

# Initialize models
price_model = PricePredictionModel()
quantity_model = QuantityPredictionModel()

def load_sales_data():
    """Helper function to load and preprocess sales data"""
    try:
        sales_data = pd.read_csv('datasets/annex2.csv')
        
        # Print column names for debugging
        print("Available columns:", sales_data.columns.tolist())
        
        # Convert date and time columns to datetime with mixed format handling
        sales_data['DateTime'] = pd.to_datetime(
            sales_data['Date'] + ' ' + sales_data['Time'],
            format='mixed'  # This will automatically detect and handle different time formats
        )
        
        # Calculate revenue
        sales_data['Revenue'] = sales_data['Quantity Sold (kilo)'] * sales_data['Unit Selling Price (RMB/kg)']
        return sales_data
    except Exception as e:
        print(f"Error loading sales data: {str(e)}")
        print(traceback.format_exc())
        raise

def fig_to_json(fig):
    """Convert a Plotly figure to a JSON-serializable dictionary"""
    return {
        'data': json.loads(json.dumps(fig.data, cls=plotly.utils.PlotlyJSONEncoder)),
        'layout': json.loads(json.dumps(fig.layout, cls=plotly.utils.PlotlyJSONEncoder))
    }

def init_analytics_routes(app):
    @app.route('/api/analytics/sales-dashboard', methods=['GET'])
    @token_required
    def get_sales_dashboard():
        """Get comprehensive sales dashboard data"""
        try:
            # Load and preprocess data
            sales_data = load_sales_data()
            
            # Create dashboard visualizations
            daily_sales = sales_data.groupby('Date').agg({
                'Quantity Sold (kilo)': 'sum',
                'Revenue': 'sum'
            }).reset_index()
            
            # Create main dashboard figure
            fig = go.Figure()
            
            # Add daily sales line
            fig.add_trace(go.Scatter(
                x=daily_sales['Date'],
                y=daily_sales['Quantity Sold (kilo)'],
                mode='lines',
                name='Daily Sales',
                line=dict(color='lightblue', width=1)
            ))
            
            # Add 7-day moving average
            daily_sales['MA_7'] = daily_sales['Quantity Sold (kilo)'].rolling(window=7).mean()
            fig.add_trace(go.Scatter(
                x=daily_sales['Date'],
                y=daily_sales['MA_7'],
                mode='lines',
                name='7-Day Moving Average',
                line=dict(color='red', width=3)
            ))
            
            # Add revenue bar chart
            fig.add_trace(go.Bar(
                x=daily_sales['Date'],
                y=daily_sales['Revenue'],
                name='Daily Revenue',
                yaxis='y2',
                opacity=0.3
            ))
            
            # Update layout with dual y-axes
            fig.update_layout(
                title='Sales Dashboard',
                xaxis_title='Date',
                yaxis_title='Quantity Sold (kg)',
                yaxis2=dict(
                    title='Revenue (RMB)',
                    overlaying='y',
                    side='right'
                ),
                template='plotly_white',
                height=800,
                showlegend=True
            )
            
            return jsonify({
                'success': True,
                'data': fig_to_json(fig)
            })
            
        except Exception as e:
            print(f"Error in sales dashboard: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/analytics/sales-forecast', methods=['GET'])
    @token_required
    def get_sales_forecast():
        """Get sales forecast data"""
        try:
            # Load and preprocess data
            sales_data = load_sales_data()
            
            # Prepare data for forecasting
            forecast_data = sales_data.groupby('Date').agg({
                'Quantity Sold (kilo)': 'sum'
            }).reset_index()
            forecast_data.columns = ['ds', 'y']
            
            # Create forecast visualization
            fig = go.Figure()
            
            # Add historical data
            fig.add_trace(go.Scatter(
                x=forecast_data['ds'],
                y=forecast_data['y'],
                mode='lines',
                name='Historical Sales',
                line=dict(color='blue', width=2)
            ))
            
            # Update layout
            fig.update_layout(
                title='Sales Forecast',
                xaxis_title='Date',
                yaxis_title='Quantity Sold (kg)',
                template='plotly_white',
                height=600
            )
            
            return jsonify({
                'success': True,
                'data': fig_to_json(fig)
            })
            
        except Exception as e:
            print(f"Error in sales forecast: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/analytics/sales-heatmap', methods=['GET'])
    @token_required
    def get_sales_heatmap():
        """Get time-based sales patterns visualization"""
        try:
            # Load and preprocess data
            sales_data = load_sales_data()
            
            # Extract hour and day from DateTime
            sales_data['Hour'] = sales_data['DateTime'].dt.hour
            sales_data['Day'] = sales_data['DateTime'].dt.day_name()
            
            # Create pivot table for heatmap
            heatmap_data = sales_data.pivot_table(
                values='Quantity Sold (kilo)',
                index='Day',
                columns='Hour',
                aggfunc='sum'
            )
            
            # Sort days in correct order
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            heatmap_data = heatmap_data.reindex(day_order)
            
            # Create visualization
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='Viridis'
            ))
            
            # Update layout
            fig.update_layout(
                title='Sales Heatmap by Time and Day',
                xaxis_title='Hour of Day',
                yaxis_title='Day of Week',
                template='plotly_white',
                height=600
            )
            
            return jsonify({
                'success': True,
                'data': fig_to_json(fig)
            })
            
        except Exception as e:
            print(f"Error in sales heatmap: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500


    return app
