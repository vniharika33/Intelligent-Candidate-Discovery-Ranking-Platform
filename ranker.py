def experience_score(c):

    exp = c["profile"]["years_of_experience"]

    if 6 <= exp <= 8:
        return 1.0

    elif 5 <= exp <= 9:
        return 0.8

    elif 4 <= exp <= 10:
        return 0.6

    return 0.2

def title_score(c):

    title = c["profile"]["current_title"].lower()

    good_titles = [
    "ai engineer",
    "senior ai engineer",
    "ml engineer",
    "machine learning engineer",
    "senior machine learning engineer",
    "recommendation systems engineer",
    "search engineer",
    "nlp engineer",
    "applied ml engineer",
    "senior nlp engineer",
    "staff machine learning engineer",
    "lead ai engineer"
    ]

    for t in good_titles:
        if t in title:
            return 1.0

    return 0.0

def behavioral_score(c):

    s = c["redrob_signals"]

    score = 0.0

    # Available candidate
    if s["open_to_work_flag"]:
        score += 0.25
    else:
        score -= 0.10

    # Recruiter responsiveness
    if s["recruiter_response_rate"] >= 0.8:
        score += 0.15

    elif s["recruiter_response_rate"] >= 0.5:
        score += 0.10

    elif s["recruiter_response_rate"] >= 0.3:
        score += 0.05

    # Interview reliability
    score += 0.20 * s["interview_completion_rate"]

    # Notice period
    if s["notice_period_days"] <= 30:
        score += 0.10
    elif s["notice_period_days"] <= 60:
        score += 0.05

    # Relocation
    if s["willing_to_relocate"]:
        score += 0.05

    # GitHub activity
    if s["github_activity_score"] > 0:
        score += min(s["github_activity_score"] / 100, 0.10)

    # Recruiter interest
    score += min(
        s["saved_by_recruiters_30d"] / 100,
        0.10
    )

    # Search visibility
    score += min(
        s["search_appearance_30d"] / 1000,
        0.05
    )

    # Verification signals
    if s["verified_email"]:
        score += 0.03

    if s["verified_phone"]:
        score += 0.03

    if s["linkedin_connected"]:
        score += 0.04

    return min(score, 1.0)

def negative_title_penalty(c):

    title = c["profile"]["current_title"].lower()

    penalty = 0

    bad_titles = [
        "marketing manager",
        "sales executive",
        "graphic designer",
        "accountant",
        "operations manager",
        "mechanical engineer",
        "civil engineer",
        "content writer",
        "frontend engineer",
        "mobile developer",
        "business analyst"
    ]

    for t in bad_titles:
        if t in title:
            penalty += 1.0

    if "research scientist" in title:
        penalty += 0.3

    if "junior" in title:
        penalty += 0.4

    return min(penalty, 1.0)


def retrieval_score(c):

    text = ""

    text += c["profile"]["headline"].lower() + " "

    for job in c["career_history"]:
        text += job["title"].lower() + " "
        text += job["description"].lower() + " "

    for skill in c["skills"]:
        text += skill["name"].lower() + " "

    keywords = [
    "retrieval",
    "ranking",
    "recommendation",
    "recommender",
    "search",
    "information retrieval",
    "learning to rank",
    "semantic search",
    "hybrid retrieval",
    "vector search",
    "candidate matching",
    "relevance",
    "ndcg",
    "mrr",
    "map",
    "a/b",
    "offline-online correlation"
    ]

    score = 0

    for k in keywords:
        if k in text:
            score += 1

    return min(score / 10, 1.0)

def company_score(c):

    product_companies = [
        "google",
        "meta",
        "apple",
        "amazon",
        "uber",
        "swiggy",
        "zomato",
        "paytm",
        "ola",
        "haptik",
        "mad street den",
        "rephrase.ai"
    ]

    consulting_companies = [
        "tcs",
        "infosys",
        "wipro",
        "accenture",
        "cognizant",
        "capgemini"
    ]

    score = 0

    for job in c["career_history"]:

        company = job["company"].lower()

        for p in product_companies:
            if p in company:
                score += 0.25

        for p in consulting_companies:
            if p in company:
                score -= 0.15

    return max(min(score, 1.0), -1.0)

def activity_score(c):

    s = c["redrob_signals"]

    score = 0

    # Applied recently
    score += min(
        s["applications_submitted_30d"] / 20,
        0.30
    )

    # Recruiters are interested
    score += min(
        s["saved_by_recruiters_30d"] / 20,
        0.30
    )

    # Appears in searches often
    score += min(
        s["search_appearance_30d"] / 1000,
        0.20
    )

    # Recently active
    score += min(
        s["profile_views_received_30d"] / 500,
        0.20
    )

    return min(score, 1.0)

def location_score(c):

    loc = c["profile"]["location"].lower()

    preferred = [
        "pune",
        "noida",
        "delhi",
        "gurgaon",
        "gurugram",
        "mumbai",
        "hyderabad"
    ]

    for city in preferred:
        if city in loc:
            return 1.0

    if c["redrob_signals"]["willing_to_relocate"]:
        return 0.8

    return 0.0

def stability_score(c):

    jobs = c["career_history"]

    if len(jobs) == 0:
        return 0

    total_months = 0

    for job in jobs:
        total_months += job["duration_months"]

    avg_tenure = total_months / len(jobs)

    if avg_tenure >= 30:
        return 1.0

    elif avg_tenure >= 24:
        return 0.8

    elif avg_tenure >= 18:
        return 0.6

    elif avg_tenure >= 12:
        return 0.3

    return 0