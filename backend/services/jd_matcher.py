from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

embedding_model = None
embedding_failed = False

def get_embedding_model():
    global embedding_model, embedding_failed

    # Load the embedding model only when it is needed
    if embedding_model is None and not embedding_failed:
        try:
            from sentence_transformers import SentenceTransformer
            embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            embedding_failed = True

    return embedding_model

def semantic_similarity(resume_text, jd_text):
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    model = get_embedding_model()

    # Use semantic embeddings when the model is available
    if model:
        embeddings = model.encode([resume_text, jd_text])
        score = cosine_similarity(
            [embeddings[0]], [embeddings[1]]
        )[0][0]

        return max(0.0, min(1.0, float(score)))

    # Fall back to TF-IDF if embeddings are unavailable
    return tfidf_similarity(resume_text, jd_text)

def tfidf_similarity(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words="english")

    try:
        matrix = vectorizer.fit_transform([resume_text, jd_text])
    except ValueError:
        return 0.0

    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]

    return max(0.0, min(1.0, float(score)))

def compare_skills(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    # Find common, missing and additional skills
    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)
    extra = sorted(resume_set - jd_set)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra
    }