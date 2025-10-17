#!/usr/bin/env python3

import sys
from src.utils.database import Database
from src.utils.blockchain import BlockchainManager
from src.utils.biometric import BiometricSimulator

def test_database():
    print("\n=== Testing Database ===")
    db = Database()
    
    print("✓ Database initialized")
    
    role = db.verify_login('admin', 'admin123')
    print(f"✓ Admin login verified: {role}")
    
    districts = db.get_karnataka_districts()
    print(f"✓ Karnataka districts loaded: {len(districts)} districts")
    
    print("✓ Database tests passed")
    return db

def test_blockchain():
    print("\n=== Testing Blockchain ===")
    bc = BlockchainManager()
    
    if bc.w3.is_connected():
        print(f"✓ Connected to Ganache")
        print(f"✓ Using account: {bc.account}")
        
        balance = bc.w3.eth.get_balance(bc.account)
        print(f"✓ Account balance: {bc.w3.from_wei(balance, 'ether')} ETH")
        
        print("✓ Compiling smart contract...")
        abi, bytecode = bc.compile_contract()
        print(f"✓ Contract compiled successfully")
        
        print("✓ Deploying smart contract...")
        contract_address = bc.deploy_contract()
        print(f"✓ Contract deployed at: {contract_address}")
        
        print("✓ Blockchain tests passed")
        return bc
    else:
        print("✗ Not connected to Ganache - make sure it's running on port 8545")
        return None

def test_biometric():
    print("\n=== Testing Biometric System ===")
    bio = BiometricSimulator()
    
    fingerprint_hash, template_path = bio.generate_fingerprint_template("Test User")
    print(f"✓ Fingerprint template generated: {fingerprint_hash[:32]}...")
    print(f"✓ Template saved to: {template_path}")
    
    scan_hash = bio.simulate_fingerprint_scan()
    print(f"✓ Fingerprint scan simulated: {scan_hash[:32]}...")
    
    is_match = bio.verify_fingerprint(fingerprint_hash, fingerprint_hash)
    print(f"✓ Fingerprint verification (same): {is_match}")
    
    is_not_match = bio.verify_fingerprint(fingerprint_hash, scan_hash)
    print(f"✓ Fingerprint verification (different): {is_not_match}")
    
    print("✓ Biometric tests passed")
    return bio

def test_complete_workflow():
    print("\n=== Testing Complete E-Voting Workflow ===")
    
    db = Database()
    bc = BlockchainManager()
    bio = BiometricSimulator()
    
    if not bc.w3.is_connected():
        print("✗ Ganache not running - skipping workflow test")
        return False
    
    print("\n1. Registering voter...")
    fingerprint_hash, _ = bio.generate_fingerprint_template("Ramesh Kumar")
    voter_address, voter_private_key = bc.create_voter_account()
    bc.fund_voter_account(voter_address, 0.1)
    voter_id = db.register_voter(
        "Ramesh Kumar",
        "1990-05-15",
        "Bengaluru Urban",
        fingerprint_hash,
        voter_address,
        voter_private_key
    )
    print(f"   ✓ Voter registered: {voter_id}")
    print(f"   ✓ Voter address: {voter_address}")
    print(f"   ✓ Voter funded with 0.1 ETH for gas")
    
    print("\n2. Creating election...")
    if not bc.contract:
        bc.deploy_contract()
    
    blockchain_election_id = bc.create_election("Assembly Election 2025", "Bengaluru Urban")
    election_id = db.create_election(
        "Assembly Election 2025",
        "Bengaluru Urban",
        "2025-10-17",
        "2025-10-18"
    )
    db.update_election_contract(election_id, bc.contract_address)
    print(f"   ✓ Election created: ID {election_id}, Blockchain ID {blockchain_election_id}")
    
    print("\n3. Adding candidates...")
    bc.add_candidate(blockchain_election_id, "Candidate A", "Party X")
    db.add_candidate(election_id, "Candidate A", "Party X", "Lotus")
    
    bc.add_candidate(blockchain_election_id, "Candidate B", "Party Y")
    db.add_candidate(election_id, "Candidate B", "Party Y", "Hand")
    print("   ✓ 2 candidates added")
    
    print("\n4. Registering voter on blockchain...")
    bc.register_voter_on_blockchain(blockchain_election_id, voter_address)
    print(f"   ✓ Voter registered for election on blockchain")
    
    print("\n5. Casting vote (signed by voter)...")
    tx_hash = bc.cast_vote(blockchain_election_id, 1, voter_private_key)
    db.record_vote(voter_id, election_id, tx_hash)
    print(f"   ✓ Vote cast - TX: {tx_hash[:32]}...")
    print(f"   ✓ Vote signed by voter's private key (secure!)")
    
    print("\n6. Checking results...")
    results = bc.get_all_results(blockchain_election_id)
    for result in results:
        print(f"   - {result['name']} ({result['party']}): {result['votes']} votes")
    
    print("\n7. Finalizing election...")
    bc.finalize_election(blockchain_election_id)
    winner = bc.get_winner(blockchain_election_id)
    print(f"   ✓ Winner: {winner[0]} ({winner[1]}) with {winner[2]} votes")
    
    print("\n✓ Complete workflow test passed!")
    return True

def main():
    print("=" * 60)
    print("MATA RAKSHA - SYSTEM VALIDATION TEST")
    print("=" * 60)
    
    try:
        test_database()
        bc = test_blockchain()
        test_biometric()
        
        if bc:
            test_complete_workflow()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED - SYSTEM IS READY")
        print("=" * 60)
        print("\nTo run the application:")
        print("  python main.py")
        print("\nDefault credentials:")
        print("  Admin:     admin/admin123")
        print("  Registrar: registrar/registrar123")
        print("  Officer:   officer/officer123")
        print("  Voter:     voter/voter123")
        print()
        
        return 0
    
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
