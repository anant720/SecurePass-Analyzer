import re
from typing import Dict, List


class AttackSimulator:
    
    COMMON_PASSWORDS = [
        '123456', 'password', '123456789', '12345678', '12345',
        '1234567', '1234567890', 'qwerty', 'abc123', '111111',
        '123123', 'admin', 'letmein', 'welcome', 'monkey',
        '1234567890', 'qwerty123', 'password1', '123456789', 'sunshine',
        'princess', 'football', 'iloveyou', 'master', 'hello',
        'freedom', 'whatever', 'qazwsx', 'trustno1', 'dragon',
        'baseball', 'iloveyou', 'starwars', 'shadow', 'michael',
        'superman', 'batman', 'thomas', 'hockey', 'ranger',
        'daniel', 'hannah', 'maggie', 'jessica', 'charlie',
        'jordan', 'tigger', 'michelle', 'charlotte', 'samantha'
    ]
    
    CHARSETS = {
        'lowercase': 26,
        'uppercase': 26,
        'numbers': 10,
        'special': 33,
        'alphanumeric': 62,
        'all': 95
    }
    
    ATTACK_SPEEDS = {
        'online': 1,
        'offline_fast': 10000000000,
        'offline_slow': 10000
    }
    
    def __init__(self):
        pass
    
    def dictionary_attack(self, password: str) -> Dict:
        password_lower = password.lower()
        
        exact_match = password_lower in [p.lower() for p in self.COMMON_PASSWORDS]
        
        contains_common = False
        matched_words = []
        
        for common_pass in self.COMMON_PASSWORDS:
            if common_pass.lower() in password_lower:
                contains_common = True
                matched_words.append(common_pass)
        
        vulnerability = 'High' if exact_match else ('Medium' if contains_common else 'Low')
        
        return {
            'vulnerable': exact_match or contains_common,
            'vulnerability_level': vulnerability,
            'exact_match': exact_match,
            'contains_common': contains_common,
            'matched_words': matched_words[:5],
            'explanation': self._get_dictionary_explanation(exact_match, contains_common)
        }
    
    def brute_force_estimate(self, password: str) -> Dict:
        if not password:
            return self._empty_brute_force_result()
        
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_number = bool(re.search(r'[0-9]', password))
        has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password))
        
        charset_size = 0
        charset_name = []
        
        if has_lower:
            charset_size += self.CHARSETS['lowercase']
            charset_name.append('lowercase')
        if has_upper:
            charset_size += self.CHARSETS['uppercase']
            charset_name.append('uppercase')
        if has_number:
            charset_size += self.CHARSETS['numbers']
            charset_name.append('numbers')
        if has_special:
            charset_size += self.CHARSETS['special']
            charset_name.append('special')
        
        if charset_size == 0:
            charset_size = 1
            charset_name = ['unknown']
        
        length = len(password)
        total_combinations = charset_size ** length
        
        results = {}
        
        for attack_type, speed in self.ATTACK_SPEEDS.items():
            seconds = total_combinations / speed
            results[attack_type] = {
                'seconds': seconds,
                'human_readable': self._format_time(seconds),
                'combinations': total_combinations
            }
        
        return {
            'length': length,
            'charset_size': charset_size,
            'charset_components': charset_name,
            'total_combinations': total_combinations,
            'combinations_scientific': f"{total_combinations:.2e}",
            'attack_estimates': results,
            'security_level': self._get_brute_force_security_level(length, charset_size)
        }
    
    def _get_dictionary_explanation(self, exact_match: bool, contains_common: bool) -> str:
        if exact_match:
            return "Your password is in the top 100 most common passwords. It can be cracked instantly by dictionary attacks."
        elif contains_common:
            return "Your password contains common words. Dictionary attacks may crack it quickly."
        else:
            return "Your password doesn't match common dictionary words. Good protection against dictionary attacks."
    
    def _format_time(self, seconds: float) -> str:
        if seconds < 1:
            return "less than a second"
        elif seconds < 60:
            return f"{int(seconds)} second{'s' if seconds != 1 else ''}"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''}"
        elif seconds < 31536000:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''}"
        elif seconds < 31536000000:
            years = seconds / 31536000
            if years < 1000:
                return f"{years:.2f} years"
            else:
                return f"{years:.0f} years"
        else:
            centuries = seconds / 3153600000
            if centuries < 1000:
                return f"{centuries:.2f} centuries"
            else:
                return "practically infinite"
    
    def _get_brute_force_security_level(self, length: int, charset_size: int) -> str:
        entropy = length * (charset_size.bit_length() if charset_size > 0 else 1)
        
        if entropy >= 100:
            return 'Very Strong'
        elif entropy >= 80:
            return 'Strong'
        elif entropy >= 60:
            return 'Medium'
        elif entropy >= 40:
            return 'Weak'
        else:
            return 'Very Weak'
    
    def _empty_brute_force_result(self) -> Dict:
        return {
            'length': 0,
            'charset_size': 0,
            'charset_components': [],
            'total_combinations': 0,
            'combinations_scientific': '0',
            'attack_estimates': {},
            'security_level': 'Very Weak'
        }
