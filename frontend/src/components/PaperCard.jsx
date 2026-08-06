export default function PaperCard({ paper, onAuthorClick })
 {console.log('onAuthorClick:', onAuthorClick);
  return (
    <div className="paper-card">
      <h3>{paper.title}</h3>
      <p className="paper-date">{paper.published.slice(0, 10)}</p>
      <p className="paper-authors">
        {paper.authors.map((author, i) => (
          <span key={i}>
            <button className="author-btn" onClick={() => onAuthorClick(author, true)}>
              {author}
            </button>
            {i < paper.authors.length - 1 && ', '}
          </span>
        ))}
      </p>
      {paper.tags && paper.tags.length > 0 && (
        <p className="paper-tags">{paper.tags.join(', ')}</p>
      )}
      <p className="paper-summary">{paper.summary}</p>
      <a href={paper.pdf_url} target="_blank" rel="noopener noreferrer" className="paper-link">Read paper</a>
    </div>
  );
}