import { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000';

const LANGUAGES = [
    { id: 'python', name: 'Python' },
    { id: 'javascript', name: 'JavaScript' },
    { id: 'java', name: 'Java' },
    { id: 'cpp', name: 'C++' },
];

const DEFAULT_CODE = {
    python: '# Write your code here\nprint("Hello World")',
    javascript: '// Write your code here\nconsole.log("Hello World");',
    java: '// Write your code here\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello World");\n    }\n}',
    cpp: '// Write your code here\n#include <iostream>\n\nint main() {\n    std::cout << "Hello World" << std::endl;\n    return 0;\n}',
};

function Interview() {
    const { sessionId } = useParams();
    const [code, setCode] = useState('// Loading...');
    const [output, setOutput] = useState('');
    const [language, setLanguage] = useState('python');
    const ws = useRef(null);
    const isRemoteUpdate = useRef(false);

    useEffect(() => {
        // Fetch initial session data
        const fetchSession = async () => {
            try {
                const response = await axios.get(`${API_URL}/sessions/${sessionId}`);
                setLanguage(response.data.language);
                // Only set default code if DB is empty, otherwise use DB content
                if (response.data.code_content) {
                    setCode(response.data.code_content);
                } else {
                    setCode(DEFAULT_CODE[response.data.language] || '');
                }
            } catch (error) {
                console.error('Error fetching session:', error);
            }
        };

        fetchSession();

        // Connect to WebSocket
        ws.current = new WebSocket(`${WS_URL}/ws/${sessionId}`);

        ws.current.onopen = () => {
            console.log('Connected to WebSocket');
        };

        ws.current.onmessage = (event) => {
            const message = JSON.parse(event.data);

            if (message.type === 'code') {
                isRemoteUpdate.current = true;
                setCode(message.payload);
                // Reset flag after a short delay
                setTimeout(() => {
                    isRemoteUpdate.current = false;
                }, 50);
            } else if (message.type === 'language') {
                setLanguage(message.payload);
            }
        };

        return () => {
            if (ws.current) {
                ws.current.close();
            }
        };
    }, [sessionId]);

    const handleEditorChange = (value) => {
        if (isRemoteUpdate.current) return;
        setCode(value);
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'code', payload: value }));
        }
    };

    const handleLanguageChange = (e) => {
        const newLang = e.target.value;
        setLanguage(newLang);

        // Update code to default for new language
        const newCode = DEFAULT_CODE[newLang] || '';
        setCode(newCode);

        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: 'language', payload: newLang }));
            ws.current.send(JSON.stringify({ type: 'code', payload: newCode }));
        }
    };

    const pyodideRef = useRef(null);

    useEffect(() => {
        // Initialize Pyodide
        const loadPyodide = async () => {
            if (window.loadPyodide && !pyodideRef.current) {
                try {
                    pyodideRef.current = await window.loadPyodide();
                    console.log("Pyodide loaded");
                } catch (err) {
                    console.error("Failed to load Pyodide:", err);
                }
            }
        };
        loadPyodide();
    }, []);

    const runCode = async () => {
        setOutput('Running...');

        if (language === 'python') {
            if (!pyodideRef.current) {
                setOutput('Python environment is loading... please wait.');
                return;
            }
            try {
                // Redirect stdout
                pyodideRef.current.runPython(`
import sys
import io
sys.stdout = io.StringIO()
`);
                await pyodideRef.current.runPythonAsync(code);
                const stdout = pyodideRef.current.runPython("sys.stdout.getvalue()");
                setOutput(stdout);
            } catch (err) {
                setOutput(String(err));
            }
        } else if (language === 'javascript') {
            try {
                const logs = [];
                const originalLog = console.log;
                console.log = (...args) => {
                    logs.push(args.map(arg => String(arg)).join(' '));
                    originalLog(...args);
                };

                // Execute JS safely-ish
                // Note: new Function is still eval, but runs in global scope usually.
                // We wrap it to capture console.log
                new Function(code)();

                console.log = originalLog;
                setOutput(logs.join('\n'));
            } catch (err) {
                setOutput(String(err));
            }
        } else if (language === 'cpp') {
            try {
                if (!window.JSCPP) {
                    setOutput('JSCPP library not loaded.');
                    return;
                }
                const config = {
                    stdio: {
                        write: (s) => {
                            setOutput(prev => prev + s);
                        }
                    }
                };
                setOutput(''); // Clear output
                const engine = new window.JSCPP(code, config);
                engine.run();
            } catch (err) {
                setOutput(String(err));
            }
        } else if (language === 'java') {
            // CheerpJ 3.0 requires initialization
            if (!window.cheerpjInit) {
                setOutput('CheerpJ not loaded.');
                return;
            }

            // Note: CheerpJ runs compiled .class or .jar files. 
            // Running raw source code (.java) requires a compiler (javac) running in the browser.
            // This is complex to set up in a simple demo.
            // For now, we will display a message explaining this limitation.

            setOutput('Java execution requires compiling source code to bytecode first.\n' +
                'Client-side compilation (javac in browser) is heavy and not fully implemented in this demo.\n' +
                'Please use Python, JavaScript, or C++ (interpreted) for client-side execution.');

            /* 
            // Experimental: If we had a way to compile, we would do:
            await cheerpjInit();
            const cj = await cheerpjRunMain("Main", "/app/classpath", ...);
            */
        } else {
            setOutput(`Client-side execution for ${language} is not supported yet.`);
        }
    };

    return (
        <div className="interview-container">
            <div className="editor-panel">
                <div className="toolbar">
                    <select
                        className="language-select"
                        value={language}
                        onChange={handleLanguageChange}
                    >
                        {LANGUAGES.map(lang => (
                            <option key={lang.id} value={lang.id}>{lang.name}</option>
                        ))}
                    </select>
                    <button className="btn-run" onClick={runCode}>
                        Run Code
                    </button>
                </div>
                <Editor
                    height="100%"
                    language={language}
                    value={code}
                    onChange={handleEditorChange}
                    theme="vs-dark"
                    options={{
                        minimap: { enabled: false },
                        fontSize: 14,
                        padding: { top: 10 },
                    }}
                />
            </div>
            <div className="output-panel">
                <div className="output-header">Output</div>
                <div className="output-content">
                    {output || 'Run code to see output...'}
                </div>
            </div>
        </div>
    );
}

export default Interview;
