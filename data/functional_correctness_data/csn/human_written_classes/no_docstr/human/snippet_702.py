from aquarius.events.util import make_did, get_dt_factory, update_did_state, get_erc20_contract, get_nft_contract
from web3.logs import DISCARD

class TokenURIUpdatedProcessor:

    def __init__(self, event, web3, es_instance, chain_id):
        self.did = make_did(event.address, chain_id)
        self.es_instance = es_instance
        self.event = event
        self.web3 = web3
        try:
            self.asset = self.es_instance.read(self.did)
        except Exception:
            self.asset = None

    def process(self):
        if not self.asset:
            return
        erc721_contract = get_nft_contract(self.web3, self.event.address)
        receipt = self.web3.eth.get_transaction_receipt(self.event.transactionHash)
        event_decoded = erc721_contract.events.TokenURIUpdate().process_receipt(receipt, errors=DISCARD)[0]
        self.asset['nft']['tokenURI'] = event_decoded.args.tokenURI
        self.es_instance.update(self.asset, self.did)
        return self.asset