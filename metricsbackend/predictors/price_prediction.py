import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib
from datetime import datetime
import os

class PricePredictionModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = [] 
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base_dir, 'models', 'price_prediction_model.joblib')
        self.scaler_path = os.path.join(base_dir, 'models', 'price_scaler.joblib')
        self.label_encoders_path = os.path.join(base_dir, 'models', 'label_encoders.joblib')
        self.feature_columns_path = os.path.join(base_dir, 'models', 'feature_columns.joblib')
        
    def load_and_preprocess_data(self):
        """Load and preprocess the data for price prediction"""
        try:        
            base_dir = os.path.dirname(os.path.abspath(__file__))
            sales_data = pd.read_csv(os.path.join(base_dir, '../datasets/annex2.csv'))
            items_data = pd.read_csv(os.path.join(base_dir, '../datasets/annex1.csv'))
            wholesale_prices = pd.read_csv(os.path.join(base_dir, '../datasets/annex3.csv'))
            loss_rates = pd.read_csv(os.path.join(base_dir, '../datasets/annex4.csv'))
        
            sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%Y-%m-%d')
            wholesale_prices['Date'] = pd.to_datetime(wholesale_prices['Date'], format='%Y-%m-%d')
            
            sales_data['hour'] = pd.to_datetime(sales_data['Time'], format='mixed').dt.hour
            
            # Merge all datasets
            df = sales_data.merge(items_data, on='Item Code', how='left')
            df = df.merge(wholesale_prices[['Date', 'Item Code', 'Wholesale Price (RMB/kg)']], on=['Date', 'Item Code'], how='left')
            df = df.merge(loss_rates[['Item Code', 'Loss Rate (%)']], on='Item Code', how='left')
            
            # Extract time-based features
            df['month'] = df['Date'].dt.month
            df['dayofweek'] = df['Date'].dt.dayofweek
            
            # Define feature columns - this is critical for consistency
            self.feature_columns = [
                'Quantity Sold (kilo)', 'Wholesale Price (RMB/kg)', 
                'Loss Rate (%)', 'month', 'dayofweek', 'hour',
                'Category Name', 'Item Name'
            ]
            
            # Handle categorical variables BEFORE selecting features
            categorical_columns = ['Category Name', 'Item Name']
            for col in categorical_columns:
                if col in df.columns:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
            
            # Now select features - ensure all columns exist
            missing_cols = [col for col in self.feature_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing columns in training data: {missing_cols}")
                
            X = df[self.feature_columns].copy()
            y = df['Unit Selling Price (RMB/kg)']
            
            # Fill any NaN values
            X = X.fillna(0)
            return X, y
            
        except Exception as e:
            print(f"Error in data preprocessing: {str(e)}")
            raise
    
    def train(self):
        """Train the price prediction model"""
        try:
            os.makedirs('models', exist_ok=True)
            
            X, y = self.load_and_preprocess_data()
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale numerical features only
            numerical_columns = X.select_dtypes(include=[np.number]).columns
            categorical_columns = [col for col in X.columns if col not in numerical_columns]
            
            print(f"Numerical columns: {numerical_columns.tolist()}")
            print(f"Categorical columns: {categorical_columns}")
            
            # Create copies to avoid SettingWithCopyWarning
            X_train_scaled = X_train.copy()
            X_test_scaled = X_test.copy()
            
            # Scale only numerical columns
            if len(numerical_columns) > 0:
                X_train_scaled[numerical_columns] = self.scaler.fit_transform(X_train[numerical_columns])
                X_test_scaled[numerical_columns] = self.scaler.transform(X_test[numerical_columns])
            
            # Train model
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.model.fit(X_train_scaled, y_train)
            
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            joblib.dump(self.label_encoders, self.label_encoders_path)
            joblib.dump(self.feature_columns, self.feature_columns_path)  

            train_score = self.model.score(X_train_scaled, y_train)
            test_score = self.model.score(X_test_scaled, y_test)
            
            print(f"Model R² score on training data: {train_score:.4f}")
            print(f"Model R² score on test data: {test_score:.4f}")
            print(f"Feature columns saved: {self.feature_columns}")
            
            return train_score, test_score
            
        except Exception as e:
            print(f"Error in model training: {str(e)}")
            raise
    
    def load_model(self):
        """Load the trained model and preprocessing objects"""
        try:
            required_files = [
                self.model_path,
                self.scaler_path, 
                self.label_encoders_path,
                self.feature_columns_path
            ]
            
            if all(os.path.exists(file) for file in required_files):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.label_encoders = joblib.load(self.label_encoders_path)
                self.feature_columns = joblib.load(self.feature_columns_path)
                return True
            else:
                missing_files = [f for f in required_files if not os.path.exists(f)]
                print(f"Missing model files: {missing_files}")
                return False
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False
    
    def predict(self, features):    
        """Make price predictions for new data"""
        try:
            if self.model is None:
                if not self.load_model():
                    raise Exception("Model not trained. Please train the model first.")
            
            prediction_df = pd.DataFrame()
            
            for col in self.feature_columns:
                if col in features.columns:
                    prediction_df[col] = features[col]
                else:
                    # Handle missing columns with defaults
                    if col in ['month', 'dayofweek', 'hour']:
                        prediction_df[col] = 0  
                    else:
                        prediction_df[col] = 0  
                        
            # Handle categorical features
            for col in self.label_encoders:
                if col in prediction_df.columns:
                    try:
                        prediction_df[col] = prediction_df[col].astype(str)
                        prediction_df[col] = self.label_encoders[col].transform(prediction_df[col])
                    except ValueError as e:
                        valid_classes = list(self.label_encoders[col].classes_)
                        prediction_df[col] = self.label_encoders[col].transform([valid_classes[0]] * len(prediction_df))
            
            numerical_columns = prediction_df.select_dtypes(include=[np.number]).columns
            if len(numerical_columns) > 0:
                prediction_df[numerical_columns] = self.scaler.transform(prediction_df[numerical_columns])
            
            prediction_df = prediction_df[self.feature_columns]
            
            return self.model.predict(prediction_df)
            
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            raise

    def get_feature_info(self):
        """Get information about expected features for the API"""
        if not self.feature_columns:
            self.load_model()
            
        categorical_features = list(self.label_encoders.keys()) if self.label_encoders else []
        
        return {
            'required_features': self.feature_columns,
            'categorical_features': categorical_features,
            'valid_categories': {
                col: list(encoder.classes_) 
                for col, encoder in self.label_encoders.items()
            } if self.label_encoders else {}
        }

if __name__ == "__main__":
    model = PricePredictionModel()
    train_score, test_score = model.train()