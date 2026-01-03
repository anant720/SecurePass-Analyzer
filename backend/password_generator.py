import secrets
import string
from typing import Dict, List


class PasswordGenerator:
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate(self, length: int = 16, include_uppercase: bool = True,
                 include_lowercase: bool = True, include_digits: bool = True,
                 include_special: bool = True, exclude_ambiguous: bool = True) -> Dict:
        if length < 8:
            length = 8
        if length > 128:
            length = 128
        
        charset = ""
        if include_lowercase:
            charset += self.lowercase
        if include_uppercase:
            charset += self.uppercase
        if include_digits:
            charset += self.digits
        if include_special:
            charset += self.special
        
        if not charset:
            charset = self.lowercase + self.uppercase + self.digits
        
        if exclude_ambiguous:
            ambiguous = "0O1lI"
            charset = ''.join(c for c in charset if c not in ambiguous)
        
        password = ''.join(secrets.choice(charset) for _ in range(length))
        
        if include_uppercase and not any(c in self.uppercase for c in password):
            password = self._ensure_char_type(password, self.uppercase, charset)
        if include_lowercase and not any(c in self.lowercase for c in password):
            password = self._ensure_char_type(password, self.lowercase, charset)
        if include_digits and not any(c in self.digits for c in password):
            password = self._ensure_char_type(password, self.digits, charset)
        if include_special and not any(c in self.special for c in password):
            password = self._ensure_char_type(password, self.special, charset)
        
        return {
            'password': password,
            'length': len(password),
            'entropy': self._calculate_entropy(password, charset),
            'charset_size': len(charset),
            'options_used': {
                'include_uppercase': include_uppercase,
                'include_lowercase': include_lowercase,
                'include_digits': include_digits,
                'include_special': include_special,
                'exclude_ambiguous': exclude_ambiguous
            }
        }
    
    def _ensure_char_type(self, password: str, char_type: str, full_charset: str) -> str:
        password_list = list(password)
        import random
        idx = random.randint(0, len(password_list) - 1)
        password_list[idx] = secrets.choice(char_type)
        return ''.join(password_list)
    
    def _calculate_entropy(self, password: str, charset: str) -> float:
        charset_size = len(set(charset))
        length = len(password)
        return length * (charset_size.bit_length() if charset_size > 0 else 1)
    
    def generate_memorable(self, word_count: int = 4, separator: str = "-",
                          capitalize: bool = True, add_number: bool = True) -> Dict:
        words = [
            'apple', 'banana', 'cherry', 'dragon', 'eagle', 'forest', 'garden',
            'hammer', 'island', 'jungle', 'knight', 'lighthouse', 'mountain',
            'ocean', 'palace', 'quasar', 'river', 'sunset', 'tiger', 'universe',
            'violet', 'waterfall', 'xylophone', 'yacht', 'zebra'
        ]
        
        selected_words = [secrets.choice(words) for _ in range(word_count)]
        
        if capitalize:
            selected_words = [w.capitalize() for w in selected_words]
        
        password = separator.join(selected_words)
        
        if add_number:
            password += str(secrets.randbelow(100))
        
        return {
            'password': password,
            'length': len(password),
            'type': 'memorable',
            'word_count': word_count
        }
