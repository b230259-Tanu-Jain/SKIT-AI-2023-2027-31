import ast
import pandas as pd

PREFERENCE_WEIGHT = 0.30
INTELLIGENCE_WEIGHT = 0.70
SKILL_MATCH_WEIGHT = 0.70
SIMILARITY_WEIGHT = 0.30

PREFERENCE_FIELDS = {
    "work_life_balance": ["work_life_balance", "workLife"],
    "culture_values": ["culture_values", "culture"],
    "career_opp": ["career_opp", "career_opportunities", "career"],
    "comp_benefits": ["comp_benefits", "compensation"],
}

def _number(value):
    try:
        value = float(value)
        return value if pd.notna(value) else None
    except (TypeError, ValueError):
        return None

def _rating_100(value):
    value = _number(value)
    if value is None or value < 0:
        return None
    return min(value * 20 if value <= 5 else value, 100)

def calculate_preference_score(row, preferences):
    scores = []

    for attribute, aliases in PREFERENCE_FIELDS.items():
        desired = _number(preferences.get(attribute))
        actual = None

        for column in aliases:
            if column in row.index:
                actual = _rating_100(row[column])
                if actual is not None:
                    break

        if desired is not None and actual is not None:
            desired = max(0, min(100, desired))
            scores.append(100 - abs(actual - desired))

    # Missing company attributes are not treated as zero.
    return round(sum(scores) / len(scores), 2) if scores else 50.0

def recommend_companies(company_df, user_profile, top_n=5):
    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    if "company_intelligence_score" not in company_df.columns:
        raise ValueError("Missing company_intelligence_score column.")

    if company_df.empty:
        return company_df.copy()

    df = company_df.copy()
    df["company_intelligence_score"] = pd.to_numeric(
        df["company_intelligence_score"], errors="coerce"
    )
    df = df.dropna(subset=["company_intelligence_score"]).copy()

    if df.empty:
        return df

    df["company_intelligence_score"] = df[
        "company_intelligence_score"
    ].clip(0, 100)

    preferences = user_profile.get_preferences()
    df["preference_score"] = df.apply(
        lambda row: calculate_preference_score(row, preferences),
        axis=1
    )

    df["recommendation_score"] = (
        INTELLIGENCE_WEIGHT * df["company_intelligence_score"]
        + PREFERENCE_WEIGHT * df["preference_score"]
    ).round(2)

    sort_columns = ["recommendation_score"]
    if "review_count" in df.columns:
        df["review_count"] = pd.to_numeric(
            df["review_count"], errors="coerce"
        ).fillna(0)
        sort_columns.append("review_count")

    return df.sort_values(
        sort_columns, ascending=False
    ).head(top_n).reset_index(drop=True)


def _parse_skills(value):
    if isinstance(value, (list, tuple, set)):
        skills = value
    elif isinstance(value, str):
        try:
            parsed = ast.literal_eval(value)
            skills = (
                parsed if isinstance(parsed, (list, tuple, set))
                else value.replace(";", ",").replace("|", ",").split(",")
            )
        except (ValueError, SyntaxError):
            skills = value.replace(";", ",").replace("|", ",").split(",")
    else:
        return set()

    return {
        str(skill).strip().lower()
        for skill in skills
        if skill is not None and str(skill).strip()
    }


def _similarity_scores(user_skills, role_skills):
    """Use Sentence-BERT when available; otherwise use TF-IDF."""
    if not user_skills:
        return [0.0] * len(role_skills)

    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity

        global _embedding_model
        try:
            _embedding_model
        except NameError:
            _embedding_model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

        user_list = sorted(user_skills)
        user_vectors = _embedding_model.encode(
            user_list, normalize_embeddings=True
        )

        scores = []
        for required in role_skills:
            if not required:
                scores.append(0.0)
                continue

            role_vectors = _embedding_model.encode(
                sorted(required), normalize_embeddings=True
            )
            similarities = cosine_similarity(role_vectors, user_vectors)
            # Each required skill receives its best similarity to a user skill.
            scores.append(
                round(float(similarities.max(axis=1).mean()) * 100, 2)
            )

        return scores

    except Exception:
        # Lightweight fallback; this is text similarity, not true semantics.
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        user_text = " ".join(sorted(user_skills))
        role_texts = [" ".join(sorted(skills)) for skills in role_skills]

        if not any(text.strip() for text in role_texts):
            return [0.0] * len(role_skills)

        try:
            matrix = TfidfVectorizer(
                analyzer="char_wb", ngram_range=(2, 4)
            ).fit_transform([user_text] + role_texts)

            return (
                cosine_similarity(matrix[0:1], matrix[1:]).flatten()
                * 100
            ).round(2).tolist()
        except ValueError:
            return [0.0] * len(role_skills)


def recommend_job_roles(job_df, user_profile, top_n=5):
    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    if "job_skill_set" not in job_df.columns:
        raise ValueError("Missing job_skill_set column.")

    if job_df.empty:
        return job_df.copy()

    df = job_df.copy()
    user_skills = _parse_skills(user_profile.get_skills())
    df["required_skills"] = df["job_skill_set"].apply(_parse_skills)

    df["matched_skills"] = df["required_skills"].apply(
        lambda skills: sorted(user_skills & skills)
    )
    df["missing_skills"] = df["required_skills"].apply(
        lambda skills: sorted(skills - user_skills)
    )
    df["skill_match_score"] = df["required_skills"].apply(
        lambda skills: round(
            100 * len(user_skills & skills) / len(skills), 2
        ) if skills else 0.0
    )

    df["similarity_score"] = _similarity_scores(
        user_skills, df["required_skills"].tolist()
    )

    df["role_suitability_score"] = (
        SKILL_MATCH_WEIGHT * df["skill_match_score"]
        + SIMILARITY_WEIGHT * df["similarity_score"]
    ).round(2)

    # Empty skill lists should not rank as suitable roles.
    df.loc[df["required_skills"].apply(len) == 0,
           "role_suitability_score"] = 0.0

    return df.sort_values(
        ["role_suitability_score", "skill_match_score"],
        ascending=False
    ).head(top_n).reset_index(drop=True)
