import { useState } from 'react';
import './App.css';

export default function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);

  async function handleSearch() {
    console.log('search clicked', query);
    setLoading(true);
    const response = await fetch('http://localhost:8000/api/landscape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query, max_results: 10 })
    });
    const data = await response.json();
    setResults(data.papers);
    setLoading(false);
  }

  return (
    <div className="app">
      <div className="header">
        <h1>ML Research Landscape</h1>
        <p>Search any ML topic to map the research landscape</p>
      </div>
      <div className="search-row">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder='e.g. "RAG", "diffusion models", "RLHF"'
        />
        <button onClick={handleSearch}>Search</button>
      </div>
      {loading && <p className="loading">Loading...</p>}
      {results && results.themes && results.themes.map((theme) => (
        <div key={theme.name} className="theme-section">
          <h2 className="theme-title">{theme.name}</h2>
          {results.papers
            .filter(paper => paper.theme === theme.name)
            .map(paper => (
              <div key={paper.arxiv_id} className="paper-card">
                <h3>{paper.title}</h3>
                <p className="paper-date">{paper.published.slice(0, 10)}</p>
                <p className="paper-tags">{paper.tags.join(', ')}</p>
                <p className="paper-summary">{paper.summary}</p>
                <a className="paper-link" href={paper.pdf_url} target="_blank">Read paper</a>
              </div>
            ))
          }
        </div>
      ))}
    </div>
  );
}