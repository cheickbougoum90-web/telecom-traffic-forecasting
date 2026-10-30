# Telecom Traffic Forecasting (time series)

Data science project: forecast mobile network Internet activity with ARIMA/SARIMA, Prophet, XGBoost
and LSTM, then serve the best model through a containerized FastAPI service.

> French version: [README.md](README.md)

## Problem
How can we anticipate mobile network load to plan and size capacity?

## Data
Telecom Italia Big Data Challenge (Milan, Nov to Dec 2013), see [docs/donnees.md](docs/donnees.md).

## Methodology
1. Exploration (trend, daily and weekly seasonality, outliers)
2. Baseline (seasonal naive)
3. SARIMA, Prophet, XGBoost, LSTM
4. Time-aware validation and comparison (MAE, RMSE, MAPE)
5. FastAPI and Docker

## Results
To be completed.

## Run
```
pip install -r requirements.txt
pytest
uvicorn src.api.main:app --reload
```
