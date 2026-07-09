/**
 * AI MedAssist - Core API Service
 * Handles all communication between frontend and Django backend.
 */

const API = {
    BASE_URL: window.location.origin + '/api',
    
    // ──────────────────────────────────────────
    // Token Management
    // ──────────────────────────────────────────
    getToken() {
        return localStorage.getItem('medassist_access_token');
    },
    
    getRefreshToken() {
        return localStorage.getItem('medassist_refresh_token');
    },
    
    setTokens(access, refresh) {
        localStorage.setItem('medassist_access_token', access);
        localStorage.setItem('medassist_refresh_token', refresh);
    },
    
    clearTokens() {
        localStorage.removeItem('medassist_access_token');
        localStorage.removeItem('medassist_refresh_token');
        localStorage.removeItem('medassist_user');
    },
    
    setUser(user) {
        localStorage.setItem('medassist_user', JSON.stringify(user));
    },
    
    getUser() {
        const data = localStorage.getItem('medassist_user');
        return data ? JSON.parse(data) : null;
    },
    
    isLoggedIn() {
        return !!this.getToken();
    },
    
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    // ──────────────────────────────────────────
    // HTTP Helpers
    // ──────────────────────────────────────────
    async request(endpoint, options = {}) {
        const url = `${this.BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken'),
            ...options.headers
        };
        
        const token = this.getToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        try {
            const response = await fetch(url, {
                ...options,
                headers,
            });
            
            // Handle 401 - try refreshing token
            if (response.status === 401 && this.getRefreshToken()) {
                const refreshed = await this.refreshToken();
                if (refreshed) {
                    headers['Authorization'] = `Bearer ${this.getToken()}`;
                    const retryResponse = await fetch(url, { ...options, headers });
                    return await retryResponse.json();
                } else {
                    this.clearTokens();
                    window.location.href = '/login/';
                    return null;
                }
            }
            
            if (!response.ok) {
                const contentType = response.headers.get("content-type");
                if (contentType && contentType.includes("application/json")) {
                    return await response.json();
                }
                return { status: 'error', message: `Server error: ${response.status}` };
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },
    
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },
    
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },
    
    // ──────────────────────────────────────────
    // Auth API
    // ──────────────────────────────────────────
    async register(userData) {
        const result = await this.post('/register/', userData);
        if (result && result.status === 'success') {
            this.setTokens(result.data.tokens.access, result.data.tokens.refresh);
            this.setUser(result.data.user);
        }
        return result;
    },
    
    async login(username, password) {
        const result = await this.post('/login/', { username, password });
        if (result && result.status === 'success') {
            this.setTokens(result.data.tokens.access, result.data.tokens.refresh);
            this.setUser(result.data.user);
        }
        return result;
    },
    
    async logout() {
        try {
            await this.post('/logout/', { refresh: this.getRefreshToken() });
        } catch (e) {
            // Ignore logout errors
        }
        this.clearTokens();
        window.location.href = '/login/';
    },
    
    async refreshToken() {
        try {
            const response = await fetch(`${this.BASE_URL}/token/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: this.getRefreshToken() }),
            });
            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('medassist_access_token', data.access);
                return true;
            }
        } catch (e) {}
        return false;
    },
    
    async getProfile() {
        return this.get('/profile/');
    },
    
    async updateProfile(data) {
        return this.put('/profile/', data);
    },
    
    // ──────────────────────────────────────────
    // Diagnosis API
    // ──────────────────────────────────────────
    async predict(symptoms, language = 'en', inputMethod = 'text') {
        return this.post('/predict/', {
            symptoms,
            language,
            input_method: inputMethod,
        });
    },
    
    async getHistory() {
        return this.get('/history/');
    },
    
    async getSymptomList() {
        return this.get('/symptoms/');
    },
    
    async getDashboardStats() {
        return this.get('/dashboard/');
    },
    
    // ──────────────────────────────────────────
    // Voice API
    // ──────────────────────────────────────────
    async processVoiceInput(transcript) {
        return this.post('/voice-input/', { transcript });
    },
    
    // ──────────────────────────────────────────
    // Ambulance API
    // ──────────────────────────────────────────
    async requestAmbulance(data) {
        return this.post('/request-ambulance/', data);
    },
    
    async getAmbulanceStatus(id) {
        return this.get(`/ambulance-status/?id=${id}`);
    },
    
    async getEmergencyContacts() {
        return this.get('/emergency-contacts/');
    },
    
    // ──────────────────────────────────────────
    // Hospitals API
    // ──────────────────────────────────────────
    async getHospitals(params = {}) {
        let query = '';
        if (params.city) query += `&city=${params.city}`;
        if (params.type) query += `&type=${params.type}`;
        if (params.emergency) query += `&emergency=true`;
        return this.get(`/hospitals/?${query}`);
    },
    
    // ──────────────────────────────────────────
    // Translation API
    // ──────────────────────────────────────────
    async translate(text, targetLanguage) {
        return this.post('/translate/', {
            text,
            target_language: targetLanguage,
        });
    },
    
    async getTranslations(lang) {
        return this.get(`/translate/?lang=${lang}`);
    },
};


