import hashlib
from typing import Dict, List, Set


class BreachChecker:
    
    def __init__(self):
        self.breached_passwords = self._load_breached_passwords()
        self.breached_hashes = self._hash_passwords()
    
    def _load_breached_passwords(self) -> Set[str]:
        common_breached = [
            '123456', 'password', '123456789', '12345678', '12345',
            '1234567', '1234567890', 'qwerty', 'abc123', '111111',
            '123123', 'admin', 'letmein', 'welcome', 'monkey',
            '1234567890', 'qwerty123', 'password1', 'sunshine', 'princess',
            'football', 'iloveyou', 'master', 'hello', 'freedom',
            'whatever', 'qazwsx', 'trustno1', 'dragon', 'baseball',
            'starwars', 'shadow', 'michael', 'hockey', 'ranger',
            'daniel', 'hannah', 'maggie', 'jessica', 'charlie',
            'jordan', 'tigger', 'michelle', 'charlotte', 'samantha',
            'welcome123', 'password123', 'admin123', 'root', 'toor',
            'pass', 'test', 'guest', 'user', 'demo'
        ]
        
        return set(common_breached)
    
    def _hash_passwords(self) -> Set[str]:
        hashed = set()
        for password in self.breached_passwords:
            hash_obj = hashlib.sha256(password.encode('utf-8'))
            hashed.add(hash_obj.hexdigest())
        return hashed
    
    def check(self, password: str) -> Dict:
        if not password:
            return {
                'breached': False,
                'severity': 'None',
                'message': 'No password provided',
                'recommendation': 'Enter a password to check'
            }
        
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        is_breached = password_hash in self.breached_hashes
        
        password_lower_hash = hashlib.sha256(password.lower().encode('utf-8')).hexdigest()
        is_breached_lower = password_lower_hash in self.breached_hashes
        
        breached = is_breached or is_breached_lower
        
        if breached:
            severity = 'Critical'
            message = 'This password has been found in known data breaches'
            recommendation = 'Change this password immediately. Use a unique, strong password.'
        else:
            severity = 'None'
            message = 'This password was not found in our breach database'
            recommendation = 'Continue using strong, unique passwords for each account.'
        
        return {
            'breached': breached,
            'severity': severity,
            'message': message,
            'recommendation': recommendation,
            'note': 'This check uses hashed comparison. Your password is never stored or transmitted.'
        }
    
    def check_with_variations(self, password: str) -> Dict:
        base_result = self.check(password)
        
        variations = [
            password.lower(),
            password.upper(),
            password.capitalize(),
            password + '123',
            password + '1',
            '123' + password
        ]
        
        variation_results = []
        for variant in variations:
            if variant != password:
                variant_hash = hashlib.sha256(variant.encode('utf-8')).hexdigest()
                if variant_hash in self.breached_hashes:
                    variation_results.append({
                        'variant': variant[:3] + '***',
                        'breached': True
                    })
        
        if variation_results:
            base_result['variation_breached'] = True
            base_result['variation_count'] = len(variation_results)
        else:
            base_result['variation_breached'] = False
            base_result['variation_count'] = 0
        
        return base_result
