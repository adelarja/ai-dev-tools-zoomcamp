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

    const runCode = async () => {
        try {
            const response = await axios.post(`${API_URL}/execute`, {
                code: code,
                language: language,
            });
            setOutput(response.data.output);
        } catch (error) {
            console.error('Error executing code:', error);
            setOutput('Error executing code');
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
