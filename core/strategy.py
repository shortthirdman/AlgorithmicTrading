from config.params import DELTA_MIN, DELTA_MAX, YIELD_MIN, YIELD_MAX, OPEN_INTEREST_MIN, SCORE_MIN

def filter_underlying(client, symbols, buying_power_limit):
    resp = client.get_stock_latest_trade(symbols)
    filtered_symbols = [symbol for symbol in resp if 100*resp[symbol].price <= buying_power_limit]
    return filtered_symbols

def filter_options(options, min_strike = 0):
    filtered_contracts = [contract for contract in options
                          if contract.delta
                          and abs(contract.delta) > DELTA_MIN
                          and abs(contract.delta) < DELTA_MAX
                          and (contract.bid_price / contract.strike) * (365 / (contract.dte + 1)) > YIELD_MIN
                          and (contract.bid_price / contract.strike) * (365 / (contract.dte + 1)) < YIELD_MAX
                          and contract.oi
                          and contract.oi > OPEN_INTEREST_MIN
                          and contract.strike >= min_strike]
    return filtered_contracts

def score_options(options):
    scores = [(1 - abs(p.delta)) * (250 / (p.dte + 5)) * (p.bid_price / p.strike) for p in options]
    return scores

def select_options(options, scores, n=None):
    filtered = [(option, score) for option, score in zip(options, scores) if score > SCORE_MIN]
    best_per_underlying = {}
    for option, score in filtered:
        underlying = option.underlying
        if (underlying not in best_per_underlying) or (score > best_per_underlying[underlying][1]):
            best_per_underlying[underlying] = (option, score)
    sorted_best = sorted(best_per_underlying.values(), key=lambda x: x[1], reverse=True)
    return [option for option, _ in sorted_best[:n]] if n else [option for option, _ in sorted_best]