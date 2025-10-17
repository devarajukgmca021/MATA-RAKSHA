# Mata Raksha - Blockchain-Based Biometric E-Voting System

A secure, transparent, and tamper-proof biometric e-voting system built as a desktop application using Python (Tkinter), SQLite, and Blockchain (Ethereum/Ganache).

## 🎯 Features

- **Role-Based Access Control**: Admin, Voter Registrar, Election Officer, and Voter portals
- **Biometric Authentication**: Simulated fingerprint verification for voter identity
- **Blockchain Integration**: Immutable vote recording using Ethereum smart contracts
- **District-Based Elections**: Support for all 30 Karnataka districts
- **Transparent Results**: Blockchain-verified vote tallying and result publication

## 📋 System Requirements

- Python 3.10 or higher
- Node.js 20.x (for Ganache)
- 4GB RAM minimum
- Operating System: Windows, macOS, or Linux with GUI support

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
# Install Python packages
pip install web3 Pillow py-solc-x pycryptodome

# Install Ganache globally
npm install -g ganache
```

### 2. Set Encryption Key (REQUIRED)

**CRITICAL SECURITY REQUIREMENT**: Set a strong encryption key for voter private key storage:

```bash
# Generate a strong random key (recommended)
export ENCRYPTION_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")

# OR set your own 32+ character key
export ENCRYPTION_KEY='your-very-strong-random-encryption-key-minimum-32-characters'
```

⚠️ **IMPORTANT**: 
- The application will FAIL if ENCRYPTION_KEY is not set
- Key must be at least 32 characters long
- Store this key securely - losing it means losing access to voter private keys
- NEVER commit this key to version control
- Change the key between environments (development/production)

### 3. Start Ganache Blockchain

```bash
# Start local blockchain (keep this terminal open)
ganache --host 127.0.0.1 --port 8545 --accounts 10 --defaultBalanceEther 1000
```

### 4. Run the Application

```bash
# In a new terminal, run the main application
python main.py
```

## 👥 User Roles & Default Credentials

| Role | Username | Password | Responsibilities |
|------|----------|----------|------------------|
| **Admin** | admin | admin123 | Create elections, add candidates, publish results |
| **Voter Registrar** | registrar | registrar123 | Register voters with biometric data |
| **Election Officer** | officer | officer123 | Verify voters and record votes |
| **Voter** | voter | voter123 | View candidates and election results |

## 📖 Usage Guide

### Admin Workflow

1. Login with admin credentials
2. **Create Election Tab**:
   - Enter election name
   - Select district from Karnataka districts
   - Set start and end dates
   - Click "Create Election on Blockchain" (deploys smart contract)

3. **Add Candidates Tab**:
   - Select the created election
   - Enter candidate name, party name, and symbol
   - Click "Add Candidate to Blockchain"

4. **View Results Tab**:
   - Select an election
   - Click "View Results" to see vote counts
   - Click "Finalize Election" to determine winner

### Voter Registrar Workflow

1. Login with registrar credentials
2. Enter voter details:
   - Full name
   - Date of birth (YYYY-MM-DD format)
   - Select district
3. Click "Capture Fingerprint" (simulates biometric capture)
4. Click "Register Voter" - generates unique Voter ID and blockchain address

### Election Officer Workflow

1. Login with officer credentials
2. **Step 1 - Verify Voter**:
   - Enter Voter ID
   - Click "Verify Fingerprint"
   - Confirm fingerprint scan

3. **Step 2 - Cast Vote**:
   - Select election (must match voter's district)
   - View candidates for that district
   - Select candidate (voter supervises)
   - Click "Submit Vote to Blockchain"
   - Vote is recorded immutably with transaction hash

### Voter Portal Workflow

1. Login with voter credentials (or custom voter account)
2. **View Elections Tab**:
   - Select an election
   - Click "View Candidates" to see candidate list

3. **View Results Tab**:
   - Select an election
   - Click "View Results" to see blockchain-verified results

## 🔗 Blockchain Architecture

### Smart Contract Features

- **VotingContract.sol**: Solidity 0.8.0 smart contract deployed on Ganache
- **Voter Registration**: On-chain pre-registration required for each election
- **Secure Authentication**: Uses `msg.sender` for voter verification (not a parameter)
- **Immutable Vote Storage**: Each vote is a blockchain transaction signed by voter
- **Duplicate Prevention**: Smart contract enforces one vote per address
- **Transparent Tallying**: Vote counts stored on-chain
- **Finalization**: Admin can finalize and determine winner
- **Access Control**: Only admin can create elections, add candidates, and finalize

### Secure Vote Flow

```
Voter Registration → Blockchain Address + Private Key Created
       ↓
Voter Funded → 0.1 ETH for gas fees
       ↓
Election Created → Smart Contract Deployed
       ↓
Candidates Added → Stored in Smart Contract
       ↓
Voter Verified → Biometric authentication by Officer
       ↓
