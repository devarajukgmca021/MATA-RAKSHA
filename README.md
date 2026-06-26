# 🗳️ MATA RAKSHA

## AI-Enhanced Biometric Blockchain Voting System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Blockchain](https://img.shields.io/badge/Blockchain-Ethereum-purple)
![Solidity](https://img.shields.io/badge/Solidity-Smart%20Contracts-black)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

</p>

A secure desktop-based voting system that integrates **biometric fingerprint authentication** with **Ethereum blockchain technology** to provide secure, transparent, and tamper-proof digital elections.

The system enables election administrators to manage the complete election lifecycle—from voter registration and biometric verification to secure vote casting and blockchain-based result generation. It also includes AI analytics modules for election intelligence, which are currently under development for future integration.

---

# 📖 Project Overview

Traditional voting systems often suffer from centralized data storage, voter impersonation, duplicate voting, and limited transparency.

**MATA RAKSHA** addresses these challenges by combining **fingerprint-based biometric authentication**, **role-based election management**, and **Ethereum blockchain technology** into a secure desktop application.

The system authenticates every voter using the **SecuGen Hamster Pro 20 (HU20-AP)** biometric fingerprint scanner before allowing vote casting. Once authenticated, votes are securely recorded as immutable blockchain transactions using Ethereum smart contracts, ensuring election integrity and transparency.

The application follows a **role-based architecture** consisting of three operational modules:

- 👨‍💼 Administrator
- 📝 Registrar
- 🛡️ Election Officer

Each module performs a dedicated responsibility throughout the election lifecycle, from election creation and voter registration to biometric verification, blockchain vote storage, and result computation.

---

# 🎯 Election Workflow

The election process follows a structured workflow to ensure secure voter authentication and transparent election management.

```text
Administrator
        │
        ▼
Create Election
        │
        ▼
Assign Registrar & Election Officer
        │
        ▼
Registrar Registers Voters
        │
        ▼
Capture Fingerprint (SecuGen HU20-AP)
        │
        ▼
Generate Encrypted Biometric Template
        │
        ▼
Store Secure Voter Information
        │
        ▼
Election Officer Verification
        │
        ▼
Fingerprint Authentication
        │
        ▼
Secure Vote Casting
        │
        ▼
Ethereum Blockchain Transaction
        │
        ▼
Immutable Vote Storage
        │
        ▼
Election Result Generation
```

---

# ✨ Key Features

## 🔐 Secure Authentication

- Role-Based Access Control (RBAC)
- Secure Login Authentication
- Fingerprint-Based Voter Verification
- Duplicate Vote Prevention
- Encrypted Biometric Template Storage
- Aadhaar-Based Voter Identification

---

## 👨‍💼 Administrator Module

The Administrator manages the complete election lifecycle.

Features include:

- Registrar Management
- Election Officer Management
- Election Creation
- District-wise Election Configuration
- Candidate Management
- Election Lifecycle Monitoring
- Result Publication

---

## 📝 Registrar Module

The Registrar is responsible for biometric voter enrollment.

Features include:

- Register New Voters
- Aadhaar Verification
- Fingerprint Capture using SecuGen HU20-AP
- Fingerprint Quality Testing
- Secure Biometric Template Storage
- Digital Voter ID Generation
- Update/Delete Voter Records
- District-wise PDF Export
- PNG Voter ID Card Generation

---

## 🛡️ Election Officer Module

The Election Officer manages secure voter verification and vote casting.

Features include:

- Verify Registered Voters
- Fingerprint Authentication
- Secure Voting Window
- Candidate Selection
- Blockchain Vote Submission
- Live Election Status
- Blockchain Connectivity Monitoring
- Turnout Progress Tracking

---

## ⛓️ Blockchain Security

The voting system uses Ethereum blockchain technology to guarantee vote integrity.

Features include:

- Ethereum Smart Contracts
- Immutable Vote Storage
- Tamper-Proof Voting Records
- Transparent Vote Counting
- Blockchain Transaction Verification
- Secure Result Computation

---

## 📊 Election Analytics

The application provides comprehensive election monitoring.

Features include:

- Real-Time Voting Progress
- District-wise Election Status
- Live Turnout Percentage
- Election Lifecycle Management
- Result Generation
- Audit Logs
- Vote History

---

# 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python 3 |
| Desktop GUI | CustomTkinter |
| Database | SQLite |
| Blockchain | Ethereum |
| Smart Contracts | Solidity |
| Blockchain Network | Ganache |
| Blockchain Integration | Web3.py |
| Biometric Device | SecuGen Hamster Pro 20 (HU20-AP) |
| Fingerprint SDK | SecuGen FDx SDK |
| Security | Cryptographic Hashing |
| AI Libraries *(Under Development)* | OpenCV, NumPy, Scikit-learn |
| Development Environment | Visual Studio Code |

---

# 🚀 Project Highlights

- ✅ Role-Based Election Management
- ✅ Fingerprint Biometric Authentication
- ✅ Ethereum Blockchain Integration
- ✅ Secure Smart Contract Voting
- ✅ District-Wise Election Support
- ✅ Election Lifecycle Management
- ✅ Candidate Management
- ✅ Secure Voter Registration
- ✅ Digital Voter ID Generation
- ✅ Live Voting Progress
- ✅ Blockchain Result Verification
- ✅ Audit Logs & Vote History
- ✅ Modular Desktop Architecture

---

# 🧠 AI Enhancement (Under Development)

To further strengthen election security and analytics, AI modules have been developed and are planned for future integration into the voting workflow.

The planned AI capabilities include:

- 🔍 Fingerprint Quality Assessment
- 📈 Voter Turnout Prediction
- 🚨 Election Anomaly Detection using Isolation Forest
- 📊 Voting Pattern Analysis
- ⚠️ Suspicious Activity Detection

> **Note:** These AI modules are implemented within the project but are currently under development and have not yet been integrated into the primary election workflow.

---
