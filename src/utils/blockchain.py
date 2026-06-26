"""from web3 import Web3
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
        
        #compiled_sol = compile_source(contract_source, output_values=['abi', 'bin'], solc_version='0.8.0')
        compiled_sol = compile_source(contract_source, output_values=['abi', 'bin'])
        contract_id, contract_interface = compiled_sol.popitem()
        
        return contract_interface['abi'], contract_interface['bin']
    
    def deploy_contract(self):
        abi, bytecode = self.compile_contract()
        
        VotingContract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        
        #tx_hash = VotingContract.constructor().transact({'from': self.account})
        tx_hash = VotingContract.constructor().transact({
            'from': self.account,
            'gas': 3000000,
            'gasPrice': self.w3.to_wei('1', 'gwei')
        })

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

    def is_connected(self) -> bool:
        try:
            return bool(self.w3 and self.w3.is_connected())
        except Exception:
            return False

    def get_transaction_receipt(self, tx_hash: str):
        try:
            rcpt = self.w3.eth.get_transaction_receipt(tx_hash)
            return {
                "blockNumber": rcpt.blockNumber,
                "status": rcpt.status,
                "from": rcpt["from"],
                "to": rcpt["to"],
                "gasUsed": rcpt.gasUsed
            }
        except Exception:
            return None

from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version
import json
import os

class BlockchainManager:
    def __init__(self, ganache_url='http://127.0.0.1:8545'):
        self.w3 = Web3(Web3.HTTPProvider(ganache_url))
        self.contract = None
        self.contract_address = None
        self.account = None

        if self.w3.is_connected():
            print("Connected to Ganache")
            self.account = self.w3.eth.accounts[0]
        else:
            raise Exception("❌ Not connected to Ganache")

        # Auto-load contract if saved earlier
        if os.path.exists("contract_address.txt") and os.path.exists("contract_abi.json"):
            try:
                with open("contract_address.txt", "r") as f:
                    address = f.read().strip()
                with open("contract_abi.json", "r") as f:
                    abi = json.load(f)

                self.contract_address = address
                self.contract = self.w3.eth.contract(address=address, abi=abi)
                print(f"Loaded existing contract at: {address}")
            except Exception:
                print("⚠ Could not load existing contract")

    # -----------------------------------------------------------
    #  Compile Solidity Contract
    # -----------------------------------------------------------
    def compile_contract(self):
        contract_path = 'contracts/VotingContract.sol'

        if not os.path.exists(contract_path):
            raise Exception("❌ Missing: contracts/VotingContract.sol")

        with open(contract_path, 'r') as file:
            contract_source = file.read()

        # Install compiler version 0.8.0 if missing
        try:
            from solcx import get_installed_solc_versions
            if "0.8.0" not in [str(v) for v in get_installed_solc_versions()]:
                install_solc("0.8.0")
        except:
            install_solc("0.8.0")

        set_solc_version("0.8.0")

        compiled_sol = compile_source(
            contract_source,
            output_values=["abi", "bin"]
        )

        contract_id, contract_interface = compiled_sol.popitem()
        abi = contract_interface["abi"]
        bytecode = contract_interface["bin"]

        # Save ABI for future runs
        with open("contract_abi.json", "w") as f:
            json.dump(abi, f)

        return abi, bytecode

    # -----------------------------------------------------------
    #  Deploy Smart Contract
    # -----------------------------------------------------------
    def deploy_contract(self):
        abi, bytecode = self.compile_contract()

        VotingContract = self.w3.eth.contract(abi=abi, bytecode=bytecode)

        tx_hash = VotingContract.constructor().transact({
            'from': self.account,
            'gas': 3000000,
            'gasPrice': self.w3.to_wei("1", "gwei")
        })

        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        self.contract_address = tx_receipt.contractAddress
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=abi
        )

        # Save contract address
        with open("contract_address.txt", "w") as f:
            f.write(self.contract_address)

        print(f"Contract deployed at: {self.contract_address}")
        return self.contract_address

    # -----------------------------------------------------------
    #  Load Contract from Address
    # -----------------------------------------------------------
    def load_contract(self, contract_address):
        if not os.path.exists("contract_abi.json"):
            raise Exception("❌ Missing contract ABI file")

        with open("contract_abi.json", "r") as f:
            abi = json.load(f)

        self.contract_address = contract_address
        self.contract = self.w3.eth.contract(address=contract_address, abi=abi)

        print(f"Loaded contract at {contract_address}")

    # -----------------------------------------------------------
    #  Election Functions
    # -----------------------------------------------------------
    def create_election(self, name, district):
        self._check_contract()
        tx_hash = self.contract.functions.createElection(name, district).transact({
            'from': self.account
        })
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return self.contract.functions.electionCount().call()

    def add_candidate(self, election_id, candidate_name, party_name):
        self._check_contract()
        tx_hash = self.contract.functions.addCandidate(election_id, candidate_name, party_name).transact({
            'from': self.account
        })
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def register_voter_on_blockchain(self, election_id, voter_address):
        self._check_contract()
        tx_hash = self.contract.functions.registerVoter(election_id, voter_address).transact({
            'from': self.account
        })
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)

    # -----------------------------------------------------------
    #  Voting Functions
    # -----------------------------------------------------------
    def cast_vote(self, election_id, candidate_id, voter_private_key):
        self._check_contract()

        voter_account = self.w3.eth.account.from_key(voter_private_key)
        voter_address = voter_account.address

        # Auto-fund voter if empty
        if self.w3.eth.get_balance(voter_address) == 0:
            self.fund_voter_account(voter_address, 0.1)

        nonce = self.w3.eth.get_transaction_count(voter_address)

        txn = self.contract.functions.vote(
            election_id, candidate_id
        ).build_transaction({
            'from': voter_address,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_txn = self.w3.eth.account.sign_transaction(txn, voter_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return receipt.transactionHash.hex()

    # -----------------------------------------------------------
    #  Read Data
    # -----------------------------------------------------------
    def get_candidate(self, election_id, candidate_id):
        self._check_contract()
        return self.contract.functions.getCandidate(election_id, candidate_id).call()

    def get_candidate_count(self, election_id):
        self._check_contract()
        return self.contract.functions.getCandidateCount(election_id).call()

    def has_voted(self, election_id, voter_address):
        self._check_contract()
        return self.contract.functions.hasVoted(election_id, voter_address).call()

    def finalize_election(self, election_id):
        self._check_contract()
        tx_hash = self.contract.functions.finalizeElection(election_id).transact({
            'from': self.account
        })
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def get_winner(self, election_id):
        self._check_contract()
        return self.contract.functions.getWinner(election_id).call()

    def get_all_results(self, election_id):
        count = self.get_candidate_count(election_id)
        results = []
        for i in range(1, count + 1):
            c = self.get_candidate(election_id, i)
            results.append({
                "id": c[0],
                "name": c[1],
                "party": c[2],
                "votes": c[3]
            })
        return results

    # -----------------------------------------------------------
    #  Wallet Functions
    # -----------------------------------------------------------
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

    # -----------------------------------------------------------
    #  Utility
    # -----------------------------------------------------------
    def is_connected(self):
        return bool(self.w3 and self.w3.is_connected())

    def get_transaction_receipt(self, tx_hash):
        try:
            rcpt = self.w3.eth.get_transaction_receipt(tx_hash)
            return {
                "blockNumber": rcpt.blockNumber,
                "status": rcpt.status,
                "from": rcpt["from"],
                "to": rcpt["to"],
                "gasUsed": rcpt.gasUsed
            }
        except:
            return None

    def _check_contract(self):
        if self.contract is None:
            raise Exception("❌ Contract not loaded. Deploy or load contract first.")"""
