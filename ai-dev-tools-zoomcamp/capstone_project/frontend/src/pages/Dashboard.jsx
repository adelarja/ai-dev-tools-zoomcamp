import { useEffect, useState } from 'react';
import api from '../api';
import { Link } from 'react-router-dom';

function Dashboard() {
    const [processes, setProcesses] = useState([]);

    useEffect(() => {
        api.get('/processes/').then((res) => setProcesses(res.data)).catch(err => console.error(err));
    }, []);

    return (
        <div style={{ padding: '20px' }}>
            <h1>Dashboard</h1>
            <h2>Available Processes</h2>
            <ul>
                {processes.map((p) => (
                    <li key={p.id} style={{ marginBottom: '10px' }}>
                        <strong>{p.name}</strong>: {p.description} <br />
                        <Link to={`/execution/${p.id}`}>Execute Process</Link>
                    </li>
                ))}
            </ul>
            <button onClick={() => {
                localStorage.removeItem('token');
                window.location.href = '/login';
            }}>Logout</button>
        </div>
    );
}

export default Dashboard;
