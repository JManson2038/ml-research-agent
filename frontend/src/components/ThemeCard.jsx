import PaperCard from './PaperCard';

export default function ThemeCard({ theme, papers, onAuthorClick }) {
  return (
    <div className="theme-card">
      <h2>{theme.name}</h2>
      <p className="theme-description">{theme.description}</p>
      <div className="theme-papers">
        {papers.map(paper => (
          <PaperCard key={paper.arxiv_id} paper={paper} onAuthorClick={onAuthorClick} />
        ))}
      </div>
    </div>
  );
}