from web3 import Web3
from solcx import compile_source, install_solc, set_solc_version
import json
import os


class BlockchainManager:
    def __init__(self, ganache_url='http://127.0.0.1:8545'):
        print("🔗 Connecting to Ganache…")

        self.w3 = Web3(Web3.HTTPProvider(ganache_url))
        self.contract = None
        self.contract_address = None

        if not self.w3.is_connected():
            raise Exception("❌ Could not connect to Ganache. Start Ganache first.")

        print("✅ Connected to Ganache")
        self.account = self.w3.eth.accounts[0]

        # Try loading existing deployed contract
        self._auto_load_or_deploy()


    # =====================================================================
    # AUTO DEPLOY / AUTO LOAD LOGIC
    # =====================================================================
    def _auto_load_or_deploy(self):
        """
        Load contract if data exists.
        If loading fails → auto deploy new contract.
        """
        addr_path = "contract_address.txt"
        abi_path = "contract_abi.json"

        if os.path.exists(addr_path) and os.path.exists(abi_path):
            try:
                with open(addr_path, "r") as f:
                    address = f.read().strip()
                with open(abi_path, "r") as f:
                    abi = json.load(f)

                # Validate address
                if not self.w3.is_address(address):
                    raise Exception("Invalid address")

                # Load contract
                self.contract_address = address
                self.contract = self.w3.eth.contract(address=address, abi=abi)

                # Test call to ensure contract exists in chain
                self.contract.functions.electionCount().call()

                print(f"📌 Loaded existing contract at {address}")
                return

            except Exception as e:
                print("⚠ Contract load failed → Will deploy new contract.")
                print("Reason:", e)

        # Deploy new contract
        self.deploy_contract()


    # =====================================================================
    # COMPILATION
    # =====================================================================
    def compile_contract(self):
        path = "contracts/VotingContract.sol"
        if not os.path.exists(path):
            raise Exception("❌ Missing: contracts/VotingContract.sol")

        with open(path, "r") as file:
            source = file.read()

        try:
            from solcx import get_installed_solc_versions
            if "0.8.0" not in [str(v) for v in get_installed_solc_versions()]:
                install_solc("0.8.0")
        except:
            install_solc("0.8.0")

        set_solc_version("0.8.0")

        compiled = compile_source(source, output_values=["abi", "bin"])
        _, interface = compiled.popitem()

        abi = interface["abi"]
        bytecode = interface["bin"]

        # Save ABI
        with open("contract_abi.json", "w") as f:
            json.dump(abi, f)

        return abi, bytecode


    # =====================================================================
    # DEPLOYMENT
    # =====================================================================
    def deploy_contract(self):
        print("🚀 Deploying new VotingContract…")

        abi, bytecode = self.compile_contract()

        Contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)
        tx_hash = Contract.constructor().transact({
            'from': self.account,
            'gas': 4000000
        })

        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        self.contract_address = receipt.contractAddress
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=abi)

        # Save address
        with open("contract_address.txt", "w") as f:
            f.write(self.contract_address)

        print(f"🎉 Contract deployed successfully at: {self.contract_address}")
        return self.contract_address


    # =====================================================================
    # UTIL
    # =====================================================================
    def _check_contract(self):
        if self.contract is None:
            raise Exception("❌ No contract loaded or deployed.")

    def is_connected(self):
        return self.w3.is_connected()


    # =====================================================================
    # WALLET FUNCTIONS
    # =====================================================================
    def create_voter_account(self):
        wallet = self.w3.eth.account.create()
        return wallet.address, wallet.key.hex()

    def fund_voter_account(self, address, amount_eth=0.1):
        tx = self.w3.eth.send_transaction({
            'from': self.account,
            'to': address,
            'value': self.w3.to_wei(amount_eth, 'ether')
        })
        self.w3.eth.wait_for_transaction_receipt(tx)


    # =====================================================================
    # ELECTION CONTROL
    # =====================================================================
    def create_election(self, name, district):
        self._check_contract()
        tx = self.contract.functions.createElection(name, district).transact({
            'from': self.account
        })
        self.w3.eth.wait_for_transaction_receipt(tx)
        return self.contract.functions.electionCount().call()

    def add_candidate(self, election_id, candidate, party):
        self._check_contract()
        tx = self.contract.functions.addCandidate(election_id, candidate, party).transact({
            'from': self.account
        })
        return self.w3.eth.wait_for_transaction_receipt(tx)

    def register_voter_on_blockchain(self, election_id, voter_address):
        self._check_contract()
        tx = self.contract.functions.registerVoter(election_id, voter_address).transact({
            'from': self.account
        })
        return self.w3.eth.wait_for_transaction_receipt(tx)


    # =====================================================================
    # VOTING
    # =====================================================================
    def cast_vote(self, election_id, candidate_id, voter_private_key):
        self._check_contract()

        acct = self.w3.eth.account.from_key(voter_private_key)
        voter_address = acct.address

        # auto fund
        if self.w3.eth.get_balance(voter_address) == 0:
            self.fund_voter_account(voter_address)

        nonce = self.w3.eth.get_transaction_count(voter_address)

        txn = self.contract.functions.vote(election_id, candidate_id).build_transaction({
            'from': voter_address,
            'nonce': nonce,
            'gas': 250000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed = self.w3.eth.account.sign_transaction(txn, voter_private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        rcpt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return rcpt.transactionHash.hex()


    # =====================================================================
    # READ DATA
    # =====================================================================
    def get_candidate(self, election_id, candidate_id):
        self._check_contract()
        return self.contract.functions.getCandidate(election_id, candidate_id).call()

    def get_candidate_count(self, election_id):
        self._check_contract()
        return self.contract.functions.getCandidateCount(election_id).call()

    def has_voted(self, election_id, voter_addr):
        self._check_contract()
        return self.contract.functions.hasVoted(election_id, voter_addr).call()

    def finalize_election(self, election_id):
        self._check_contract()
        tx = self.contract.functions.finalizeElection(election_id).transact({
            'from': self.account
        })
        return self.w3.eth.wait_for_transaction_receipt(tx)

    def get_winner(self, election_id):
        self._check_contract()
        return self.contract.functions.getWinner(election_id).call()

    def get_all_results(self, election_id):
        count = self.get_candidate_count(election_id)
        results = []
        for i in range(1, count + 1):
            cid, name, party, votes = self.get_candidate(election_id, i)
            results.append((
                cid,
                name,
                party,
                votes
            ))
        return results



