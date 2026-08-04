import argparse
import textwrap
from datetime import datetime

from src.fetch import fetch_papers
from src.summarize import summarize_papers
from src.cluster import cluster_papers


def build_research_landscape(clustered, width=80):
    """Render a clean research landscape from clustered paper data."""
    themes = clustered.get("themes", [])
    papers = clustered.get("papers", [])
    if not papers:
        return "No papers available to display."

    papers_by_theme = {theme["name"]: [] for theme in themes}
    for paper in papers:
        theme_name = paper.get("theme", "Uncategorized")
        papers_by_theme.setdefault(theme_name, []).append(paper)

    lines = []
    lines.append("RESEARCH LANDSCAPE")
    lines.append("=" * len(lines[0]))
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    for index, theme in enumerate(themes, start=1):
        theme_name = theme.get("name", "Unnamed Theme")
        theme_description = theme.get("description", "")
        theme_papers = papers_by_theme.get(theme_name, [])

        lines.append(f"{index}. {theme_name} ({len(theme_papers)} paper{'s' if len(theme_papers) != 1 else ''})")
        if theme_description:
            lines.extend(_wrap_lines(theme_description, width, prefix="   "))
        lines.append("")

        for paper in theme_papers:
            lines.extend(_render_paper(paper, width))
            lines.append("")

    extra_themes = [name for name in papers_by_theme if name not in {t["name"] for t in themes}]
    for theme_name in extra_themes:
        lines.append(f"{len(lines) + 1}. {theme_name} ({len(papers_by_theme[theme_name])} papers)")
        lines.append("")
        for paper in papers_by_theme[theme_name]:
            lines.extend(_render_paper(paper, width))
            lines.append("")

    return "\n".join(lines).strip()


def _render_paper(paper, width):
    title = paper.get("title", "Untitled")
    arxiv_id = paper.get("arxiv_id", "")
    authors = paper.get("authors", [])
    summary = paper.get("summary", "No summary available.")
    tags = paper.get("tags", [])
    pdf_url = paper.get("pdf_url", "")

    lines = []
    heading = f"- {title} [{arxiv_id}]"
    lines.append(heading)
    if authors:
        lines.append(f"  Authors: {', '.join(authors)}")
    if pdf_url:
        lines.append(f"  Link: {pdf_url}")
    if tags:
        lines.append(f"  Tags: {', '.join(tags)}")
    lines.extend(_wrap_lines(summary, width, prefix="  "))
    return lines


def _wrap_lines(text, width, prefix=""):
    wrapped = textwrap.wrap(text, width=width - len(prefix))
    return [f"{prefix}{line}" for line in wrapped] if wrapped else [prefix]


def print_research_landscape(clustered, width=80):
    print(build_research_landscape(clustered, width=width))


def run_topic_report(query, max_results=10, n_clusters=None, width=80):
    papers = fetch_papers(query, max_results=max_results)
    if not papers:
        print("No papers were fetched for the query.")
        return

    papers = summarize_papers(papers)
    clustered = cluster_papers(papers, n_clusters=n_clusters)
    print_research_landscape(clustered, width=width)


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a terminal research landscape from arXiv papers."
    )
    parser.add_argument("query", help="Search query for arXiv papers.")
    parser.add_argument("--max-results", type=int, default=10, help="Maximum number of papers to fetch.")
    parser.add_argument("--clusters", type=int, default=None, help="Number of clusters to generate.")
    parser.add_argument("--width", type=int, default=80, help="Terminal width for text wrapping.")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    run_topic_report(
        query=args.query,
        max_results=args.max_results,
        n_clusters=args.clusters,
        width=args.width,
    )
