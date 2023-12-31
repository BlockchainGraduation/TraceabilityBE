import json

from .provider import Web3Provider
from django.conf import settings


class ProductProvider(Web3Provider):
    def __init__(self):
        with open("./abi/product.txt", "r", encoding="utf-8") as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(
            settings.WEB3_PROVIDER, settings.ADDRESS_CONTRACT_PRODUCT_MANAGER
        )
        self.chain_id = settings.CHAIN_ID
        self.contract = self.w3.eth.contract(
            address=settings.ADDRESS_CONTRACT_PRODUCT_MANAGER, abi=factory_abi
        )

    def create_product(
        self,
        product_id,
        product_type,
        price,
        quantity,
        status,
        owner,
        hash_info,
        trans_id=None,
    ):
        function = self.contract.functions.create(
            product_id,
            product_type,
            price,
            quantity,
            trans_id,
            status,
            owner,
            hash_info,
        )
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def update_product(self, product_id, price, quantity, status, hash_info):
        function = self.contract.functions.update(
            product_id, price, quantity, status, hash_info
        )
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def get_product_by_id(self, product_id):
        return self.contract.functions.readOneProduct(product_id).call()

    def get_list_type_product(self, product_id: str):
        return self.contract.functions.get_list_type_product(product_id).call()
