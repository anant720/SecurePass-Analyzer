import re
from typing import Dict, List, Tuple


class PasswordRules:
    
    COMMON_PATTERNS = [
        r'12345', r'abcde', r'qwerty', r'password', r'admin',
        r'welcome', r'letmein', r'monkey', r'dragon', r'master'
    ]
    
    SEQUENTIAL_PATTERNS = [
        '0123456789', 'abcdefghijklmnopqrstuvwxyz',
        'qwertyuiop', 'asdfghjkl', 'zxcvbnm'
    ]
    
    def __init__(self):
        self.score = 0
        self.issues = []
        self.suggestions = []
    
    def check_length(self, password: str) -> Tuple[int, List[str]]:
        score = 0
        issues = []
        suggestions = []
        
        length = len(password)
        
        if length >= 16:
            score = 25
        elif length >= 12:
            score = 20
        elif length >= 8:
            score = 10
            suggestions.append("Use at least 12 characters for better security")
        else:
            score = 0
            issues.append(f"Password is too short ({length} characters)")
            suggestions.append("Use at least 12 characters")
        
        return score, issues, suggestions
    
    def check_uppercase(self, password: str) -> Tuple[int, List[str], List[str]]:
        score = 0
        issues = []
        suggestions = []
        
        if re.search(r'[A-Z]', password):
            score = 10
        else:
            issues.append("Missing uppercase letters")
            suggestions.append("Add uppercase letters (A-Z)")
        
        return score, issues, suggestions
    
    def check_lowercase(self, password: str) -> Tuple[int, List[str], List[str]]:
        score = 0
        issues = []
        suggestions = []
        
        if re.search(r'[a-z]', password):
            score = 10
        else:
            issues.append("Missing lowercase letters")
            suggestions.append("Add lowercase letters (a-z)")
        
        return score, issues, suggestions
    
    def check_numbers(self, password: str) -> Tuple[int, List[str], List[str]]:
        score = 0
        issues = []
        suggestions = []
        
        if re.search(r'[0-9]', password):
            score = 10
        else:
            issues.append("Missing numbers")
            suggestions.append("Add numbers (0-9)")
        
        return score, issues, suggestions
    
    def check_special_chars(self, password: str) -> Tuple[int, List[str], List[str]]:
        score = 0
        issues = []
        suggestions = []
        
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password):
            score = 15
        else:
            issues.append("Missing special characters")
            suggestions.append("Add special characters (!@#$%^&*)")
        
        return score, issues, suggestions
    
    def check_repeated_chars(self, password: str) -> Tuple[int, List[str], List[str]]:
        score = 0
        issues = []
        suggestions = []
        
        if re.search(r'(.)\1{2,}', password):
            score = -10
            issues.append("Contains repeated characters")
            suggestions.append("Avoid repeating the same character multiple times")
        else:
            score = 0
        
        return score, issues, suggestions
    
    def check_common_patterns(self, password: str) -> Tuple[int, List[str], List[str]]:
        score = 0
        issues = []
        suggestions = []
        
        password_lower = password.lower()
        
        for pattern in self.COMMON_PATTERNS:
            if re.search(pattern, password_lower, re.IGNORECASE):
                score = -15
                issues.append(f"Contains common pattern: {pattern}")
                suggestions.append("Avoid common words and patterns")
                break
        
        return score, issues, suggestions
    
    def check_sequential_patterns(self, password: str) -> Tuple[int, List[str], List[str]]:
        score = 0
        issues = []
        suggestions = []
        
        password_lower = password.lower()
        
        for seq in self.SEQUENTIAL_PATTERNS:
            for i in range(len(seq) - 2):
                pattern = seq[i:i+4]
                if pattern in password_lower:
                    score = -10
                    issues.append("Contains sequential characters")
                    suggestions.append("Avoid sequential patterns (abc, 123, qwerty)")
                    break
            if score < 0:
                break
        
        return score, issues, suggestions
    
    def analyze(self, password: str) -> Dict:
        if not password:
            return {
                'score': 0,
                'issues': ['Password is empty'],
                'suggestions': ['Enter a password to analyze'],
                'rules_passed': 0,
                'rules_total': 7
            }
        
        total_score = 0
        all_issues = []
        all_suggestions = []
        rules_passed = 0
        rules_total = 7
        
        checks = [
            self.check_length,
            self.check_uppercase,
            self.check_lowercase,
            self.check_numbers,
            self.check_special_chars,
            self.check_repeated_chars,
            self.check_common_patterns,
            self.check_sequential_patterns
        ]
        
        for check in checks:
            score, issues, suggestions = check(password)
            total_score += score
            all_issues.extend(issues)
            all_suggestions.extend(suggestions)
            if score > 0:
                rules_passed += 1
        
        total_score = max(0, total_score)
        
        return {
            'score': total_score,
            'issues': list(set(all_issues)),
            'suggestions': list(set(all_suggestions)),
            'rules_passed': rules_passed,
            'rules_total': rules_total
        }
