from flask import jsonify, request
from datetime import datetime
import pandas as pd
import traceback
from predictors.price_prediction import PricePredictionModel
from predictors.quantity_prediction import QuantityPredictionModel
from routes.auth_routes import token_required

# Initialize both models
price_model = PricePredictionModel()
quantity_model = QuantityPredictionModel()

price_model_loaded = price_model.load_model()
quantity_model_loaded = quantity_model.load_model()

if not price_model_loaded:
    print("Warning: Price model not loaded at startup. Please train the model first.")
    
if not quantity_model_loaded:
    print("Warning: Quantity model not loaded at startup. Please train the model first.")

def init_model_routes(app):
    
    # ================== PRICE PREDICTION ROUTES ==================
    
    @app.route('/api/price-model-info', methods=['GET'])
    @token_required
    def get_price_model_info():
        """Get information about the price model's expected features"""
        try:
            if not price_model.model:
                return jsonify({
                    'success': False,
                    'error': 'Price model not loaded. Please train the model first.'
                }), 400
                
            feature_info = price_model.get_feature_info()
            return jsonify({
                'success': True,
                'model_type': 'price_prediction',
                'feature_info': feature_info
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/predict-price', methods=['POST'])
    @token_required
    def predict_price():
        try:
            if not price_model.model:
                return jsonify({
                    'success': False,
                    'error': 'Price model not loaded. Please train the model first.'
                }), 400
                
            data = request.get_json()
            
            # Required fields validation
            required_fields = ['quantity_sold', 'wholesale_price', 'loss_rate', 'date', 'time', 'category_name', 'item_name']
            missing_fields = [field for field in required_fields if field not in data or data[field] is None]
            
            if missing_fields:
                return jsonify({
                    'success': False,
                    'error': f'Missing required fields: {", ".join(missing_fields)}',
                    'required_fields': required_fields
                }), 400
            
            features_dict = {}
            
            # Type validation for numeric fields
            try:
                features_dict['Quantity Sold (kilo)'] = float(data['quantity_sold'])
                features_dict['Wholesale Price (RMB/kg)'] = float(data['wholesale_price'])
                features_dict['Loss Rate (%)'] = float(data['loss_rate'])
            except ValueError as e:
                return jsonify({
                    'success': False,
                    'error': 'Invalid numeric value provided for quantity_sold, wholesale_price, or loss_rate. All must be valid numbers.'
                }), 400
            
            # Date and time validation
            try:
                date_obj = datetime.strptime(data['date'], '%Y-%m-%d')
                time_obj = datetime.strptime(data['time'], '%H:%M:%S')
                
                features_dict['month'] = date_obj.month
                features_dict['dayofweek'] = date_obj.weekday()
                features_dict['hour'] = time_obj.hour
            except ValueError as e:
                return jsonify({
                    'success': False,
                    'error': 'Invalid date or time format. Use YYYY-MM-DD for date and HH:MM:SS for time.'
                }), 400
                    
            features_dict['Category Name'] = str(data['category_name'])
            features_dict['Item Name'] = str(data['item_name'])
            
            # Create DataFrame
            features = pd.DataFrame([features_dict])
            # Make prediction
            predicted_price = price_model.predict(features)
            
            return jsonify({
                'success': True,
                'predicted_price': float(predicted_price[0]),
                'input_features': features_dict,
                'model_type': 'price_prediction'
            })
            
        except Exception as e:
            print(f"Price prediction error: {str(e)}")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400

    @app.route('/api/retrain-price-model', methods=['POST'])
    @token_required
    def retrain_price_model():
        """Endpoint to retrain the price model"""
        try:
            print("Starting price model retraining...")
            train_score, test_score = price_model.train()
            
            return jsonify({
                'success': True,
                'message': 'Price model retrained successfully',
                'model_type': 'price_prediction',
                'train_score': train_score,
                'test_score': test_score
            })
        except Exception as e:
            print(f"Price model retraining error: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    # ================== QUANTITY PREDICTION ROUTES ==================
    
    @app.route('/api/quantity-model-info', methods=['GET'])
    @token_required
    def get_quantity_model_info():
        """Get information about the quantity model's expected features"""
        try:
            if not quantity_model.model:
                return jsonify({
                    'success': False,
                    'error': 'Quantity model not loaded. Please train the model first.'
                }), 400
                
            feature_info = quantity_model.get_feature_info()
            return jsonify({
                'success': True,
                'model_type': 'quantity_prediction',
                'feature_info': feature_info
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/predict-quantity', methods=['POST'])
    @token_required
    def predict_quantity():
        try:
            if not quantity_model.model:
                return jsonify({
                    'success': False,
                    'error': 'Quantity model not loaded. Please train the model first.'
                }), 400
                
            data = request.get_json()
            
            # Required fields validation
            required_fields = ['selling_price', 'wholesale_price', 'loss_rate', 'date', 'time', 'category_name', 'item_name']
            missing_fields = [field for field in required_fields if field not in data or data[field] is None]
            
            if missing_fields:
                return jsonify({
                    'success': False,
                    'error': f'Missing required fields: {", ".join(missing_fields)}',
                    'required_fields': required_fields
                }), 400
            
            features_dict = {}
            
            # Type validation for numeric fields
            try:
                selling_price = float(data['selling_price'])
                wholesale_price = float(data['wholesale_price'])
                loss_rate = float(data['loss_rate'])
                
                features_dict['Unit Selling Price (RMB/kg)'] = selling_price
                features_dict['Wholesale Price (RMB/kg)'] = wholesale_price
                features_dict['Loss Rate (%)'] = loss_rate
                
                # Calculate derived features
                features_dict['price_efficiency'] = selling_price / wholesale_price if wholesale_price > 0 else 1.0
                features_dict['adjusted_price'] = selling_price * (1 + loss_rate / 100)
                
            except ValueError as e:
                return jsonify({
                    'success': False,
                    'error': 'Invalid numeric value provided for selling_price, wholesale_price, or loss_rate. All must be valid numbers.'
                }), 400
            
            # Date and time validation
            try:
                date_obj = datetime.strptime(data['date'], '%Y-%m-%d')
                time_obj = datetime.strptime(data['time'], '%H:%M:%S')
                
                features_dict['month'] = date_obj.month
                features_dict['dayofweek'] = date_obj.weekday()
                features_dict['hour'] = time_obj.hour
                features_dict['is_weekend'] = 1 if date_obj.weekday() in [5, 6] else 0
            except ValueError as e:
                return jsonify({
                    'success': False,
                    'error': 'Invalid date or time format. Use YYYY-MM-DD for date and HH:MM:SS for time.'
                }), 400
                    
            features_dict['Category Name'] = str(data['category_name'])
            features_dict['Item Name'] = str(data['item_name'])
            
            # Create DataFrame
            features = pd.DataFrame([features_dict])
            # Make prediction
            predicted_quantity = quantity_model.predict(features)
            
            return jsonify({
                'success': True,
                'predicted_quantity': float(predicted_quantity[0]),
                'input_features': features_dict,
                'model_type': 'quantity_prediction'
            })
            
        except Exception as e:
            print(f"Quantity prediction error: {str(e)}")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400

    @app.route('/api/retrain-quantity-model', methods=['POST'])
    @token_required
    def retrain_quantity_model():
        """Endpoint to retrain the quantity model"""
        try:
            print("Starting quantity model retraining...")
            train_score, test_score = quantity_model.train()
            
            return jsonify({
                'success': True,
                'message': 'Quantity model retrained successfully',
                'model_type': 'quantity_prediction',
                'train_score': train_score,
                'test_score': test_score
            })
        except Exception as e:
            print(f"Quantity model retraining error: {str(e)}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    # ================== COMBINED PREDICTION ROUTES ==================
    
    @app.route('/api/predict-both', methods=['POST'])
    @token_required
    def predict_both():
        """Predict both price and quantity for comprehensive forecasting"""
        try:
            if not price_model.model or not quantity_model.model:
                return jsonify({
                    'success': False,
                    'error': 'One or both models not loaded. Please train both models first.'
                }), 400
                
            data = request.get_json()
            
            # For combined prediction, we need different inputs depending on what we're predicting
            required_fields = ['wholesale_price', 'loss_rate', 'date', 'time', 'category_name', 'item_name']
            missing_fields = [field for field in required_fields if field not in data or data[field] is None]
            
            if missing_fields:
                return jsonify({
                    'success': False,
                    'error': f'Missing required fields: {", ".join(missing_fields)}',
                    'required_fields': required_fields
                }), 400
            
            # If selling_price is provided, predict quantity
            # If quantity_sold is provided, predict price
            # If neither is provided, use average values or return error
            
            has_price = 'selling_price' in data and data['selling_price'] is not None
            has_quantity = 'quantity_sold' in data and data['quantity_sold'] is not None
            
            if not has_price and not has_quantity:
                return jsonify({
                    'success': False,
                    'error': 'Must provide either selling_price or quantity_sold for combined prediction'
                }), 400
            
            results = {}
            
            # Common features
            try:
                wholesale_price = float(data['wholesale_price'])
                loss_rate = float(data['loss_rate'])
                
                date_obj = datetime.strptime(data['date'], '%Y-%m-%d')
                time_obj = datetime.strptime(data['time'], '%H:%M:%S')
                
                common_features = {
                    'Wholesale Price (RMB/kg)': wholesale_price,
                    'Loss Rate (%)': loss_rate,
                    'month': date_obj.month,
                    'dayofweek': date_obj.weekday(),
                    'hour': time_obj.hour,
                    'Category Name': str(data['category_name']),
                    'Item Name': str(data['item_name'])
                }
                
            except ValueError as e:
                return jsonify({
                    'success': False,
                    'error': 'Invalid numeric or date/time values provided'
                }), 400
            
            # Predict quantity if price is given
            if has_price:
                try:
                    selling_price = float(data['selling_price'])
                    quantity_features = common_features.copy()
                    quantity_features.update({
                        'Unit Selling Price (RMB/kg)': selling_price,
                        'price_efficiency': selling_price / wholesale_price if wholesale_price > 0 else 1.0,
                        'adjusted_price': selling_price * (1 + loss_rate / 100),
                        'is_weekend': 1 if date_obj.weekday() in [5, 6] else 0
                    })
                    
                    quantity_df = pd.DataFrame([quantity_features])
                    predicted_quantity = quantity_model.predict(quantity_df)
                    results['predicted_quantity'] = float(predicted_quantity[0])
                    
                except Exception as e:
                    results['quantity_error'] = str(e)
            
            # Predict price if quantity is given
            if has_quantity:
                try:
                    quantity_sold = float(data['quantity_sold'])
                    price_features = common_features.copy()
                    price_features['Quantity Sold (kilo)'] = quantity_sold
                    
                    price_df = pd.DataFrame([price_features])
                    predicted_price = price_model.predict(price_df)
                    results['predicted_price'] = float(predicted_price[0])
                    
                except Exception as e:
                    results['price_error'] = str(e)
            
            return jsonify({
                'success': True,
                'predictions': results,
                'input_data': data,
                'model_type': 'combined_prediction'
            })
            
        except Exception as e:
            print(f"Combined prediction error: {str(e)}")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400

    @app.route('/api/models-status', methods=['GET'])
    @token_required
    def get_models_status():
        """Get the status of all models"""
        return jsonify({
            'success': True,
            'models': {
                'price_model': {
                    'loaded': price_model.model is not None,
                    'type': 'price_prediction'
                },
                'quantity_model': {
                    'loaded': quantity_model.model is not None,
                    'type': 'quantity_prediction'
                }
            }
        })

    return app