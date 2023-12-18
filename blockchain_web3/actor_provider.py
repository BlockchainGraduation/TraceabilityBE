import json
import os.path
import uuid

from django.conf import settings

from blockchain_web3.provider import Web3Provider


class ActorProvider(Web3Provider):
    def __init__(self):
        path_abi = os.path.join(os.getcwd(), "abi/actor.txt")
        with open(path_abi, "r", encoding="utf-8") as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        # breakpoint()
        super().__init__(
            settings.WEB3_PROVIDER, settings.ADDRESS_CONTRACT_ACTOR_MANAGER
        )
        self.chain_id = 421614
        self.contract = self.w3.eth.contract(
            address=settings.ADDRESS_CONTRACT_ACTOR_MANAGER, abi=factory_abi
        )

    def create_actor(self, user_id: str, address, role, hash_info):
        # breakpoint()
        function = self.contract.functions.create(user_id, address, role, hash_info)
        return self.sign_and_send_transaction(function)

    def update_actor(self, user_id: str, hash_info: str):
        function = self.contract.functions.updateActorHashInfo(user_id, hash_info)

        return self.sign_and_send_transaction(function)

    def get_actor_by_id(self, user_id):
        return self.contract.functions.getActorById(user_id).call()

    def get_ids_by_role(self, role):
        return self.contract.functions.getIdsByRole(role).call()

    def deposited(self, user_id: str, amount: int):
        function = self.contract.functions.deposit(user_id, amount)
        return self.sign_and_send_transaction(function)

    def withdraw(self, user_id: str, amount: int):
        function = self.contract.functions.withdrawBalance(user_id, amount)
        return self.sign_and_send_transaction(function)


if __name__ == "__main__":
    actor_provider = ActorProvider()
    tx_hash = actor_provider.deposited(
        user_id="06678b94-30e8-474e-917c-84447ac4fc6b", amount=1000000
    )
    print(tx_hash)
