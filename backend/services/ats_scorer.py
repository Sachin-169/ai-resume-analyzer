def calculate_ats_score(matched_skills, jd_skills, semantic_score):
    """
    Combine keyword matching and semantic similarity to produce a single ATS score between 0 and 100.

    65% keyword overlap means resumes that are actually having the skills the JD asks for.
    35% semantic similarity means resumes that are topically/contextually a strong fit even when exact keywords differ.
    """
    if jd_skills:
        keyword_score = len(matched_skills) / len(jd_skills)
    else:
        keyword_score = 0.0

    final_score = (0.65 * keyword_score) + (0.35 * semantic_score)
    final_score = round(final_score * 100)
    final_score = max(0, min(100, final_score))

    return {
        "ats_score": final_score,
        "keyword_score": round(keyword_score * 100),
        "semantic_score": round(semantic_score * 100),
    }

def generate_strengths_and_gaps(matched_skills, missing_skills, semantic_score):

    # A summary of the resume's strengths and gaps against this specific JD. 
    # This is a placeholder for what llm_service.py will eventually generate with real AI.

    strengths = []
    gaps = []

    # Check the main areas where the resume matches the JD
    if matched_skills:
        strengths.append(f"Strong keyword overlap: {', '.join(matched_skills[:5])}")

    if semantic_score >= 0.6:
        strengths.append("Overall resume wording closely matches the job description's language.")

    # Identify missing skills and low semantic similarity
    if missing_skills:
        gaps.append(f"Missing or unmentioned: {', '.join(missing_skills[:5])}")

    if semantic_score < 0.3:
        gaps.append("Resume wording differs significantly from the JD -- consider mirroring its key phrases.")

    if not strengths:
        strengths.append("No strong keyword or semantic overlap detected yet.")

    if not gaps:
        gaps.append("No major gaps found -- strong match overall.")

    return {"strengths": strengths, "gaps": gaps}
