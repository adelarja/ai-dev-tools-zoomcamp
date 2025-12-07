import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = import.meta.env.DEV ? 'http://localhost:8000' : '';

function Home() {
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const createSession = async () => {
        setLoading(true);
        try {
            const response = await axios.post(`${API_URL}/sessions/`, { language: 'python' });
            navigate(`/interview/${response.data.id}`);
        } catch (error) {
            console.error('Error creating session:', error);
            alert('Failed to create session');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="home-container">
            <div className="card">
                <h1>Coding Interview App</h1>
                <p>Create a new session to start interviewing.</p>
                <button className="btn-primary" onClick={createSession} disabled={loading}>
                    {loading ? 'Creating...' : 'Create New Interview'}
                </button>
            </div>
        </div>
    );
}

export default Home;
