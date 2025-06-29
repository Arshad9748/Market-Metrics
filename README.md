# Market Metrics 

**Project Title**: MarketMetrics: A Big Market Analysis
A React and Tailwind CSS frontend with a Flask-based backend service for market price predictions and analytics.

## Team
This project was developed by:
- **ARSHAD MURTAZA AHMED** - [Project Lead]
- **Subinoy Khatua.**
- **Sayan Malakar** 
- **Praveen Kumar**
- **Rimi Das** 

## Overview

**Frontend**: React-based user interface with Tailwind CSS styling.
**Backend**: Flask-based API for market data and predictions.
This service provides APIs for:
- User authentication (signup/signin)
- Price predictions for market items
- Model information and statistics
- Protected routes with JWT authentication

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- MongoDB
- pip (Python package manager)

## Environment Setup

Clone the repository:
```bash
git clone https://github.com/Arshad9748/Market-Metrics .git
```
 
**Frontend**:
1. Navigate to the frontend directory:
```bash
cd frontend
```
2. Install dependencies:
```bash
npm install
```

**Backend**:
1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```env
MONGO_URI=mongodb://localhost:27017/
SECRET_KEY=your_jwt_secret_key_here
```


## Project Structure

```
market-metrics/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── assets/          # Page components
│   │   ├── services/       # API service calls
│   │   └── styles/ 
│   ├── public/
│   ├── package.json
│   
```

```
metricsbackend/
├── app.py                  # Main application entry point
├── routes/
│   ├── auth_routes.py     # Authentication routes
│   └── model_routes.py    # Model prediction routes
├── predictors/
│   ├── price_prediction.py # Price prediction model
│   └── models/            # Trained model files
├── datasets/              # Training datasets
│   ├── annex1.csv        # Item and category mappings
│   ├── annex2.csv        # Sales data
│   ├── annex3.csv        # Wholesale prices
│   └── annex4.csv        # Loss rates
└── requirements.txt      # Project dependencies
```

## Database Setup

1. Ensure MongoDB is running on your system
2. The application will automatically create the required collections:
   - users
   - market_metrics

## Running the Application

**Frontend**:
1. Navigate to the `frontend` directory
```bash
cd frontend
```
2. Start the React development server:
```bash
npm run dev
```

**Backend**:

In a new terminal, navigate to the metricsbackend directory:
1. Ensure you're in the virtual environment:
```bash
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Start the Flask application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Documentation

Detailed API documentation can be found in `implementation.MD`. Here's a quick overview:

### Authentication Endpoints

1. **Signup**
   - POST `/signup`
   - Creates new user account

2. **Signin**
   - POST `/signin`
   - Authenticates user and returns JWT token

### Protected Endpoints

All these endpoints require JWT token in Authorization header:
`Authorization: Bearer <your_token>`

1. **Price Prediction**
   - POST `/api/predict-price`
   - Predicts retail price for items

2. **Model Information**
   - GET `/api/model-info`
   - Returns model features and valid categories/items

3. **Model Retraining**
   - POST `/api/retrain-model`
   - Retrains the prediction model

## Model Training

The price prediction model needs to be trained before making predictions:

1. Ensure all dataset files are in the `datasets/` directory
2. Run the training script:
```bash
python -c "from predictors.price_prediction import PricePredictionModel; model = PricePredictionModel(); model.train()"
```

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 500: Server Error

All responses follow the format:
```json
{
    "success": boolean,
    "error": string (optional),
    "data": object (optional)
}
```

## Development

### Adding New Routes
1. Create new route file in `routes/`
2. Import and initialize in `app.py`
3. Update documentation

### Modifying the Model
1. Update `predictors/price_prediction.py`
2. Retrain model using the API
3. Test predictions

## Testing

Run tests using:
```bash
python -m pytest
```

## Security Notes

1. Never commit `.env` file
2. Keep JWT secret key secure
3. Use HTTPS in production
4. Store tokens securely (HTTP-only cookies)

## Troubleshooting

1. **MongoDB Connection Issues**
   - Verify MongoDB is running
   - Check MONGO_URI in .env

2. **Model Prediction Errors**
   - Ensure model is trained
   - Verify input data format
   - Check logs for details

3. **Authentication Issues**
   - Verify token format
   - Check token expiration
   - Ensure secret key matches


## License

This project is licensed under the MIT License — see the [LICENSE](./LICENSE) file for details.

## Copyright

© 2025 Arshad Murtaza Ahmed, Subinoy Khatua, Sayan Malakar, Praveen Kumar, Rimi Das. All contributors retain their rights under the MIT License.


