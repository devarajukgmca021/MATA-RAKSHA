import sqlite3
import hashlib
import os
from datetime import datetime
from src.utils.encryption import EncryptionManager

class Database:
    def __init__(self, db_path='database/mata_raksha.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.encryption = EncryptionManager()
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS voters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voter_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                dob DATE NOT NULL,
                district TEXT NOT NULL,
                fingerprint_hash TEXT NOT NULL,
                blockchain_address TEXT UNIQUE NOT NULL,
                private_key TEXT NOT NULL,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                has_voted INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS elections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                election_name TEXT NOT NULL,
                district TEXT NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                contract_address TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                election_id INTEGER NOT NULL,
                candidate_name TEXT NOT NULL,
                party_name TEXT NOT NULL,
                symbol TEXT,
                FOREIGN KEY (election_id) REFERENCES elections(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vote_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voter_id TEXT NOT NULL,
                election_id INTEGER NOT NULL,
                tx_hash TEXT NOT NULL,
                voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (voter_id) REFERENCES voters(voter_id),
                FOREIGN KEY (election_id) REFERENCES elections(id)
            )
        ''')
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        if cursor.fetchone()[0] == 0:
            admin_password = self.hash_password('admin123')
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ('admin', admin_password, 'admin')
            )
            
            registrar_password = self.hash_password('registrar123')
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ('registrar', registrar_password, 'registrar')
            )
            
            officer_password = self.hash_password('officer123')
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ('officer', officer_password, 'officer')
            )
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_login(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT role FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def register_voter(self, name, dob, district, fingerprint_hash, blockchain_address, private_key):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        voter_id = f"VID{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        encrypted_private_key = self.encryption.encrypt(private_key)
        
        cursor.execute(
            '''INSERT INTO voters (voter_id, name, dob, district, fingerprint_hash, blockchain_address, private_key)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (voter_id, name, dob, district, fingerprint_hash, blockchain_address, encrypted_private_key)
        )
        
        conn.commit()
        conn.close()
        
        return voter_id
    
    def get_voter_by_fingerprint(self, fingerprint_hash):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM voters WHERE fingerprint_hash = ?",
            (fingerprint_hash,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result
    
    def get_voter_by_id(self, voter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM voters WHERE voter_id = ?", (voter_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            result = list(result)
            result[7] = self.encryption.decrypt(result[7])
            result = tuple(result)
        
        return result
    
    def create_election(self, election_name, district, start_date, end_date):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''INSERT INTO elections (election_name, district, start_date, end_date, status)
               VALUES (?, ?, ?, ?, 'active')''',
            (election_name, district, start_date, end_date)
        )
        
        election_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return election_id
    
    def add_candidate(self, election_id, candidate_name, party_name, symbol):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''INSERT INTO candidates (election_id, candidate_name, party_name, symbol)
               VALUES (?, ?, ?, ?)''',
            (election_id, candidate_name, party_name, symbol)
        )
        
        conn.commit()
        conn.close()
    
    def get_elections(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM elections ORDER BY created_at DESC")
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def get_candidates_by_election(self, election_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM candidates WHERE election_id = ?",
            (election_id,)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    def record_vote(self, voter_id, election_id, tx_hash):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''INSERT INTO vote_records (voter_id, election_id, tx_hash)
               VALUES (?, ?, ?)''',
            (voter_id, election_id, tx_hash)
        )
        
        cursor.execute(
            "UPDATE voters SET has_voted = 1 WHERE voter_id = ?",
            (voter_id,)
        )
        
        conn.commit()
        conn.close()
    
    def update_election_contract(self, election_id, contract_address):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE elections SET contract_address = ? WHERE id = ?",
            (contract_address, election_id)
        )
        
        conn.commit()
        conn.close()
    
    def get_karnataka_districts(self):
        return [
            "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban",
            "Bidar", "Chamarajanagar", "Chikkaballapur", "Chikkamagaluru", "Chitradurga",
            "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", "Hassan",
            "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal",
            "Mandya", "Mysuru", "Raichur", "Ramanagara", "Shivamogga",
            "Tumakuru", "Udupi", "Uttara Kannada", "Vijayapura", "Yadgir"
        ]
