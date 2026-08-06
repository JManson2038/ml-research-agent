import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def fetch_papers(query, max_results=10, is_author=False):
    """Fetch papers from the arXiv API for a search query."""
    if is_author:
        formatted = "au:" + query.replace(" ", "_").lower()
    else:
        formatted = f"all:{query}"

    params = urllib.parse.urlencode(
        {
            "search_query": formatted,
            "start": 0,
            "max_results": max_results,
        }
    )
    url = f"https://export.arxiv.org/api/query?{params}"

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ml-research-agent/1.0"},
    )
    with urllib.request.urlopen(request) as response:
        root = ET.fromstring(response.read())

    papers = []
    for entry in root.findall("atom:entry", ATOM_NS):
        paper_id = _text(entry, "atom:id", ATOM_NS)
        pdf_url = None
        for link in entry.findall("atom:link", ATOM_NS):
            if link.get("title") == "pdf":
                pdf_url = link.get("href")
                break

        papers.append(
            {
                "arxiv_id": paper_id.rsplit("/", 1)[-1] if paper_id else "",
                "title": _text(entry, "atom:title", ATOM_NS).strip(),
                "authors": [
                    _text(author, "atom:name", ATOM_NS)
                    for author in entry.findall("atom:author", ATOM_NS)
                ],
                "summary": _text(entry, "atom:summary", ATOM_NS).strip(),
                "published": _text(entry, "atom:published", ATOM_NS),
                "pdf_url": pdf_url,
                "categories": [
                    category.get("term", "")
                    for category in entry.findall("atom:category", ATOM_NS)
                ],
            }
        )

    return papers


def _text(element, path, ns):
    child = element.find(path, ns)
    return child.text if child is not None and child.text else ""

if __name__ == "__main__":
    import json
    papers = fetch_papers("RAG", max_results=3)
    print(json.dumps(papers, indent=2))
