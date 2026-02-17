const { useState, useEffect } = React;

// API Configuration
const API_URL = 'http://localhost:8001';

function App() {
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [tickets, setTickets] = useState([]);
    const [stats, setStats] = useState(null);

    // Fetch tickets on mount
    useEffect(() => {
        fetchTickets();
        fetchStats();
    }, []);

    const fetchTickets = async () => {
        try {
            const response = await fetch(`${API_URL}/tickets`);
            const data = await response.json();
            setTickets(data.tickets);
        } catch (err) {
            console.error('Error fetching tickets:', err);
        }
    };

    const fetchStats = async () => {
        try {
            const response = await fetch(`${API_URL}/tickets/stats`);
            const data = await response.json();
            setStats(data);
        } catch (err) {
            console.error('Error fetching stats:', err);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!message.trim() || message.length < 10) {
            setError('Message must be at least 10 characters long');
            return;
        }

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await fetch(`${API_URL}/tickets`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_message: message })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to create ticket');
            }

            const data = await response.json();
            setResult(data);
            setMessage('');
            
            // Refresh tickets and stats
            await fetchTickets();
            await fetchStats();
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <header className="header">
                <h1>🤖 Nexus AI</h1>
                <p>Intelligent Ticket Classification System</p>
            </header>

            <div className="container">
                {/* Left Column: Submit Ticket */}
                <div className="card">
                    <h2>📝 Submit Ticket</h2>
                    <form onSubmit={handleSubmit} className="ticket-form">
                        <textarea
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                            placeholder="Describe your issue or request... (minimum 10 characters)"
                            disabled={loading}
                        />
                        <button type="submit" disabled={loading}>
                            {loading ? (
                                <span><span className="loading"></span> Analyzing...</span>
                            ) : (
                                '🚀 Submit & Classify'
                            )}
                        </button>
                    </form>

                    {/* Result Display */}
                    {result && (
                        <div className="result success">
                            <h3>✅ Classification Result</h3>
                            <div className="result-item">
                                <span className="result-label">Category:</span>
                                <span>{result.category}</span>
                            </div>
                            <div className="result-item">
                                <span className="result-label">Urgency:</span>
                                <span className={`badge badge-${result.urgency.toLowerCase()}`}>
                                    {result.urgency}
                                </span>
                            </div>
                            <div className="result-item">
                                <span className="result-label">Sentiment:</span>
                                <span className={`badge badge-${result.sentiment.toLowerCase()}`}>
                                    {result.sentiment}
                                </span>
                            </div>
                            <div className="result-item">
                                <span className="result-label">Confidence:</span>
                                <span>{(result.confidence * 100).toFixed(1)}%</span>
                            </div>
                            <div className="result-item">
                                <span className="result-label">Model:</span>
                                <span style={{fontSize: '0.85em'}}>{result.model_version}</span>
                            </div>
                        </div>
                    )}

                    {/* Error Display */}
                    {error && (
                        <div className="result error">
                            <strong>❌ Error:</strong> {error}
                        </div>
                    )}
                </div>

                {/* Right Column: Statistics */}
                <div className="card">
                    <h2>📊 Statistics</h2>
                    {stats ? (
                        <div className="stats-grid">
                            <div className="stat-card">
                                <div className="stat-number">{stats.total_tickets}</div>
                                <div className="stat-label">Total Tickets</div>
                            </div>
                            <div className="stat-card">
                                <div className="stat-number">
                                    {(stats.avg_confidence * 100).toFixed(0)}%
                                </div>
                                <div className="stat-label">Avg Confidence</div>
                            </div>
                        </div>
                    ) : (
                        <div className="empty-state">Loading stats...</div>
                    )}

                    {stats && (
                        <>
                            <h3 style={{marginTop: '20px', marginBottom: '10px'}}>By Category</h3>
                            {Object.entries(stats.by_category || {}).map(([category, count]) => (
                                <div key={category} className="result-item">
                                    <span>{category}</span>
                                    <span className="badge badge-medium">{count}</span>
                                </div>
                            ))}

                            <h3 style={{marginTop: '20px', marginBottom: '10px'}}>By Urgency</h3>
                            {Object.entries(stats.by_urgency || {}).map(([urgency, count]) => (
                                <div key={urgency} className="result-item">
                                    <span>{urgency}</span>
                                    <span className={`badge badge-${urgency.toLowerCase()}`}>{count}</span>
                                </div>
                            ))}
                        </>
                    )}
                </div>
            </div>

            {/* Ticket List */}
            <div className="card">
                <h2>🎫 Recent Tickets</h2>
                <div className="ticket-list">
                    {tickets.length === 0 ? (
                        <div className="empty-state">
                            <p>No tickets yet. Submit your first ticket above!</p>
                        </div>
                    ) : (
                        tickets.map((ticket) => (
                            <div key={ticket.id} className="ticket-item">
                                <div className="ticket-message">"{ticket.user_message}"</div>
                                <div className="ticket-meta">
                                    <span><strong>ID:</strong> #{ticket.id}</span>
                                    <span><strong>Category:</strong> {ticket.category}</span>
                                    <span className={`badge badge-${ticket.urgency.toLowerCase()}`}>
                                        {ticket.urgency}
                                    </span>
                                    <span className={`badge badge-${ticket.sentiment.toLowerCase()}`}>
                                        {ticket.sentiment}
                                    </span>
                                    <span><strong>Confidence:</strong> {(ticket.confidence * 100).toFixed(1)}%</span>
                                    <span style={{fontSize: '0.85em', color: '#6c757d'}}>
                                        {ticket.model_version}
                                    </span>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}

// Render the app
ReactDOM.render(<App />, document.getElementById('root'));
