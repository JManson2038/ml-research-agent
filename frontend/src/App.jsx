import { useState } from 'react';
import './App.css';
import ThemeCard from './components/ThemeCard';

export default function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  const [results, setResults] = useState([]);
  const [sortorder, setSortOrder] = useState('newest');
  const [error, setError] = useState(null);
  const [searchMode, setSearchMode] = useState('topic'); // 'topic' or 'author'


  async function handleSearch(searchTerm = query, isAuthor = searchMode === 'author') {
    setLoading(true);
    setError(null);
    setLoadingMessage('Fetching papers from arxiv...');

    const loadingSteps = [
      'Fetching papers from arxiv...',
      'Summarizing with Claude...',
      'Clustering by theme...'
    ];

    let stepIndex = 0;
    const progressTimer = window.setInterval(() => {
      stepIndex += 1;
      if (stepIndex < loadingSteps.length) {
        setLoadingMessage(loadingSteps[stepIndex]);
      }
    }, 1200);

    try {
      const response = await fetch('https://ml-research-agent.onrender.com/api/landscape', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchTerm, max_results: isAuthor ? 15 : 10, is_author: isAuthor })
      });

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      setResults(data.papers || []);
    } catch (err) {
      setError(err.message || 'Failed to fetch results.');
      setResults([]);
    } finally {
      window.clearInterval(progressTimer);
      setLoading(false);
      setLoadingMessage('');
    }
  }

  return (
    <div className="app">
      <div className="header">
        <h1>ML Research Landscape</h1>
        <p>Search any ML topic to map the research landscape</p>
      </div>
      <div className="search-row">
        <select
          value={searchMode}
          onChange={(e) => setSearchMode(e.target.value)}
          aria-label="Search mode"
        >
          <option value="topic">Topic</option>
          <option value="author">Author</option>
        </select>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={(e) => { if (e.key === 'Enter') handleSearch(); }}
          placeholder='e.g. "RAG", "diffusion models", "RLHF"'
          placeholder={searchMode === 'author' 
            ? 'e.g. "Yoshua Bengio", "Ian Goodfellow"' 
            : 'e.g. "RAG", "diffusion models", "RLHF"'}
        />
        <button onClick={() => handleSearch()}>Search</button>
      </div>

      {loading && (
        <div className="spinner-wrapper">
          <div className="spinner"></div>
          <div className="loading-status">{loadingMessage}</div>
        </div>
      )}

      {error && (
  <div className="error-row">
    <div className="error-message">{error}</div>
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