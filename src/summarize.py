import json
import os
import re

import anthropic
from dotenv import load_dotenv

from src.fetch import fetch_papers

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

cl = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

PROMPT = """You are summarizing ML research papers for a literature review pipeline.

For each paper below, write:
- summary: 2-3 sentences in plain language describing the main contribution, method, and results. Do not copy the abstract verbatim.
- tags: 3-6 short topical tags (lowercase, e.g. "retrieval-augmented generation", "benchmarking") that capture themes for clustering similar papers.

Return ONLY a JSON array with one object per paper, in the same order as listed:
[
  {{"arxiv_id": "...", "summary": "...", "tags": ["...", "..."]}},
  ...
]

Papers:

{papers_block}
"""


def summarize_papers(papers):
    """Add Claude-generated summary and tags to each paper in one API call."""
    if not papers:
        return papers

    response = cl.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=8192,
        messages=[{"role": "user", "content": _build_prompt(papers)}],
    )

    try:
        parsed = _parse_response(response.content[0].text)
        results_by_id = {item["arxiv_id"]: item for item in parsed}
    except (json.JSONDecodeError, KeyError, TypeError):
        results_by_id = {}

    for paper in papers:
        try:
            result = results_by_id[paper["arxiv_id"]]
            paper["summary"] = result["summary"]
            paper["tags"] = result["tags"]
        except KeyError:
            paper["tags"] = []
            paper["summary"] = ""
            print(f"No summary found for paper {paper['arxiv_id']}")

    return papers


def _build_prompt(papers):
    blocks = []
    for paper in papers:
        authors = ", ".join(paper["authors"])
        categories = ", ".join(paper["categories"])
        blocks.append(
            f"arxiv_id: {paper['arxiv_id']}\n"
            f"title: {paper['title']}\n"
            f"authors: {authors}\n"
            f"categories: {categories}\n"
            f"abstract:\n{paper['summary']}\n"
        )
    return PROMPT.format(papers_block="\n---\n".join(blocks))


def _parse_response(text):
    text = text.strip()
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1)
    return json.loads(text)


if __name__ == "__main__":
    papers = fetch_papers("RAG", max_results=3)
    papers = summarize_papers(papers)
    print(json.dumps(papers, indent=2))
