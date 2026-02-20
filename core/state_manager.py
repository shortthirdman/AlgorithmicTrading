from .utils import parse_option_symbol
from alpaca.trading.enums import AssetClass

def calculate_risk(positions):
    risk = 0
    for p in positions:
        if p.asset_class == AssetClass.US_EQUITY:
            risk += float(p.avg_entry_price) * abs(int(p.qty))
        elif p.asset_class == AssetClass.US_OPTION:
            _, option_type, strike_price = parse_option_symbol(p.symbol)
            if option_type == 'P':
                risk += 100 * strike_price * abs(int(p.qty))
    return risk