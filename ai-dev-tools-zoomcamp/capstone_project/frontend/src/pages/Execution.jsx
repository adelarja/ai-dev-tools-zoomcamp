import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';

function Execution() {
    const { processId } = useParams();
    const [inputs, setInputs] = useState([]);
    const [quantities, setQuantities] = useState({});
    const navigate = useNavigate();

    useEffect(() => {
        api.get('/inputs/').then((res) => setInputs(res.data));
    }, []);

    const handleSubmit = async () => {
        try {
            const execRes = await api.post('/executions/', {
                process: processId,
                status: 'SUBMITTED'
            });
            const executionId = execRes.data.id;

            for (const [inputId, qty] of Object.entries(quantities)) {
                if (qty > 0) {
                    await api.post('/usages/', {
                        execution: executionId,
                        input: inputId,
                        quantity: qty
                    });
                }
            }
            alert('Execution recorded successfully!');
            navigate('/');
        } catch (error) {
            console.error(error);
            alert('Error recording execution. Check console for details.');
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Record Execution</h1>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '400px' }}>
                {inputs.map((input) => (
                    <div key={input.id} style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <label>{input.name} ({input.default_unit}): </label>
                        <input
                            type="number"
                            step="0.01"
                            onChange={(e) => setQuantities({ ...quantities, [input.id]: e.target.value })}
                        />
                    </div>
                ))}
            </div>
            <br />
            <button onClick={handleSubmit}>Submit Execution</button>
            <br /><br />
            <button onClick={() => navigate('/')}>Back to Dashboard</button>
        </div>
    );
}

export default Execution;
