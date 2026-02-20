import re
import pytz
from datetime import datetime

def parse_option_symbol(symbol):
    match = re.match(r'^([A-Za-z]+)(\d{6})([PC])(\d{8})$', symbol)
    if match:
        underlying = match.group(1)
        option_type = match.group(3)
        strike_raw = match.group(4)
        strike_price = int(strike_raw) / 1000.0
        return underlying, option_type, strike_price
    else:
        raise ValueError(f"Invalid option symbol format: {symbol}")

def get_ny_timestamp():
    ny_tz = pytz.timezone("America/New_York")
    ny_time = datetime.now(ny_tz)
    return ny_time.isoformat()