const API_BASE_URL = 'http://localhost:5000/api';

const passwordInput = document.getElementById('passwordInput');
const toggleVisibility = document.getElementById('toggleVisibility');
const copyBtn = document.getElementById('copyBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const generateBtn = document.getElementById('generateBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const results = document.getElementById('results');
const errorMessage = document.getElementById('errorMessage');

const generatorPanel = document.getElementById('generatorPanel');
const closeGenerator = document.getElementById('closeGenerator');
const generatePasswordBtn = document.getElementById('generatePasswordBtn');
const genLength = document.getElementById('genLength');
const lengthValue = document.getElementById('lengthValue');

const strengthBar = document.getElementById('strengthBar');
const strengthLevel = document.getElementById('strengthLevel');
const strengthScore = document.getElementById('strengthScore');
const crackTime = document.getElementById('crackTime');
const customScore = document.getElementById('customScore');
const zxcvbnScore = document.getElementById('zxcvbnScore');

const breachStatus = document.getElementById('breachStatus');
const breachMessage = document.getElementById('breachMessage');
const breachRecommendation = document.getElementById('breachRecommendation');

const dictVulnerability = document.getElementById('dictVulnerability');
const dictExplanation = document.getElementById('dictExplanation');
const bfLength = document.getElementById('bfLength');
const bfCharset = document.getElementById('bfCharset');
const bfCombinations = document.getElementById('bfCombinations');
const bfOnline = document.getElementById('bfOnline');
const bfOfflineFast = document.getElementById('bfOfflineFast');
const bfOfflineSlow = document.getElementById('bfOfflineSlow');

const suggestionsList = document.getElementById('suggestionsList');
const issuesSection = document.getElementById('issuesSection');
const issuesList = document.getElementById('issuesList');

analyzeBtn.addEventListener('click', analyzePassword);
generateBtn.addEventListener('click', () => {
    generatorPanel.style.display = generatorPanel.style.display === 'none' ? 'block' : 'none';
});
closeGenerator.addEventListener('click', () => {
    generatorPanel.style.display = 'none';
});
generatePasswordBtn.addEventListener('click', generatePassword);

passwordInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        analyzePassword();
    }
});

passwordInput.addEventListener('input', () => {
    if (passwordInput.value.length > 0) {
        copyBtn.style.display = 'flex';
    } else {
        copyBtn.style.display = 'none';
    }
});

toggleVisibility.addEventListener('click', () => {
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
});

copyBtn.addEventListener('click', async () => {
    const password = passwordInput.value;
    if (!password) return;
    
    try {
        await navigator.clipboard.writeText(password);
        copyBtn.classList.add('copy-success');
        setTimeout(() => {
            copyBtn.classList.remove('copy-success');
        }, 500);
    } catch (err) {
        passwordInput.select();
        document.execCommand('copy');
        copyBtn.classList.add('copy-success');
        setTimeout(() => {
            copyBtn.classList.remove('copy-success');
        }, 500);
    }
});

genLength.addEventListener('input', (e) => {
    lengthValue.textContent = e.target.value;
});

async function analyzePassword() {
    const password = passwordInput.value.trim();
    
    if (!password) {
        showError('Please enter a password to analyze');
        return;
    }
    
    loadingIndicator.style.display = 'block';
    results.style.display = 'none';
    errorMessage.style.display = 'none';
    analyzeBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password: password })
        });
        
        if (!response.ok) {
            if (response.status === 429) {
                throw new Error('Rate limit exceeded. Please wait a minute before trying again.');
            }
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to analyze password');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        showError(error.message || 'An error occurred while analyzing the password');
    } finally {
        loadingIndicator.style.display = 'none';
        analyzeBtn.disabled = false;
    }
}

function displayResults(data) {
    displayStrength(data.strength);
    
    displayBreach(data.breach_check);
    
    displayDictionaryAttack(data.dictionary_attack);
    displayBruteForce(data.brute_force);
    
    displaySuggestions(data.strength.suggestions);
    displayIssues(data.strength.issues);
    
    results.style.display = 'block';
}

