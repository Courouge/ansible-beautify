import React, { useState, useCallback, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
    // Main component state
    const [inputText, setInputText] = useState('');
    const [outputText, setOutputText] = useState('');
    const [loading, setLoading] = useState(false);
    const [validationError, setValidationError] = useState('');
    const [copied, setCopied] = useState(false);
    const [darkMode, setDarkMode] = useState(() => {
        const saved = localStorage.getItem('darkMode');
        return saved ? JSON.parse(saved) : false;
    });

    // Ansible one-liner examples
    const examples = [
        '  apt: name=nginx state=present update_cache=yes',
        '  service: name=apache2 state=started enabled=yes',
        '  user: name=myuser shell=/bin/bash groups=sudo append=yes',
        '  copy: src=/tmp/foo dest=/etc/foo backup=yes mode=0644',
        '  template: src=nginx.conf.j2 dest=/etc/nginx/nginx.conf notify="restart nginx"',
        '  shell: echo "Hello World" | grep Hello',
        '  command: /usr/bin/make install',
        '  git: repo=https://github.com/ansible/ansible.git dest=/srv/checkout version=release-0.4',
        '  file: path=/etc/foo.conf state=absent',
        '  lineinfile: path=/etc/hosts line="127.0.0.1 localhost" state=present'
    ];

    // Dark mode toggle
    const toggleDarkMode = useCallback(() => {
        setDarkMode(prev => {
            const newMode = !prev;
            localStorage.setItem('darkMode', JSON.stringify(newMode));
            return newMode;
        });
    }, []);

    // Apply dark mode class to body
    useEffect(() => {
        if (darkMode) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    }, [darkMode]);

    // Reset copied state after 2 seconds
    useEffect(() => {
        if (copied) {
            const timer = setTimeout(() => setCopied(false), 2000);
            return () => clearTimeout(timer);
        }
    }, [copied]);

    // Handle input changes
    const handleInputChange = useCallback((e) => {
        setInputText(e.target.value);
        setValidationError('');
    }, []);

    // Basic validation
    const validateInput = useCallback((text) => {
        if (!text || !text.trim()) {
            return 'Input text cannot be empty';
        }
        
        if (text.length > 10000) {
            return 'Text is too long (maximum 10,000 characters)';
        }

        return '';
    }, []);

    // Ansible transformation
    const transformAnsible = useCallback(async () => {
        const error = validateInput(inputText);
        if (error) {
            setValidationError(error);
            return;
        }

        setLoading(true);
        setValidationError('');
        
        try {
            const response = await fetch('http://localhost:5000/api/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ in: inputText })
            });

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            setOutputText(data.out || '');
            
        } catch (error) {
            console.error('Transformation error:', error);
            setValidationError(`Error: ${error.message}`);
            setOutputText('');
        } finally {
            setLoading(false);
        }
    }, [inputText, validateInput]);

    // Generate example
    const generateExample = useCallback(() => {
        const randomExample = examples[Math.floor(Math.random() * examples.length)];
        setInputText(randomExample);
        setOutputText('');
        setValidationError('');
    }, [examples]);

    // Clear content
    const clearInput = useCallback(() => {
        setInputText('');
        setOutputText('');
        setValidationError('');
    }, []);

    // Copy to clipboard
    const copyToClipboard = useCallback(async () => {
        if (!outputText.trim()) return;
        
        try {
            await navigator.clipboard.writeText(outputText);
            setCopied(true);
        } catch (error) {
            console.error('Copy error:', error);
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = outputText;
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                setCopied(true);
            } catch (fallbackError) {
                console.error('Fallback copy error:', fallbackError);
            }
            document.body.removeChild(textArea);
        }
    }, [outputText]);

    return (
        <div className={`App ${darkMode ? 'dark-theme' : ''}`}>
            <div className="container-fluid">
                {/* Header Section */}
                <div className="header-section text-center py-4 position-relative">
                    <button
                        className="btn btn-outline-secondary position-absolute"
                        style={{ top: '1rem', right: '1rem', borderRadius: '50%', width: '45px', height: '45px' }}
                        onClick={toggleDarkMode}
                        title={darkMode ? 'Light mode' : 'Dark mode'}
                    >
                        {darkMode ? '☀️' : '🌙'}
                    </button>
                    
                    <h1 className="display-4 mb-3">
                        🎨 Ansible Beautify
                    </h1>
                    <p className="lead">
                        Transform your Ansible one-liners into beautiful, readable YAML
                    </p>
                </div>

                {/* Input Section - Full Width */}
                <div className="row mb-4">
                    <div className="col-12">
                        <div className="panel-container">
                            <div className="panel-header">
                                <h5 className="mb-0">
                                    📝 Ansible One-liner
                                </h5>
                                <div className="btn-group btn-group-sm">
                                    <button
                                        className="btn btn-outline-secondary"
                                        onClick={generateExample}
                                        disabled={loading}
                                        title="Generate example"
                                    >
                                        🎲 Example
                                    </button>
                                    <button
                                        className="btn btn-outline-danger"
                                        onClick={clearInput}
                                        disabled={loading || !inputText.trim()}
                                        title="Clear content"
                                    >
                                        🗑️ Clear
                                    </button>
                                </div>
                            </div>
                            
                            <textarea
                                className={`form-control code-textarea ${validationError ? 'is-invalid' : ''}`}
                                value={inputText}
                                onChange={handleInputChange}
                                placeholder="# Ansible one-liner example
  shell: echo 'Hello World' | grep Hello
  
# Or multiple tasks:
  apt: name=nginx state=present
  service: name=nginx state=started enabled=yes"
                                disabled={loading}
                                style={{ minHeight: '200px' }}
                            />
                            
                            {validationError && (
                                <div className="invalid-feedback">
                                    ⚠️ {validationError}
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Action Section - Centered */}
                <div className="row mb-4">
                    <div className="col-12">
                        <div className="action-panel-horizontal">
                            <div className="d-flex justify-content-center align-items-center gap-4 flex-wrap">
                                <button
                                    className="btn transform-btn"
                                    onClick={transformAnsible}
                                    disabled={loading || !inputText.trim()}
                                >
                                    {loading ? (
                                        <>
                                            <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                                            Transforming...
                                        </>
                                    ) : (
                                        <>
                                            ✨ Beautify Ansible
                                        </>
                                    )}
                                </button>
                                
                                <div className="features-horizontal d-none d-md-flex">
                                    <span className="feature-badge">YAML Formatting</span>
                                    <span className="feature-badge">2077+ Modules</span>
                                    <span className="feature-badge">Syntax Validation</span>
                                    <span className="feature-badge">Quick Copy</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Output Section - Full Width */}
                <div className="row mb-4">
                    <div className="col-12">
                        <div className="panel-container">
                            <div className="panel-header">
                                <h5 className="mb-0">
                                    ✨ Beautified YAML
                                </h5>
                                <div className="btn-group btn-group-sm">
                                    <button
                                        className={`btn ${copied ? 'btn-success' : 'btn-outline-primary'}`}
                                        onClick={copyToClipboard}
                                        disabled={!outputText.trim()}
                                        title="Copy to clipboard"
                                    >
                                        {copied ? '✅ Copied!' : '📋 Copy'}
                                    </button>
                                </div>
                            </div>
                            
                            <textarea
                                className="form-control code-textarea output-textarea"
                                value={outputText}
                                readOnly
                                placeholder="The transformed result will appear here...

✨ Use the 'Beautify Ansible' button to get started
🎲 Or generate an example to test quickly"
                                style={{ minHeight: '300px' }}
                            />
                            
                            {outputText && (
                                <div className="output-stats">
                                    ✅ Transform successful • {outputText.split('\n').length} lines • {outputText.length} characters
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Footer */}
                <div className="footer-section text-center py-4">
                    <p className="mb-0 text-muted">
                        Built with ❤️ by{' '}
                        <a href="https://github.com/fcourouge" target="_blank" rel="noopener noreferrer">
                            Florian Courouge
                        </a>
                        {' • '}
                        <a href="https://github.com/fcourouge/ansible-beautify" target="_blank" rel="noopener noreferrer">
                            Source Code
                        </a>
                        {' • '}
                        Powered by React & Flask
                    </p>
                </div>
            </div>
        </div>
    );
}

export default App;
