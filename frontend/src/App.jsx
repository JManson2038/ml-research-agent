import { useState } from 'react';
import './App.css';
import ThemeCard from './components/ThemeCard';

export default function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [sortorder, setSortOrder] = useState('newest');

  async function handleSearch(searchTerm = query) {
    setLoading(true);
    const response = await fetch('http://localhost:8000/api/landscape', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: searchTerm, max_results: 10 })
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
          onKeyPress={(e) => { if (e.key === 'Enter') handleSearch(); }}
          placeholder='e.g. "RAG", "diffusion models", "RLHF"'
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {loading && (
        <div className="spinner-wrapper">
          <div className="spinner"></div>
        </div>
      )}

      {results && results.themes && (
        <>
          <div className="sort-row">
            <label>Sort by:</label>
            <select value={sortorder} onChange={(e) => setSortOrder(e.target.value)}>
              <option value="newest">Newest</option>
              <option value="oldest">Oldest</option>
            </select>
          </div>
          <div className="Reset-button">
            <button onClick={() => { setResults([]); setQuery(''); }}>Clear results</button>
          </div>
          {results.themes.map((theme) => {
            const sortedPapers = results.papers
              .filter(paper => paper.theme === theme.name)
              .sort((a, b) => sortorder === 'newest'
                ? new Date(b.published) - new Date(a.published)
                : new Date(a.published) - new Date(b.published));
            return <ThemeCard key={theme.name} theme={theme} papers={sortedPapers} onAuthorClick={handleSearch} />;
          })}
        </>
      )}
    </div>
  );
}