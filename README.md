# Resume Analyzer & Job Match

AI-assisted tool that parses a resume PDF, compares it against a job
description, and produces an ATS-style match score with missing
skills and improvement suggestions.

## Status

- **Phase 1** — PDF upload, text extraction, section splitting, skill extraction: ✅ done
- **Phase 2** — JD input + resume-vs-JD comparison: ✅ done
- **Phase 3** — ATS score with reasons: ✅ done
- **Phase 4** — LLM bullet-point rewriting: ✅ backend endpoint wired up (works with OpenAI/Gemini key, or a rule-based fallback with no key). Not yet surfaced in the UI — see "Next steps" below.

## Project structure

```
resume-analyzer/
├── frontend/           React + Vite app
│   └── src/
│       ├── components/ ResumeUpload, JDInput, ScoreGauge, ResultsDashboard
│       ├── api.js      fetch wrappers for the Flask API
│       └── App.jsx
├── backend/
│   ├── app.py           Flask routes
│   ├── parser.py         PDF text extraction + section splitting (PyMuPDF/pdfplumber)
│   ├── utils.py           text cleaning helpers
│   ├── skill_extractor.py spaCy PhraseMatcher-based skill extraction
│   ├── ats.py             ATS scoring + comparison logic
│   ├── similarity.py      Sentence-Transformers / TF-IDF semantic similarity
│   └── llm.py             Phase 4: bullet-point rewriting (OpenAI/Gemini/fallback)
├── uploads/             scratch space for uploaded PDFs (auto-cleared per request)
├── requirements.txt
└── README.md
```

## Backend setup

```bash
cd resume-analyzer
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

python backend/app.py           # runs on http://localhost:5000
```

The first time `/api/analyze` is called, `sentence-transformers` will
try to download the `all-MiniLM-L6-v2` model (~90MB). If there's no
internet access, `similarity.py` automatically falls back to a TF-IDF
based similarity score, so the app still works end-to-end.

### Optional: enable real AI bullet rewriting (Phase 4)

```bash
export OPENAI_API_KEY=sk-...
# or
export GEMINI_API_KEY=...
```

If neither is set, `/api/rewrite-bullet` still works using a simple
rule-based rewrite (swaps weak verbs, injects a missing keyword).

## Frontend setup

```bash
cd resume-analyzer/frontend
npm install
npm run dev                     # runs on http://localhost:5173
```

The Vite dev server proxies `/api/*` requests to `http://localhost:5000`,
so run the backend first.

## API reference

### `POST /api/parse-resume`
`multipart/form-data` with a `file` field (PDF). Returns:
```json
{
  "filename": "resume.pdf",
  "raw_text": "...",
  "cleaned_text": "...",
  "sections": { "education": "...", "skills": "...", "experience": "...", "projects": "...", "other": "..." },
  "skills": ["Python", "React", "Flask"]
}
```

### `POST /api/analyze`
```json
{ "resume_text": "...", "jd_text": "..." }
```
Returns:
```json
{
  "ats_score": 72,
  "skill_overlap_score": 60,
  "semantic_similarity_score": 91,
  "matched_skills": ["Python", "TensorFlow", "React"],
  "missing_skills": ["Docker", "AWS", "SQL"],
  "extra_skills": ["MongoDB"],
  "reasons": [{"skill": "Python", "status": "match"}, {"skill": "Docker", "status": "missing"}],
  "suggested_keywords": ["Docker", "AWS", "SQL"],
  "suggestions": ["Add or highlight experience with: Docker, AWS, SQL...", "..."]
}
```

### `POST /api/rewrite-bullet`
```json
{ "bullet": "Developed a Flask API...", "keywords": ["Docker", "AWS"] }
```
Returns `{ "rewritten": "...", "provider": "openai" | "gemini" | "fallback" }`.

## How the ATS score is calculated

```
final_score = 0.65 * (matched JD skills / total JD skills)
            + 0.35 * (semantic similarity between resume & JD text)
```

Skill matching uses a curated dictionary (`skill_extractor.py`) matched
via spaCy's `PhraseMatcher`, so multi-word skills (e.g. "machine
learning") and common synonyms (e.g. "k8s" → Kubernetes) are handled.
Semantic similarity uses sentence embeddings so wording differences
(e.g. "built REST APIs" vs "developed backend services") still
contribute to the score, not just exact keyword hits.

## Extending the skill dictionary

Add entries to `SKILL_DB` in `backend/skill_extractor.py`:
```python
"Kubernetes": ["kubernetes", "k8s"],
```
The key is the canonical name shown in the UI; the list is every
surface form to match in resume/JD text.

## Next steps

1. Wire the `/api/rewrite-bullet` endpoint into the frontend (e.g. an
   "Improve this bullet" button per experience line, using the
   `experience` section text extracted from the resume).
2. Add OCR fallback (e.g. `pytesseract`) for scanned/image-based PDF resumes.
3. Persist analysis history per user (currently stateless).
4. Add a proper resume section parser for bullet-level extraction
   instead of raw section text (useful for the Phase 4 rewrite feature).
