import spacy
from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")

# key = canonical skill name shown to the user
# value = every surface form / synonym we want to catch in resume or JD text
SKILL_DB = {
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "c sharp"],
    "SQL": ["sql"],
    "NoSQL": ["nosql"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node.js", "node", "nodejs"],
    "Flask": ["flask"],
    "Django": ["django"],
    "FastAPI": ["fastapi"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "spaCy": ["spacy"],
    "NLP": ["nlp", "natural language processing"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "dl"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "MongoDB": ["mongodb", "mongo"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "Git": ["git"],
    "REST API": ["rest api", "restful api", "rest"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
}

# PhraseMatcher needs to share vocab with whatever pipeline processes the text.
# attr="LOWER" makes matching case-insensitive, so "Python"/"python"/"PYTHON" all hit.
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

for canonical_name, synonyms in SKILL_DB.items():
    # build one spaCy pattern per synonym, register them all under the canonical name
    # -> whichever synonym matches, spaCy reports back the canonical name, not the synonym
    patterns = [nlp.make_doc(synonym) for synonym in synonyms]
    matcher.add(canonical_name, patterns)


def extract_skills(text):
    """
    Scans `text` for known skills and returns a sorted list of canonical
    skill names (e.g. "k8s" in the text -> "Kubernetes" in the output).
    """
    if not text or not text.strip():
        return []

    doc = nlp(text)
    matches = matcher(doc)

    # use a set so the same skill mentioned 5 times only shows up once
    found_skills = set()
    for match_id, start, end in matches:
        canonical_name = nlp.vocab.strings[match_id]
        found_skills.add(canonical_name)

    return sorted(found_skills)