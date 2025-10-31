from aquarius.graphql import get_number_orders_price
from aquarius.events.util import make_did, get_dt_factory, update_did_state, get_erc20_contract, get_nft_contract

class OrderStartedProcessor:

    def __init__(self, token_address, es_instance, last_sync_block, chain_id):
        self.did = make_did(token_address, chain_id)
        self.chain_id = chain_id
        self.es_instance = es_instance
        self.token_address = token_address
        self.last_sync_block = last_sync_block
        try:
            self.asset = self.es_instance.read(self.did)
        except Exception:
            logger.debug(f'Asset {self.did} is missing from ES.')
            self.asset = None

    def process(self):
        if not self.asset:
            return
        logger.debug(f'Retrieving number of orders for {self.token_address}.')
        number_orders, price = get_number_orders_price(self.token_address, self.last_sync_block, self.chain_id)
        self.asset['stats']['orders'] = number_orders
        self.asset['stats']['price'] = price
        logger.debug(f'Updating number of orders to {number_orders} for {self.did}.')
        self.es_instance.update(self.asset, self.did)
        return self.asset