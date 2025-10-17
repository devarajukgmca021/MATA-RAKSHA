import hashlib
import random
from PIL import Image, ImageDraw
import os

class BiometricSimulator:
    def __init__(self):
        self.template_dir = 'assets/biometric_templates'
        os.makedirs(self.template_dir, exist_ok=True)
    
    def generate_fingerprint_template(self, name):
        unique_string = f"{name}_{random.randint(1000, 9999)}"
        fingerprint_hash = hashlib.sha256(unique_string.encode()).hexdigest()
        
        img = Image.new('RGB', (200, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        for i in range(20):
            x1 = random.randint(10, 190)
            y1 = random.randint(10, 190)
            x2 = x1 + random.randint(-50, 50)
            y2 = y1 + random.randint(-50, 50)
            draw.line([(x1, y1), (x2, y2)], fill='black', width=2)
        
        for i in range(10):
            x = random.randint(10, 190)
            y = random.randint(10, 190)
            draw.ellipse([x-3, y-3, x+3, y+3], fill='black')
        
        template_path = os.path.join(self.template_dir, f"{fingerprint_hash[:16]}.png")
        img.save(template_path)
        
        return fingerprint_hash, template_path
    
    def simulate_fingerprint_scan(self):
        scan_string = f"scan_{random.randint(10000, 99999)}"
        return hashlib.sha256(scan_string.encode()).hexdigest()
    
    def verify_fingerprint(self, stored_hash, scanned_hash):
        return stored_hash == scanned_hash
    
    def get_fingerprint_hash_from_name(self, name):
        unique_string = f"{name}_{random.randint(1000, 9999)}"
        return hashlib.sha256(unique_string.encode()).hexdigest()
