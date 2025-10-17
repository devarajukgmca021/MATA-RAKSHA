from web3 import Web3
from solcx import compile_source, install_solc
import json
import os

class BlockchainManager:
    def __init__(self, ganache_url='http://127.0.0.1:8545'):
        self.w3 = Web3(Web3.HTTPProvider(ganache_url))
        self.contract = None
        self.contract_address = None
        self.account = None
        
        if self.w3.is_connected():
            self.account = self.w3.eth.accounts[0]
        else:
            print("Warning: Not connected to Ganache")
    
    def compile_contract(self):
        contract_path = 'contracts/VotingContract.sol'
        
        with open(contract_path, 'r') as file:
            contract_source = file.read()
        
        try:
            from solcx import get_installed_solc_versions
            if '0.8.0' not in [str(v) for v in get_installed_solc_versions()]:
                install_solc('0.8.0')
        except Exception as e:
            install_solc('0.8.0')
        
        from solcx import set_solc_version
        set_solc_version('0.8.0')
        
        compiled_sol = compile_source(contract_source, output_values=['abi', 'bin'], solc_version='0.8.0')
        contract_id, contract_interface = compiled_sol.popitem()
        
        return contract_interface['abi'], contract_interface['bin']
    
    def deploy_contract(self):
        abi, bytecode = self.compile_contract()
        
        VotingContract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        
        tx_hash = VotingContract.constructor().transact({'from': self.account})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        self.contract_address = tx_receipt.contractAddress
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=abi)
        
        return self.contract_address
    
    def load_contract(self, contract_address):
        abi, _ = self.compile_contract()
        self.contract_address = contract_address
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)
    
    def create_election(self, name, district):
        tx_hash = self.contract.functions.createElection(name, district).transact({'from': self.account})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        election_count = self.contract.functions.electionCount().call()
        return election_count
    
    def add_candidate(self, election_id, candidate_name, party_name):
        tx_hash = self.contract.functions.addCandidate(election_id, candidate_name, party_name).transact({'from': self.account})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
    
    def register_voter_on_blockchain(self, election_id, voter_address):
        tx_hash = self.contract.functions.registerVoter(election_id, voter_address).transact({'from': self.account})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
    
    def is_voter_registered(self, election_id, voter_address):
        return self.contract.functions.isRegistered(election_id, voter_address).call()
    
    def cast_vote(self, election_id, candidate_id, voter_private_key):
        voter_account = self.w3.eth.account.from_key(voter_private_key)
        voter_address = voter_account.address
        
        nonce = self.w3.eth.get_transaction_count(voter_address)
        
        transaction = self.contract.functions.vote(election_id, candidate_id).build_transaction({
            'from': voter_address,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, voter_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return receipt.transactionHash.hex()
    
    def get_candidate(self, election_id, candidate_id):
        return self.contract.functions.getCandidate(election_id, candidate_id).call()
    
    def get_candidate_count(self, election_id):
        return self.contract.functions.getCandidateCount(election_id).call()
    
    def has_voted(self, election_id, voter_address):
        return self.contract.functions.hasVoted(election_id, voter_address).call()
    
    def finalize_election(self, election_id):
        tx_hash = self.contract.functions.finalizeElection(election_id).transact({'from': self.account})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
    
    def get_winner(self, election_id):
        return self.contract.functions.getWinner(election_id).call()
    
    def get_all_results(self, election_id):
        candidate_count = self.get_candidate_count(election_id)
        results = []
        
        for i in range(1, candidate_count + 1):
            candidate_data = self.get_candidate(election_id, i)
            results.append({
                'id': candidate_data[0],
                'name': candidate_data[1],
                'party': candidate_data[2],
                'votes': candidate_data[3]
            })
        
        return results
    
    def create_voter_account(self):
        account = self.w3.eth.account.create()
        return account.address, account.key.hex()
    
    def fund_voter_account(self, voter_address, amount_eth=0.1):
        tx_hash = self.w3.eth.send_transaction({
            'from': self.account,
            'to': voter_address,
            'value': self.w3.to_wei(amount_eth, 'ether')
        })
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
