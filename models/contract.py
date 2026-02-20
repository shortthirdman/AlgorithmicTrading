import json
import datetime

from typing import Optional
from dataclasses import dataclass, field

from core.broker_client import BrokerClient
from core.utils import get_ny_timestamp

@dataclass
class Contract:
    underlying: str
    symbol: str
    contract_type: str
    dte: Optional[float] = None
    strike: Optional[float] = None
    delta: Optional[float] = None
    bid_price: Optional[float] = None
    ask_price: Optional[float] = None
    last_price: Optional[float] = None
    oi: Optional[int] = None
    underlying_price: Optional[float] = None
    client: Optional["BrokerClient"] = field(default=None, repr=False, compare=False)

    def __post_init__(self):
        if self.client:
            self.update()

    @classmethod
    def from_contract(cls, contract, client=None) -> "Contract":
        return cls(
            underlying = contract.underlying_symbol,
            symbol = contract.symbol,
            contract_type = contract.type.title().lower(),
            oi = float(contract.open_interest) if contract.open_interest is not None else None,
            dte = (contract.expiration_date - datetime.date.today()).days,
            strike = contract.strike_price,
            client = client
        )

    @classmethod
    def from_contract_snapshot(cls, contract, snapshot) -> "Contract":
        if not snapshot:
            raise ValueError(f"Snapshot data is required to create a Contract from a snapshot for symbol {contract.symbol}.")
        return cls(
            underlying = contract.underlying_symbol,
            symbol = contract.symbol,
            contract_type = contract.type.title().lower(),
            oi = float(contract.open_interest) if contract.open_interest is not None else None,
            dte = (contract.expiration_date - datetime.date.today()).days,
            strike = contract.strike_price,
            delta = snapshot.greeks.delta if hasattr(snapshot, 'greeks') and snapshot.greeks else None,
            bid_price = snapshot.latest_quote.bid_price if hasattr(snapshot, 'latest_quote') and snapshot.latest_quote else None,
            ask_price = snapshot.latest_quote.ask_price if hasattr(snapshot, 'latest_quote') and snapshot.latest_quote else None,
            last_price = snapshot.latest_trade.price if hasattr(snapshot, 'latest_trade') and snapshot.latest_trade else None
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Contract":
        return cls(**data)

    def update(self):
        if not self.client:
            raise ValueError("Cannot update Contract without a client.")
        snapshot = self.client.get_option_snapshot(self.symbol)
        if snapshot and self.symbol in snapshot:
            data = snapshot[self.symbol]
            if hasattr(data, 'greeks') and data.greeks:
                self.delta = data.greeks.delta
            if hasattr(data, 'latest_quote') and data.latest_quote:
                self.bid_price = data.latest_quote.bid_price
                self.ask_price = data.latest_quote.ask_price
                self.last_price = getattr(data.latest_trade, "price", None)
            if hasattr(data, 'latest_trade') and data.latest_trade:
                self.last_price = data.latest_trade.price

    def to_dict(self):
        return {
            "underlying": self.underlying,
            "symbol": self.symbol,
            "contract_type": self.contract_type,
            "dte": self.dte,
            "strike": self.strike,
            "delta": self.delta,
            "bid_price": self.bid_price,
            "ask_price": self.ask_price,
            "last_price": self.last_price,
            "oi": self.oi,
            "underlying_price": self.underlying_price,
        }

    @staticmethod
    def save_to_json(contracts: list["Contract"], filepath: str):
        payload = {
            "timestamp": get_ny_timestamp(),
            "contracts": [c.to_dict() for c in contracts]
        }
        with open(filepath, "w") as f:
            json.dump(payload, f, indent=2)

    @staticmethod
    def load_from_json(filepath: str):
        with open(filepath, "r") as f:
            payload = json.load(f)
        return [Contract.from_dict(d) for d in payload["contracts"]]