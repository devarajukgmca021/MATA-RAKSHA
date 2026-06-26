"""import sqlite3
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
        return hashlib.sha256(password.encode()).hexdigest()"""
import sqlite3
import hashlib
import os
from contextlib import closing
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

        # Existing tables (unchanged)
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
                aadhaar TEXT UNIQUE NOT NULL,
                district TEXT NOT NULL,
                fingerprint_hash TEXT NOT NULL,
                blockchain_address TEXT UNIQUE NOT NULL,
                private_key TEXT NOT NULL,
                photo_path TEXT,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vote_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voter_id TEXT NOT NULL,
                election_id INTEGER NOT NULL,
                candidate_id INTEGER NOT NULL,                
                tx_hash TEXT NOT NULL,
                voted_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (voter_id)    REFERENCES voters(voter_id),
                FOREIGN KEY (election_id) REFERENCES elections(id),
                FOREIGN KEY (candidate_id) REFERENCES candidates(id)
                UNIQUE(voter_id, election_id)
            )
        """)


        # ✅ New table for Registrars
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                district TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # ✅ New table for Officers (one per district)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS officers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                district TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create default admin if not exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        if cursor.fetchone()[0] == 0:
            admin_password = self.hash_password('admin123')
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ('admin', admin_password, 'admin')
            )

        conn.commit()
        conn.close()

    # ---------------------------- Utility Methods ----------------------------
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    # ---------------------------- Registrar CRUD ----------------------------
    def add_registrar(self, name, district, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO registrars (name, district, password_hash) VALUES (?, ?, ?)",
            (name, district, self.hash_password(password))
        )
        conn.commit()
        conn.close()

    def get_registrars(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, district FROM registrars ORDER BY id DESC")
        result = cursor.fetchall()
        conn.close()
        return result

    def update_registrar(self, old_name, new_name, new_district, new_password):
        conn = self.get_connection()
        cursor = conn.cursor()
        if new_password:
            cursor.execute(
                "UPDATE registrars SET name=?, district=?, password_hash=? WHERE name=?",
                (new_name, new_district, self.hash_password(new_password), old_name)
            )
        else:
            cursor.execute(
                "UPDATE registrars SET name=?, district=? WHERE name=?",
                (new_name, new_district, old_name)
            )
        conn.commit()
        conn.close()

    def delete_registrar(self, name):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM registrars WHERE name=?", (name,))
        conn.commit()
        conn.close()

    # ---------------------------- Officer CRUD ----------------------------
    def add_officer(self, name, district, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        password_hash = self.hash_password(password)
        cursor.execute(
            "INSERT INTO officers (name, district, password_hash) VALUES (?, ?, ?)",
            (name, district, self.hash_password(password))
        )
        conn.commit()
        conn.close()

    def get_officers(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, district FROM officers ORDER BY id DESC")
        result = cursor.fetchall()
        conn.close()
        return result

    def check_officer_exists(self, district):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM officers WHERE district = ?", (district,))
        result = cursor.fetchone()
        return result[0] > 0


    def update_officer(self, old_name, new_name, new_district, new_password):
        conn = self.get_connection()
        cursor = conn.cursor()
        if new_password:
            password_hash = self.hash_password(new_password)
            cursor.execute(
                "UPDATE officers SET name=?, district=?, password_hash=? WHERE name=?",
                (new_name, new_district, self.hash_password(new_password), old_name)
            )
        else:
            cursor.execute(
                "UPDATE officers SET name=?, district=? WHERE name=?",
                (new_name, new_district, old_name)
            )
        conn.commit()
        conn.close()

    def delete_officer(self, name):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM officers WHERE name = ?", (name,))
        conn.commit()
        conn.close()


    # ---------------------------- Other Existing Methods ----------------------------
    # (keep all your previous methods: verify_login, create_election, etc.)

    
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
    def verify_login_registrar(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT * FROM registrars WHERE name = ? AND password_hash = ?",
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return "registrar" if result else None    

    def verify_login_officer(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT * FROM officers WHERE name = ? AND password_hash = ?",
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return "officer" if result else None
    
    def register_voter(self, name, dob, district, aadhaar,fingerprint_hash, blockchain_address, private_key):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        voter_id = f"VID{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        encrypted_private_key = self.encryption.encrypt(private_key)
        
        cursor.execute(
            '''INSERT INTO voters (voter_id, name, dob, district, aadhaar, fingerprint_hash, blockchain_address, private_key)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (voter_id, name, dob, district, aadhaar, fingerprint_hash, blockchain_address, encrypted_private_key)
        )
        
        conn.commit()
        conn.close()
        
        return voter_id
    
    def get_voter_by_fingerprint(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT voter_id, name, fingerprint_hash FROM voters"
        )
        
        result = cursor.fetchall()
        conn.close()
        return result
    def fingerprint_exists(self, fp_hash: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT voter_id, name FROM voters WHERE fingerprint_hash = ?",
            (fp_hash,)
        )
        row = cursor.fetchone()
        return row   # returns (voter_id, name) or None

    
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
               VALUES (?, ?, ?, ?, 'pending')''',
            (election_name, district, start_date, end_date)
        )
        
        election_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return election_id

    def get_candidates(self):
        """Fetch all candidates with election, district, party, and symbol details."""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT e.election_name, c.candidate_name, e.district, c.party_name, c.symbol
            FROM candidates c
            JOIN elections e ON c.election_id = e.id
            ORDER BY e.election_name, e.district
        """)
        result = cur.fetchall()
        conn.close()
        return result
    def get_candidates_filtered(self, election_name, district):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, e.election_name, c.candidate_name, c.party_name, c.symbol
            FROM candidates c
            JOIN elections e ON c.election_id = e.id
            WHERE e.election_name = ? AND e.district = ?
        """, (election_name, district))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_voter_by_aadhaar_or_id(self, key):
        """
        Fetch voter details using either Aadhaar number or Voter ID.

        Args:
            key (str): Aadhaar number or Voter ID

        Returns:
            tuple: voter record (id, voter_id, name, dob, aadhaar, district, fingerprint_hash, blockchain_address, private_key, photo_path, registered_at, has_voted)
                    or None if not found
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # Try Aadhaar first, then voter_id
        cursor.execute("""
            SELECT * FROM voters WHERE aadhaar = ? OR voter_id = ?
        """, (key, key))

        result = cursor.fetchone()
        conn.close()

        # If found, decrypt private key before returning
        if result:
            result = list(result)
            try:
                result[8] = self.encryption.decrypt(result[8])
            except Exception:
                pass
            return tuple(result)
        else:
            return None

    
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


    def update_candidate(self, old_name, election_id, candidate_name, party_name, symbol):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE candidates
            SET election_id = ?, candidate_name = ?, party_name = ?, symbol = ?
            WHERE candidate_name = ?
        """, (election_id, candidate_name, party_name, symbol, old_name))
        conn.commit()
        conn.close()

    def delete_candidate(self, candidate_name):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM candidates WHERE candidate_name = ?", (candidate_name,))
        conn.commit()
        conn.close()

    def get_candidates_by_election_district(self, election_name, district):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT candidate_name, party_name, symbol
            FROM candidates
            WHERE election_id IN (
                SELECT id FROM elections WHERE election_name = ? AND district = ?
            )
            ORDER BY id DESC
        """, (election_name, district))
        result = cursor.fetchall()
        conn.close()
        return result

    """def record_vote(self, voter_id, election_id, candidate_id, tx_hash=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO vote_records (voter_id, election_id, candidate_id, tx_hash)
                VALUES (?, ?, ?, ?)
            ''', (voter_id, election_id, candidate_id, tx_hash))

            cursor.execute('UPDATE voters SET has_voted = 1 WHERE voter_id = ?', (voter_id,))
            conn.commit()
        except sqlite3.IntegrityError:
            raise Exception("This voter has already voted in this election.")
        finally:
            conn.close())"""

    def get_vote_counts(self, election_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.candidate_name, c.party_name, COUNT(v.id) AS total_votes
            FROM candidates c
            LEFT JOIN vote_records v ON c.id = v.candidate_id
            WHERE c.election_id = ?
            GROUP BY c.id
            ORDER BY total_votes DESC
        ''', (election_id,))
        results = cursor.fetchall()
        conn.close()
        return results

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
        # ---------------------------- Election Lifecycle Helpers ----------------------------
    def update_election_status(self, election_id: int, new_status: str):
        """Update the lifecycle status (pending, active, completed, archived)."""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE elections SET status = ? WHERE id = ?", (new_status, election_id))
        conn.commit()
        conn.close()

    def count_voters_in_district(self, district: str) -> int:
        """Return total registered voters in a specific district."""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM voters WHERE district = ?", (district,))
        n = cur.fetchone()[0] or 0
        conn.close()
        return n

    def count_votes_in_election(self, election_id: int) -> int:
        """Return number of votes cast in a given election."""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM vote_records WHERE election_id = ?", (election_id,))
        n = cur.fetchone()[0] or 0
        conn.close()
        return n
    
    def get_candidates_by_election(self, election_id: int):
        # returns [(id, candidate_name, party_name, symbol), ...]
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, candidate_name, party_name, symbol FROM candidates WHERE election_id = ?", (election_id,))
        rows = cur.fetchall()
        conn.close()
        return rows
    
    def get_vote_counts_by_candidate(self, election_id: int):
        """
        Return list of (candidate_name, votes) for result display.
        NOTE: Works only if 'vote_records' has 'candidate_id' column.
        If not, update your schema accordingly.
        """
        conn = self.get_connection()
        cur = conn.cursor()

        # ✅ Make sure your table 'vote_records' has 'candidate_id INTEGER' column!
        try:
            cur.execute("""
                SELECT c.candidate_name, COUNT(v.id) as votes
                FROM candidates c
                LEFT JOIN vote_records v
                ON v.candidate_id = c.id
                WHERE c.election_id = ?
                GROUP BY c.id, c.candidate_name
            """, (election_id,))
        except sqlite3.OperationalError:
            # fallback if column not added yet
            cur.execute("SELECT candidate_name, 0 FROM candidates WHERE election_id = ?", (election_id,))

        results = cur.fetchall()
        conn.close()
        return results

    def get_voters_by_district(self, district_name: str):
        """Fetch all voters belonging to a given district."""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT voter_id, name, dob, aadhaar, district FROM voters WHERE district = ?",(district_name,))
        rows = cur.fetchall()
        return rows

    def get_voters_by_district_bc(self, district_name: str):
        """Fetch all voters belonging to a given district."""
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT blockchain_address,voter_id FROM voters WHERE district = ?",(district_name,))
        rows = cur.fetchall()
        return rows

    
    def update_voter(self, voter_id, name, dob, aadhaar, district, fingerprint_hash):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE voters SET name=?, dob=?, aadhaar=?, district=?, fingerprint_hash=?
            WHERE voter_id=?
        """, (name, dob, aadhaar, district, fingerprint_hash, voter_id))
        conn.commit()
        conn.close()
    def fingerprint_exists_except(self, current_voter_id: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT voter_id, name, fingerprint_hash 
            FROM voters 
            WHERE voter_id != ?
        """,(current_voter_id,))
        rows = cursor.fetchall()
        return rows

    def delete_voter(self, voter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM voters WHERE voter_id=?", (voter_id,))
        conn.commit()
        conn.close()


# --- ADD helpers below your existing methods ---

    def get_officer_district_from_role(self, role_or_username: str) -> str | None:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT district FROM officers WHERE name=?" ,(role_or_username,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
        

    def get_active_election_by_district(self, district: str):
        """Return (id, election_name, start_date, end_date, status) of the latest ACTIVE election in a district."""
        with closing(self.get_connection()) as conn, closing(conn.cursor()) as c:
            c.execute("""
                SELECT id, election_name, start_date, end_date, status
                FROM elections
                WHERE district = ? AND status = 'active'
                ORDER BY datetime(created_at) DESC
                LIMIT 1
            """, (district,))
            return c.fetchone()

    #def get_voter_by_aadhaar_or_id(self, key: str):
        """Find voter by aadhaar or voter_id (exact match)."""
        #with closing(self.get_connection()) as conn, closing(conn.cursor()) as c:
            #c.execute("""
                #SELECT id, voter_id, name, dob, district, aadhaar, fingerprint_hash,
                       #blockchain_address, private_key, has_voted
                #FROM voters
                #WHERE aadhaar = ? OR voter_id = ?
            #""", (key, key))
            #return c.fetchone()

    def get_candidates_for_election_district(self, election_id: int, district: str):
        """
        Return list of candidates for a given election_id (the election already fixed to a district in your schema).
        Shape: [(candidate_id, candidate_name, party_name, symbol)]
        """
        with closing(self.get_connection()) as conn, closing(conn.cursor()) as c:
            c.execute("""
                SELECT c.id, c.candidate_name, c.party_name, c.symbol
                FROM candidates c
                WHERE c.election_id = ?
            """, (election_id,))
            return c.fetchall()
        #ORDER BY c.candidate_name COLLATE NOCASE
    def verify_voter_e(self, voter_id: str, election_id: int,):
        with closing(self.get_connection()) as conn, closing(conn.cursor()) as c:
            c.execute("""
                SELECT voter_id FROM vote_records WHERE voter_id=? AND election_id=?
            """, (voter_id, election_id))
            return c.fetchall()

    def record_vote(self, voter_id: str, election_id: int, candidate_id: int, tx_hash: str):
        with closing(self.get_connection()) as conn, closing(conn.cursor()) as c:
            c.execute("""
                INSERT INTO vote_records (voter_id, election_id, candidate_id, tx_hash)
                VALUES (?, ?, ?, ?)
            """, (voter_id, election_id, candidate_id, tx_hash))
            conn.commit()

    def count_voters_in_district(self, district: str) -> int:
        with closing(self.get_connection()) as conn, closing(conn.cursor()) as c:
            c.execute("SELECT COUNT(*) FROM voters WHERE district = ?", (district,))
            return int(c.fetchone()[0] or 0)

    def count_voted_in_election_district(self, election_id: int, district: str) -> int:
        with closing(self.get_connection()) as conn, closing(conn.cursor()) as c:
            c.execute("""
                SELECT COUNT(*)
                FROM vote_records vr
                JOIN elections e ON e.id = vr.election_id
                JOIN voters v ON v.voter_id = vr.voter_id
                WHERE vr.election_id = ? AND e.district = ? AND v.district = e.district
            """, (election_id, district))
            return int(c.fetchone()[0] or 0)

    def results_summary_by_election(self, election_id: int):
        """
        Return [(candidate_name, party_name, symbol, votes)] ordered by votes desc.
        """
        with closing(self.get_connection()) as conn, closing(conn.cursor()) as c:
            c.execute("""
                SELECT c.candidate_name, c.party_name, c.symbol, COUNT(vr.id) AS votes
                FROM candidates c
                LEFT JOIN vote_records vr ON vr.candidate_id = c.id
                WHERE c.election_id = ?
                GROUP BY c.id
                ORDER BY votes DESC, c.candidate_name COLLATE NOCASE
            """, (election_id,))
            return c.fetchall()

    
