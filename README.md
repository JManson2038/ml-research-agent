# ml-research-agent

AI research agent for mapping the machine learning literature landscape. It fetches papers from arXiv, summarizes each paper with Claude, and clusters related work into themes.

## Demo

> Add a screenshot or animated demo here once you have the UI running.

![Demo placeholder](./demo.png)

## How it works

1. `src/fetch.py` queries the arXiv API and returns paper metadata for a topic.
2. `src/summarize.py` sends paper abstracts and metadata to Anthropic Claude to generate concise summaries and topical tags.
3. `src/cluster.py` builds binary tag vectors and groups papers into themes using KMeans clustering.
4. `src/api.py` exposes a FastAPI endpoint at `/api/landscape` for the frontend to request a research landscape.

## Setup

1. Clone the repo and enter the project directory.

2. Create a Python virtual environment and install backend dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file in the repository root with your Anthropic API key:

```env
ANTHROPIC_API_KEY=your_key_here
```

4. Install frontend dependencies:

```bash
cd frontend
npm install
```

## Run

Start the backend server from the repo root:

```bash
.\.venv\Scripts\activate
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

In a second terminal, start the frontend:

```bash
cd frontend
npm run dev
```

Then open the Vite local URL shown in the terminal (usually `http://localhost:5173`).

## Usage

Use the API directly for a quick query:

```bash
curl -X POST http://localhost:8000/api/landscape \
  -H "Content-Type: application/json" \
  -d '{"query": "retrieval augmented generation", "max_results": 8}'
```

Example response structure:

```json
{
  "papers": {
    "themes": [
      {
        "name": "retrieval-augmented generation / evaluation",
        "description": "Papers tagged with: retrieval-augmented generation, evaluation",
        "arxiv_ids": ["2301.00001", "2302.00002"]
      }
    ],
    "papers": [
      {
        "arxiv_id": "2301.00001",
        "title": "...",
        "summary": "...",
        "tags": ["retrieval-augmented generation", "benchmarking"],
        "theme": "retrieval-augmented generation / evaluation"
      }
    ]
  }
}
```

## Notes

- The backend uses `anthropic` and requires `ANTHROPIC_API_KEY`.
- The frontend runs on Vite and communicates with the backend via CORS on `http://localhost:5173`.
- Search queries are sent to the arXiv API through `src/fetch.py`.

