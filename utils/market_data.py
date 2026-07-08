def get_economic_events():
    """Return sample economic events."""
    return [
        {'time': '08:30 EST', 'currency': 'USD', 'event': 'CPI Data', 'impact': 'High', 'forecast': '3.1%'},
        {'time': '09:15 EST', 'currency': 'EUR', 'event': 'ECB Rate Decision', 'impact': 'High', 'forecast': '4.00%'},
        {'time': '10:00 EST', 'currency': 'GBP', 'event': 'BOE Minutes', 'impact': 'Medium', 'forecast': '-'},
        {'time': '12:30 EST', 'currency': 'USD', 'event': 'Unemployment Claims', 'impact': 'Medium', 'forecast': '220K'},
        {'time': '14:00 EST', 'currency': 'USD', 'event': 'Consumer Confidence', 'impact': 'Low', 'forecast': '68.5'},
    ]

def get_market_sentiment():
    """Return sample market sentiment data."""
    return {
        'EUR/USD': {'sentiment': 'Bullish', 'strength': 7},
        'GBP/USD': {'sentiment': 'Bearish', 'strength': 6},
        'USD/JPY': {'sentiment': 'Bullish', 'strength': 5},
        'AUD/USD': {'sentiment': 'Neutral', 'strength': 4},
        'XAU/USD': {'sentiment': 'Bullish', 'strength': 8},
    }