function displayStrength(strength) {
    const score = strength.final_score;
    const level = strength.strength_level;
    const color = strength.strength_color;
    
    strengthBar.style.width = `${score}%`;
    strengthBar.style.background = color;
    
    strengthLevel.textContent = level;
    strengthLevel.style.color = color;
    strengthScore.textContent = `${score}/100`;
    
    crackTime.textContent = strength.crack_time_human;
    customScore.textContent = `${strength.custom_score}`;
    zxcvbnScore.textContent = `${strength.zxcvbn_score}/4`;
}

function displayBreach(breach) {
    if (breach.breached) {
        breachStatus.className = 'breach-status breached';
        breachStatus.innerHTML = `
            <span class="breach-icon">🚨</span>
            <span class="breach-message">${breach.message}</span>
        `;
    } else {
        breachStatus.className = 'breach-status safe';
        breachStatus.innerHTML = `
            <span class="breach-icon">✅</span>
            <span class="breach-message">${breach.message}</span>
        `;
    }
    
    breachRecommendation.textContent = breach.recommendation;
}

function displayDictionaryAttack(dict) {
    const level = dict.vulnerability_level.toLowerCase();
    dictVulnerability.textContent = dict.vulnerability_level;
    dictVulnerability.className = `vulnerability-badge ${level}`;
    dictExplanation.textContent = dict.explanation;
}

function displayBruteForce(bf) {
    bfLength.textContent = `${bf.length} characters`;
    
    const charsetComponents = bf.charset_components || [];
    bfCharset.textContent = charsetComponents.length > 0 
        ? charsetComponents.join(', ').toUpperCase()
        : 'Unknown';
    
    bfCombinations.textContent = bf.combinations_scientific || '0';
    
    if (bf.attack_estimates) {
        bfOnline.textContent = bf.attack_estimates.online?.human_readable || '-';
        bfOfflineFast.textContent = bf.attack_estimates.offline_fast?.human_readable || '-';
        bfOfflineSlow.textContent = bf.attack_estimates.offline_slow?.human_readable || '-';
    }
}

function displaySuggestions(suggestions) {
    suggestionsList.innerHTML = '';
    
    if (!suggestions || suggestions.length === 0) {
        suggestionsList.innerHTML = '<li>No suggestions. Your password looks good!</li>';
        return;
    }
    
    suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = `💡 ${suggestion}`;
        suggestionsList.appendChild(li);
    });
}

function displayIssues(issues) {
    issuesList.innerHTML = '';
    
    if (!issues || issues.length === 0) {
        issuesSection.style.display = 'none';
        return;
    }
    
    issuesSection.style.display = 'block';
    
    issues.forEach(issue => {
        const li = document.createElement('li');
        li.textContent = `⚠️ ${issue}`;
        issuesList.appendChild(li);
    });
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    results.style.display = 'none';
}

async function generatePassword() {
    const length = parseInt(genLength.value);
    const includeUppercase = document.getElementById('genUppercase').checked;
    const includeLowercase = document.getElementById('genLowercase').checked;
    const includeDigits = document.getElementById('genDigits').checked;
    const includeSpecial = document.getElementById('genSpecial').checked;
    const excludeAmbiguous = document.getElementById('genExcludeAmbiguous').checked;
    const genType = document.querySelector('input[name="genType"]:checked').value;
    
    generatePasswordBtn.disabled = true;
    generatePasswordBtn.textContent = 'Generating...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                length: length,
                include_uppercase: includeUppercase,
                include_lowercase: includeLowercase,
                include_digits: includeDigits,
                include_special: includeSpecial,
                exclude_ambiguous: excludeAmbiguous,
                memorable: genType === 'memorable',
                word_count: 4,
                separator: '-',
                capitalize: true,
                add_number: true
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate password');
        }
        
        const data = await response.json();
        passwordInput.value = data.password;
        passwordInput.setAttribute('type', 'text');
        copyBtn.style.display = 'flex';
        
        setTimeout(() => {
            analyzePassword();
        }, 300);
        
    } catch (error) {
        showError('Failed to generate password: ' + error.message);
    } finally {
        generatePasswordBtn.disabled = false;
        generatePasswordBtn.textContent = 'Generate Password';
    }
}

window.addEventListener('load', async () => {
    try {
        const response = await fetch('http://localhost:5000/health');
        if (!response.ok) {
            showError('Backend API is not available. Please make sure the Flask server is running.');
        }
    } catch (error) {
        showError('Cannot connect to backend API. Please start the Flask server (python backend/app.py)');
    }
});
