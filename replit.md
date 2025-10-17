# Mata Raksha - Blockchain E-Voting System

## Project Overview

Mata Raksha is a secure blockchain-based biometric e-voting desktop application built for Karnataka state elections. The system uses Python (Tkinter), SQLite, and Ethereum (Ganache) to provide tamper-proof, transparent voting.

## Recent Changes

**Date**: October 17, 2025

### Initial Implementation
- ✅ Complete project structure with modular architecture
- ✅ SQLite database schema with all required tables
- ✅ Solidity smart contract for immutable vote storage
- ✅ Four role-based Tkinter GUI dashboards (Admin, Registrar, Officer, Voter)
- ✅ Blockchain integration with web3.py
- ✅ Simulated biometric fingerprint authentication
- ✅ Ganache local blockchain configured and running
- ✅ Comprehensive README documentation

## User Preferences

### Development Environment
- **Language**: Python 3.11
- **GUI Framework**: Tkinter (desktop application)
- **Database**: SQLite (file-based, portable)
- **Blockchain**: Ganache (local Ethereum testnet)
- **Biometric**: Simulated fingerprint verification (for MVP)

### Default Credentials
- Admin: admin/admin123
- Registrar: registrar/registrar123  
- Officer: officer/officer123
- Voter: voter/voter123

## Project Architecture

### Core Components

1. **Database Layer** (`src/utils/database.py`)
   - SQLite database with 5 tables: users, voters, elections, candidates, vote_records
   - Handles voter registration, election management, vote recording
   - Supports all 30 Karnataka districts

2. **Blockchain Layer** (`src/utils/blockchain.py`)
   - Web3.py integration with Ganache
   - Smart contract compilation and deployment
   - Vote submission and retrieval
   - Result verification

3. **Smart Contract** (`contracts/VotingContract.sol`)
   - Solidity 0.8.0 contract
   - Immutable vote storage
   - Duplicate vote prevention
   - Automated vote counting
   - Election finalization

4. **GUI Layer** (`src/gui/`)
   - Login window with role-based authentication
   - Admin dashboard: election/candidate creation, results
   - Registrar dashboard: voter registration with biometric
   - Officer dashboard: voter verification, supervised voting
   - Voter portal: view candidates and results

5. **Biometric Simulation** (`src/utils/biometric.py`)
   - Generates simulated fingerprint templates
   - Creates hash-based fingerprint verification
   - Saves visual fingerprint representations

### Workflow Architecture

```
Ganache Blockchain (Port 8545)
    ↓
Smart Contract Deployment
    ↓
┌─────────────────────────────────────────┐
│  Voter Registration (Registrar)         │
│  → Capture biometric                    │
│  → Create blockchain address            │
│  → Store in SQLite                      │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Election Creation (Admin)               │
│  → Deploy smart contract                │
│  → Add candidates to blockchain         │
│  → Store election in SQLite             │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Vote Casting (Officer + Voter)         │
│  → Verify biometric                     │
│  → Check district match                 │
│  → Submit vote to blockchain            │
│  → Record tx hash in SQLite             │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Results (Admin/Voter)                  │
│  → Fetch from blockchain                │
│  → Display vote counts                  │
│  → Determine winner                     │
└─────────────────────────────────────────┘
```

### Security Features

- **Password Security**: SHA-256 hashing
- **Biometric Verification**: Fingerprint hash matching
- **Blockchain Immutability**: Votes cannot be altered
- **District Verification**: Voters restricted to their district
- **Duplicate Prevention**: Smart contract enforces one vote per address
- **Transaction Audit**: Every vote has blockchain tx hash

### File Structure

```
mata-raksha/
├── main.py                     # Application entry point
├── contracts/
│   └── VotingContract.sol     # Ethereum smart contract
├── src/
│   ├── gui/                   # Tkinter interfaces
│   │   ├── login_window.py
│   │   ├── admin_dashboard.py
│   │   ├── registrar_dashboard.py
│   │   ├── officer_dashboard.py
│   │   └── voter_dashboard.py
│   └── utils/                 # Core utilities
│       ├── database.py        # SQLite manager
│       ├── blockchain.py      # Web3 integration
│       └── biometric.py       # Fingerprint simulation
├── database/                  # SQLite database (auto-created)
├── assets/
│   └── biometric_templates/   # Fingerprint images
└── README.md                  # User documentation
```

## Running the Application

### Prerequisites
- Python 3.11 with tkinter support
- Node.js 20 (for Ganache)
- Desktop environment with GUI support

### In Replit
```bash
# Ganache is already running in workflow
# To run locally, execute:
python main.py
```

### Running Locally (Outside Replit)

1. **Clone and Install**:
   ```bash
   pip install web3 Pillow py-solc-x
   npm install -g ganache
   ```

2. **Start Ganache**:
   ```bash
   ganache --host 127.0.0.1 --port 8545 --accounts 10 --defaultBalanceEther 1000
   ```

3. **Run Application**:
   ```bash
   python main.py
   ```

## Known Limitations (MVP)

1. **Tkinter GUI**: Requires desktop environment (won't run in Replit web interface)
2. **Simulated Biometric**: Uses hash-based simulation instead of real hardware
3. **Local Blockchain**: Uses Ganache instead of testnet/mainnet
4. **No Encryption**: Biometric data stored as hashes (not encrypted)

## Future Enhancements

- [ ] Real MFS100 fingerprint scanner integration
- [ ] Deploy to Ethereum Testnet (Sepolia)
- [ ] End-to-end encryption for sensitive data
- [ ] Web-based interface (Flask/Django backend)
- [ ] Multi-factor authentication
- [ ] Real-time analytics dashboard
- [ ] Aadhaar integration for voter verification

## Development Notes

### Database Schema
- **users**: Login credentials (username, password_hash, role)
- **voters**: Voter profiles (voter_id, name, dob, district, fingerprint_hash, blockchain_address)
- **elections**: Elections (election_name, district, dates, contract_address, status)
- **candidates**: Candidates (election_id, candidate_name, party_name, symbol)
- **vote_records**: Vote audit (voter_id, election_id, tx_hash, timestamp)

### Smart Contract Functions
- `createElection()`: Deploy new election
- `addCandidate()`: Add candidate to election
- `vote()`: Cast vote (enforces duplicate prevention)
- `getCandidate()`: Retrieve candidate data
- `finalizeElection()`: Lock election and determine winner
- `getWinner()`: Get election winner

### Testing Checklist
- [x] Admin can create elections
- [x] Admin can add candidates
- [x] Registrar can register voters
- [x] Officer can verify and record votes
- [x] Blockchain stores votes immutably
- [x] Results can be viewed and finalized
- [ ] End-to-end workflow test (requires GUI)

## Technical Stack

- **Frontend**: Python Tkinter (Desktop GUI)
- **Backend**: Python 3.11
- **Database**: SQLite 3
- **Blockchain**: Ethereum (Ganache 7.9.2)
- **Smart Contracts**: Solidity 0.8.0
- **Web3**: web3.py 7.14.0
- **Biometric**: Pillow (image generation)

## Contributors

- Devaraju K G
- Bharath H R
- Institution: RNS Institute of Technology

---

**Last Updated**: October 17, 2025
