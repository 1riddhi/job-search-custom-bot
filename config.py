HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

GREENHOUSE_COMPANIES = [
    ("Atlassian", "atlassian"),
    ("GitLab", "gitlab"),
    ("Stripe", "stripe"),
    ("Rubrik", "rubrik"),
    ("Airbnb", "airbnb"),
    ("Coinbase", "coinbase"),
]

KEYWORDS = [
    "software engineer", "sde", "developer", "swe",
    "backend", "back end", "frontend", "full stack", "fullstack"
]

BAD_KEYWORDS = [
    "principal",
    "architect",
    "manager",
    "staff",
    "distinguished",
    "partner",
    "senior", "director", "head", "lead", "legal",
    "sales", "solutions", "consultant",
    "operations", "intern"
]

INDIA_LOCATIONS = [
    "india", "bangalore", "bengaluru",
    "hyderabad", "pune", "chennai",
    "gurgaon", "noida", "mumbai"
]
# last 24 hours filter
MAX_HOURS = 24