import json
import voyageai
import os
from dotenv import load_dotenv
from sklearn.cluster import KMeans


from src.fetch import fetch_papers
from src.summarize import summarize_papers
    
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))



def cluster_papers(papers, n_clusters=None):
    """Group tagged papers into themes via K-means on binary tag vectors."""
    if not papers:
        return {"themes": [], "papers": papers}

    embeddings = _embed_summaries(papers)
    if not embeddings:
        theme = {
            "name": "Uncategorized",
            "description": "No tags available for clustering.",
            "arxiv_ids": [p["arxiv_id"] for p in papers],
        }
        for paper in papers:
            paper["theme"] = theme["name"]
        return {"themes": [theme], "papers": papers}

    k = n_clusters or _default_k(len(papers))
    labels = KMeans(n_clusters=k, n_init="auto", random_state=0).fit_predict(embeddings)

    themes = _build_themes(papers, labels)
    theme_by_id = {
        arxiv_id: theme["name"]
        for theme in themes
        for arxiv_id in theme["arxiv_ids"]
    }
    for paper in papers:
        paper["theme"] = theme_by_id[paper["arxiv_id"]]

    return {"themes": themes, "papers": papers}


def _embed_summaries(papers):
    summaries = [paper["summary"] for paper in papers]
    result = vo.embed(summaries, model="voyage-3-lite", input_type="document")

    return result.embeddings

def _default_k(n):
    return min(max(2, n // 2), n)


def _build_themes(papers, labels):
    vocab = sorted({tag.lower() for paper in papers for tag in paper.get("tags", [])})
    clusters = {}
    for paper, label in zip(papers, labels):
        clusters.setdefault(label, []).append(paper)

    themes = []
    for label in sorted(clusters):
        cluster_papers = clusters[label]
        top_tags = _top_tags(cluster_papers, vocab)
        name = " / ".join(top_tags) if top_tags else f"Cluster {label + 1}"
        themes.append({
            "name": name,
            "description": f"Papers tagged with: {', '.join(top_tags)}" if top_tags else "",
            "arxiv_ids": [p["arxiv_id"] for p in cluster_papers],
        })
    return themes


def _top_tags(papers, vocab, n=3):
    counts = {tag: 0 for tag in vocab}
    for paper in papers:
        for tag in paper.get("tags", []):
            counts[tag.lower()] += 1
    ranked = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return [tag for tag, count in ranked if count > 0][:n]


if __name__ == "__main__":
    papers = fetch_papers("RAG", max_results=3)
    papers = summarize_papers(papers)
    result = cluster_papers(papers)
    print(json.dumps(result, indent=2))
