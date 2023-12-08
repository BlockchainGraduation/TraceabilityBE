import json
import logging
import os.path

from django.conf import settings

from blockchain_web3.provider import Web3Provider

logger = logging.getLogger(__name__)


class TraceabilityProvider(Web3Provider):
    def __init__(self):
        path_abi = os.path.join(os.getcwd(), "abi/traceability.txt")
        with open(path_abi, "r", encoding="utf-8") as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(settings.WEB3_PROVIDER, settings.ADDRESS_CONTRACT_TRACEBILITY)
        self.chain_id = settings.CHAIN_ID
        self.contract = self.w3.eth.contract(
            address=settings.ADDRESS_CONTRACT_TRACEBILITY, abi=factory_abi
        )

    def buy_product(self, product_id, id_trans, buyer, quantity):
        function = self.contract.functions.buyItemOnMarketplace(
            product_id, id_trans, buyer, quantity
        )
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def get_transaction_by_id(self, trans_id):
        return self.contract.functions.get_transaction_by_id(trans_id).call()

    def get_seek_an_origin(self, product_id):
        return self.contract.functions.seekAnOrigin(product_id).call()

    def update_status_transaction(self, trans_id: str, status: int):
        function = self.contract.functions.updateStatusTransaction(trans_id, status)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash
