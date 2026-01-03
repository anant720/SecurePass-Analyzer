from typing import Dict
import zxcvbn
from password_rules import PasswordRules


class StrengthChecker:
    
    def __init__(self):
        self.rules_engine = PasswordRules()
    
    def analyze(self, password: str) -> Dict:
        if not password:
            return self._empty_result()
        
        rules_result = self.rules_engine.analyze(password)
        
        zxcvbn_result = zxcvbn.zxcvbn(password)
        
        custom_score = rules_result['score']
        zxcvbn_score = zxcvbn_result['score']
        zxcvbn_weighted = zxcvbn_score * 20
        
        final_score = (custom_score + zxcvbn_weighted) / 2
        final_score = min(100, max(0, final_score))
        
        strength_level = self._get_strength_level(final_score)
        
        crack_time = zxcvbn_result['crack_times_seconds']['offline_slow_hashing_1e4_per_second']
        crack_time_human = self._format_crack_time(crack_time)
        
        feedback = zxcvbn_result.get('feedback', {})
        zxcvbn_warnings = feedback.get('warning', '')
        zxcvbn_suggestions = feedback.get('suggestions', [])
        
        all_suggestions = list(set(rules_result['suggestions'] + zxcvbn_suggestions))
        
        return {
            'final_score': round(final_score, 1),
            'strength_level': strength_level,
            'strength_color': self._get_strength_color(strength_level),
            'custom_score': round(custom_score, 1),
            'zxcvbn_score': zxcvbn_score,
            'zxcvbn_score_weighted': round(zxcvbn_weighted, 1),
            'crack_time_seconds': crack_time,
            'crack_time_human': crack_time_human,
            'issues': rules_result['issues'],
            'suggestions': all_suggestions,
            'rules_passed': rules_result['rules_passed'],
            'rules_total': rules_result['rules_total'],
            'zxcvbn_warning': zxcvbn_warnings,
            'guesses': zxcvbn_result['guesses'],
            'guesses_log10': zxcvbn_result['guesses_log10']
        }
    
    def _get_strength_level(self, score: float) -> str:
        if score >= 80:
            return 'Very Strong'
        elif score >= 60:
            return 'Strong'
        elif score >= 40:
            return 'Medium'
        elif score >= 20:
            return 'Weak'
        else:
            return 'Very Weak'
    
    def _get_strength_color(self, level: str) -> str:
        colors = {
            'Very Strong': '#0066cc',
            'Strong': '#00cc00',
            'Medium': '#ff9900',
            'Weak': '#ff6600',
            'Very Weak': '#cc0000'
        }
        return colors.get(level, '#666666')
    
    def _format_crack_time(self, seconds: float) -> str:
        if seconds < 1:
            return "instant"
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
            if years < 100:
                return f"{years:.1f} years"
            else:
                return f"{years:.0f} years"
        else:
            centuries = seconds / 3153600000
            return f"{centuries:.1f} centuries"
    
    def _empty_result(self) -> Dict:
        return {
            'final_score': 0,
            'strength_level': 'Very Weak',
            'strength_color': '#cc0000',
            'custom_score': 0,
            'zxcvbn_score': 0,
            'zxcvbn_score_weighted': 0,
            'crack_time_seconds': 0,
            'crack_time_human': 'instant',
            'issues': ['Password is empty'],
            'suggestions': ['Enter a password to analyze'],
            'rules_passed': 0,
            'rules_total': 7,
            'zxcvbn_warning': '',
            'guesses': 0,
            'guesses_log10': 0
        }
