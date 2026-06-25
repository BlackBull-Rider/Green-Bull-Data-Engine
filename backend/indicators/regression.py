import numpy as np
from typing import Dict, Any
from backend.indicators.math_utils import enforce_writeable_float_array_fast

def compile_advanced_regression_matrix(close_array: np.ndarray, period: int = 20) -> Dict[str, Any]:
    """
    [Green Bull Rider V6 - Layer 1: regression]
    Computes rolling linear regression lines, forecast pricing, and institutional 
    displacement bands via RMSE (Root Mean Squared Error) boundary channels.
    """
    closes = enforce_writeable_float_array_fast(close_array)
    n = closes.shape[0]
    
    if n < period:
        return {"status": "FAILED_COMPILATION", "reason": "Insufficient data elements for regression profiling."}
        
    # Setup X coordinates (0 to period-1)
    x = np.arange(period, dtype=float)
    x_mean = np.mean(x)
    x_dev = x - x_mean
    x_var_sum = np.sum(x_dev ** 2)
    if x_var_sum == 0:
        x_var_sum = 1e-7
        
    # Vectors to store rolling calculations
    forecast_line = np.empty_like(closes)
    forecast_line[:] = np.nan
    rmse_line = np.empty_like(closes)
    rmse_line[:] = np.nan
    
    # Fast rolling matrix window iteration
    for i in range(period - 1, n):
        y = closes[i - period + 1 : i + 1]
        y_mean = np.mean(y)
        
        # Calculate Slope (m) and Intercept (c) -> y = mx + c
        slope = np.sum(x_dev * (y - y_mean)) / x_var_sum
        intercept = y_mean - (slope * x_mean)
        
        # Fair Value Forecast at the current bar index (x = period - 1)
        current_forecast = (slope * (period - 1)) + intercept
        forecast_line[i] = current_forecast
        
        # Calculate Root Mean Squared Error (RMSE) for the current window
        fitted_values = (slope * x) + intercept
        rmse = np.sqrt(np.mean((y - fitted_values) ** 2))
        rmse_line[i] = rmse if rmse > 0 else 1e-7

    # Establish Institutional Displacement Bands
    upper_displacement_band = forecast_line + (2.0 * rmse_line)
    lower_displacement_band = forecast_line - (2.0 * rmse_line)
    
    idx = -1
    c_close = float(closes[idx])
    c_forecast = float(forecast_line[idx])
    c_rmse = float(rmse_line[idx])
    
    # Calculate current price displacement percentage from fair value
    displacement_pct = ((c_close - c_forecast) / c_forecast) * 100.0
    
    return {
        "engine": "Advanced Regression Core Cluster v1.0_Pro",
        "fair_value_forecast": float(round(c_forecast, 2)),
        "root_mean_squared_error_rmse": float(round(c_rmse, 2)),
        "displacement_channels": {
            "upper_band_limit": float(round(upper_displacement_band[idx], 2)),
            "lower_band_limit": float(round(lower_displacement_band[idx], 2))
        },
        "price_displacement_pct": float(round(displacement_pct, 2)),
        "equilibrium_state": "OVEREXTENDED_ABOVE" if c_close > upper_displacement_band[idx] else (
            "OVEREXTENDED_BELOW" if c_close < lower_displacement_band[idx] else "WITHIN_EQUILIBRIUM"
        )
    }
