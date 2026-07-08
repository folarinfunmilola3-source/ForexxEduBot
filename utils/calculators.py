def calculate_position_size(balance, risk_pct, stop_loss_pips):
    """Calculate the optimal position size."""
    risk_amount = balance * (risk_pct / 100)
    pip_value = 10  # Standard lot pip value in USD (for USD pairs)
    lot_size = risk_amount / (stop_loss_pips * pip_value)
    return {
        'risk_amount': risk_amount,
        'lot_size': round(lot_size, 2)
    }

def calculate_pip_value(pair, lot_size):
    """Calculate pip value for a currency pair."""
    # Simplified calculation
    pip_value = 10 * lot_size  # Standard calculation for USD pairs
    return {
        'pip_value': pip_value
    }

def calculate_risk_reward(entry, stop, take):
    """Calculate risk-reward ratio."""
    risk = abs(entry - stop)
    reward = abs(take - entry)
    ratio = round(reward / risk, 2) if risk > 0 else 0
    return {
        'risk': round(risk, 4),
        'reward': round(reward, 4),
        'ratio': ratio
    }

def calculate_pivot_points(high, low, close):
    """Calculate daily pivot points."""
    pivot = (high + low + close) / 3
    r1 = (2 * pivot) - low
    r2 = pivot + (high - low)
    r3 = high + 2 * (pivot - low)
    s1 = (2 * pivot) - high
    s2 = pivot - (high - low)
    s3 = low - 2 * (high - pivot)
    
    return {
        'pivot': round(pivot, 4),
        'r1': round(r1, 4),
        'r2': round(r2, 4),
        'r3': round(r3, 4),
        's1': round(s1, 4),
        's2': round(s2, 4),
        's3': round(s3, 4)
    }
