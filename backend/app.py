from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from typing import Dict

from strength_checker import StrengthChecker
from attack_simulator import AttackSimulator
from breach_checker import BreachChecker
from password_generator import PasswordGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5 per minute"],
    storage_uri="memory://"
)

strength_checker = StrengthChecker()
attack_simulator = AttackSimulator()
breach_checker = BreachChecker()
password_generator = PasswordGenerator()


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'Password Analyzer API'}), 200


@app.route('/api/analyze', methods=['POST'])
@limiter.limit("5 per minute")
def analyze_password():
    try:
        data = request.get_json()
        
        if not data or 'password' not in data:
            return jsonify({
                'error': 'Password is required',
                'message': 'Please provide a password in the request body'
            }), 400
        
        password = data['password']
        
        logger.info(f"Password analysis requested (length: {len(password) if password else 0})")
        
        strength_result = strength_checker.analyze(password)
        dictionary_result = attack_simulator.dictionary_attack(password)
        brute_force_result = attack_simulator.brute_force_estimate(password)
        breach_result = breach_checker.check(password)
        
        result = {
            'strength': strength_result,
            'dictionary_attack': dictionary_result,
            'brute_force': brute_force_result,
            'breach_check': breach_result,
            'timestamp': None
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error analyzing password: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An error occurred while analyzing the password'
        }), 500


@app.route('/api/strength', methods=['POST'])
@limiter.limit("5 per minute")
def check_strength():
    try:
        data = request.get_json()
        
        if not data or 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
        
        password = data['password']
        result = strength_checker.analyze(password)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error checking strength: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/breach', methods=['POST'])
@limiter.limit("5 per minute")
def check_breach():
    try:
        data = request.get_json()
        
        if not data or 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
        
        password = data['password']
        result = breach_checker.check(password)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error checking breach: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/generate', methods=['POST'])
@limiter.limit("10 per minute")
def generate_password():
    try:
        data = request.get_json() or {}
        
        length = data.get('length', 16)
        include_uppercase = data.get('include_uppercase', True)
        include_lowercase = data.get('include_lowercase', True)
        include_digits = data.get('include_digits', True)
        include_special = data.get('include_special', True)
        exclude_ambiguous = data.get('exclude_ambiguous', True)
        memorable = data.get('memorable', False)
        
        if memorable:
            word_count = data.get('word_count', 4)
            result = password_generator.generate_memorable(
                word_count=word_count,
                separator=data.get('separator', '-'),
                capitalize=data.get('capitalize', True),
                add_number=data.get('add_number', True)
            )
        else:
            result = password_generator.generate(
                length=length,
                include_uppercase=include_uppercase,
                include_lowercase=include_lowercase,
                include_digits=include_digits,
                include_special=include_special,
                exclude_ambiguous=exclude_ambiguous
            )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error generating password: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': 'Too many requests. Please try again in a minute.'
    }), 429


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
