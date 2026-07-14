import { useState } from 'react';

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
    <div>
      <h1>ML Research Landscape</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      <button onClick={handleSearch}>Search</button>

      {loading && <p>Loading...</p>}
      {results && results.themes && results.themes.map((theme) => (
        <div key={theme.name}>
          <h2>{theme.name}</h2>
        {results.papers
          .filter(paper => paper.theme === theme.name)
          .map(paper => (
            <div key={paper.arxiv_id}>
              <h3>{paper.title}</h3>
              <p>{paper.published.slice(0, 10)}</p>
              <p>{paper.tags.join(', ')}</p>
              <p>{paper.summary}</p>
              <a href={paper.pdf_url} target="_blank">Read paper</a>
            </div>
          ))
        }
        </div>
      ))}
    </div>
  );
}