/**
 * Voice Recognition Service
 * Uses browser's Web Speech API for speech-to-text.
 */
const VoiceService = {
    recognition: null,
    isListening: false,
    
    init() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            console.warn('Speech Recognition not supported in this browser.');
            return false;
        }
        
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = false; // Set to false for better stability and less network noise
        this.recognition.maxAlternatives = 1;
        this.recognition.lang = this.currentLang || 'en-IN'; // Default to en-IN for Indian users
        return true;
    },
    
    currentLang: 'en-IN',
    
    setLanguage(lang) {
        const langMap = {
            'en': 'en-IN',
            'hi': 'hi-IN',
            'kn': 'kn-IN',
        };
        this.currentLang = langMap[lang] || 'en-IN';
        if (this.recognition) {
            this.recognition.lang = this.currentLang;
        }
    },
    
    start(onResult, onEnd, onError) {
        // Re-initialize to ensure a fresh state (fixes 'network' and 'busy' errors)
        if (!this.init()) {
            if (onError) onError('Speech Recognition not supported');
            return;
        }
        
        this.recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(r => r[0].transcript)
                .join(' ');
            if (onResult) onResult(transcript, event.results[event.resultIndex].isFinal);
        };
        
        this.recognition.onend = () => {
            this.isListening = false;
            if (onEnd) onEnd();
        };
        
        this.recognition.onerror = (event) => {
            this.isListening = false;
            let errorMsg = event.error;
            if (event.error === 'network') {
                errorMsg = 'Network error: Please check your connection or try again. This service requires a stable internet connection.';
            } else if (event.error === 'not-allowed') {
                errorMsg = 'Microphone access denied. Please enable microphone permissions.';
            }
            if (onError) onError(errorMsg);
        };
        
        try {
            this.recognition.start();
            this.isListening = true;
        } catch (e) {
            console.error('Speech start error:', e);
            this.isListening = false;
            if (onError) onError('Could not start voice recognition');
        }
    },
    
    stop() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
            this.isListening = false;
        }
    }
};


/**
 * UI Helper Utilities
 */
const UIHelpers = {
    showNotification(message, type = 'success') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `medassist-notification medassist-notification--${type}`;
        notification.innerHTML = `
            <div style="
                position: fixed; top: 20px; right: 20px; z-index: 10000;
                padding: 16px 24px; border-radius: 12px;
                font-family: 'Manrope', sans-serif; font-size: 14px;
                color: white; max-width: 400px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                animation: slideIn 0.3s ease-out;
                background: ${type === 'success' ? 'linear-gradient(135deg, #006874, #5cd7e9)' :
                             type === 'error' ? 'linear-gradient(135deg, #ba1a1a, #ff6b6b)' :
                             'linear-gradient(135deg, #785a00, #ffd062)'};
            ">
                <span style="margin-right: 8px;">${type === 'success' ? '✅' : type === 'error' ? '❌' : '⚠️'}</span>
                ${message}
            </div>
        `;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transition = 'opacity 0.3s';
            setTimeout(() => notification.remove(), 300);
        }, 4000);
    },
    
    showLoading(element, text = 'Processing...') {
        if (!element) return;
        element.dataset.originalText = element.innerHTML;
        element.disabled = true;
        element.innerHTML = `
            <span style="display: inline-flex; align-items: center; gap: 8px;">
                <span style="width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3);
                    border-top: 2px solid white; border-radius: 50%;
                    animation: spin 0.8s linear infinite; display: inline-block;"></span>
                ${text}
            </span>
        `;
    },
    
    hideLoading(element) {
        if (!element) return;
        element.disabled = false;
        if (element.dataset.originalText) {
            element.innerHTML = element.dataset.originalText;
        }
    },
    
    formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-US', {
            year: 'numeric', month: 'short', day: 'numeric',
            hour: '2-digit', minute: '2-digit'
        });
    },
    
    getSeverityColor(severity) {
        const colors = {
            'low': '#22c55e',
            'medium': '#f59e0b',
            'high': '#ef4444',
            'critical': '#dc2626',
        };
        return colors[severity] || '#6b7280';
    },
    
    updateAuthUI() {
        const user = API.getUser();
        const loginLinks = document.querySelectorAll('a[href*="login"], [data-auth="login"]');
        const registerLinks = document.querySelectorAll('a[href*="register"], [data-auth="register"]');
        const logoutBtns = document.querySelectorAll('[data-auth="logout"]');
        const userNameEls = document.querySelectorAll('[data-auth="username"]');
        
        if (API.isLoggedIn() && user) {
            loginLinks.forEach(el => el.style.display = 'none');
            registerLinks.forEach(el => el.style.display = 'none');
            logoutBtns.forEach(el => el.style.display = '');
            userNameEls.forEach(el => el.textContent = user.full_name || user.username);
        } else {
            logoutBtns.forEach(el => el.style.display = 'none');
        }
    }
};

// Add keyframe animations
const style = document.createElement('style');
style.textContent = `
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
`;
document.head.appendChild(style);

// Initialize auth UI on page load
document.addEventListener('DOMContentLoaded', () => {
    UIHelpers.updateAuthUI();
});
