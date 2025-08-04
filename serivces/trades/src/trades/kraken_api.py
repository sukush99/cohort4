from pydantic import BaseModel
from typing import List
import json
from websocket import create_connection

from loguru import logger


class Trade(BaseModel):
    product_id: str
    price: float
    quantity: float
    timestamp: str


    def to_dict(self) -> dict:
        return self.model_dump()


class KrakenAPI:

    URL = 'wss://ws.kraken.com/v2'

    def __init__(self,
                 product_ids: list[str]):
        # Initialize the Kraken API client here
        self.product_ids = product_ids
        self._ws_client = create_connection(self.URL)
        self._subscribe(self.product_ids)

    def get_trades(self) -> list[Trade]:
        
        data = self._ws_client.recv()

        if 'heartbeat' in data:
            logger.debug("Heartbeat received, no trades available.")
            return []
        
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            return []
        
        try:
            trades_data = data['data']
        except KeyError as e:
            logger.error(f"KeyError: {e} in data: {data}")
            return []
        

        # trades = []
        # for trade in trades_data:
        #     try:
        #         trades.append(Trade(
        #             product_id=trade['symbol'],
        #             price=float(trade['price']),
        #             quantity=float(trade['qty']),
        #             timestamp=trade['timestamp']
        #         ))
        #     except (KeyError, ValueError) as e:
        #         logger.error(f"Error processing trade data: {e} in trade: {trade}")

        #using list comprehension for better performance
        trades = [
            Trade(
                product_id=trade['symbol'],
                price=float(trade['price']),
                quantity=float(trade['qty']),
                timestamp=trade['timestamp']
            ) for trade in trades_data if 'symbol' in trade and 'price' in trade and 'qty' in trade and 'timestamp' in trade
        ]

        # breakpoint()  # For debugging purposes
        return trades

    def _subscribe(self, product_ids: list[str]):
        """
        Subscribe to the Kraken WebSocket API for the specified product IDs.
        
        Args:
            product_ids (list[str]): List of product IDs to subscribe to.
        """
        self._ws_client.send(
            json.dumps(
                {
                    'method': 'subscribe',
                    'params': {
                        'channel': 'trade',
                        'symbol': product_ids,
                        'snapshot': False,
                    }
                }
            )
        )
        # breakpoint()
        for _ in self.product_ids:
            _ = self._ws_client.recv()
            _ = self._ws_client.recv()