Voter Registered on Blockchain → Pre-registration for election
       ↓
Vote Cast → Transaction SIGNED BY VOTER'S PRIVATE KEY
       ↓
Smart Contract Validates → Checks msg.sender, registration, duplicates
       ↓
Vote Recorded → Immutably stored on blockchain
       ↓
Results Tallied → Blockchain verification
       ↓
Election Finalized → Winner declared
```

## 🗂️ Project Structure

```
mata-raksha/
├── main.py                          # Application entry point
├── contracts/
│   └── VotingContract.sol          # Ethereum smart contract
├── src/
│   ├── gui/
│   │   ├── login_window.py         # Login interface
│   │   ├── admin_dashboard.py      # Admin portal
│   │   ├── registrar_dashboard.py  # Registrar portal
│   │   ├── officer_dashboard.py    # Officer portal
│   │   └── voter_dashboard.py      # Voter portal
│   └── utils/
│       ├── database.py             # SQLite database manager
│       ├── blockchain.py           # Web3 blockchain integration
│       └── biometric.py            # Fingerprint simulation
├── database/
│   └── mata_raksha.db             # SQLite database (auto-created)
└── assets/
    └── biometric_templates/        # Simulated fingerprint images
```

## 🗄️ Database Schema

### Tables

1. **users**: Login credentials and roles
2. **voters**: Voter registration with biometric hash
3. **elections**: District-based elections with blockchain contract addresses
4. **candidates**: Candidates linked to elections
5. **vote_records**: Vote audit trail with transaction hashes

## 🔐 Security Features

- **Password Hashing**: SHA-256 hashed passwords for user authentication
- **Biometric Verification**: Fingerprint hash matching (simulated) for voter identity
- **Blockchain Immutability**: Votes cannot be altered after submission on blockchain
- **District Verification**: Voters can only vote in their registered district
- **Voter Authentication**: Each voter signs transactions with their own private key
- **On-Chain Registration**: Voters must be pre-registered on blockchain for each election
- **Duplicate Prevention**: Smart contract enforces one vote per address using msg.sender
- **Transaction Verification**: Each vote includes blockchain transaction hash
- **Gas Funding**: Voters funded with ETH for transaction fees during registration
- **Cryptographic Signing**: All votes cryptographically signed by voter's private key
- **Encrypted Key Storage**: Private keys encrypted at rest using AES-256 with PBKDF2 key derivation
- **Secure Key Management**: Encryption key can be set via ENCRYPTION_KEY environment variable

## 🌐 Karnataka Districts Supported

All 30 districts of Karnataka are supported:
- Bagalkot, Ballari, Belagavi, Bengaluru Rural, Bengaluru Urban
- Bidar, Chamarajanagar, Chikkaballapur, Chikkamagaluru, Chitradurga
- Dakshina Kannada, Davanagere, Dharwad, Gadag, Hassan
- Haveri, Kalaburagi, Kodagu, Kolar, Koppal
- Mandya, Mysuru, Raichur, Ramanagara, Shivamogga
- Tumakuru, Udupi, Uttara Kannada, Vijayapura, Yadgir

## 🧪 Testing Workflow

### Complete End-to-End Test

1. **Start Ganache** (Terminal 1):
   ```bash
   ganache --host 127.0.0.1 --port 8545
   ```

2. **Run Application** (Terminal 2):
   ```bash
   python main.py
   ```

3. **Register Voter** (as Registrar):
   - Login: registrar/registrar123
   - Register voter in "Bengaluru Urban" district

4. **Create Election** (as Admin):
   - Login: admin/admin123
   - Create election for "Bengaluru Urban"
   - Add 2-3 candidates

5. **Cast Vote** (as Officer):
   - Login: officer/officer123
   - Verify registered voter
   - Cast vote for a candidate

6. **View Results** (as Admin or Voter):
   - Check blockchain results
   - Finalize election to see winner

## 🚧 Troubleshooting

### Issue: "Not connected to Ganache"
**Solution**: Make sure Ganache is running on port 8545

### Issue: "Failed to compile contract"
**Solution**: Install Solidity compiler:
```bash
pip install py-solc-x
```

### Issue: Tkinter not available
**Solution**: Install tkinter:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (via Homebrew)
brew install python-tk

# Windows: Included with Python installer
```

## 📊 Future Enhancements

- Real fingerprint scanner integration (MFS100)
- Deploy to Ethereum Testnet (Sepolia/Goerli)
- End-to-end encryption for biometric data
- Multi-factor authentication
- Real-time election analytics dashboard
- Mobile application support
- Aadhaar integration

## 👨‍💻 Development Team

**Prepared by**: Devaraju K G, Bharath H R  
**Institution**: RNS Institute of Technology  
**Date**: October 2025

## 📄 License

This project is developed for educational and demonstration purposes.

---

**Note**: This is a MVP implementation with simulated biometric verification. For production use, integrate actual fingerprint hardware and deploy smart contracts to a secure testnet or mainnet.
