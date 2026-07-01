import hashlib

COMPANY_QUESTIONS = [
    {"id": "amazon-easy-dsa-001", "company": "Amazon", "difficulty": "easy", "topic": "DSA", "question": "Explain time complexity of binary search."},
    {"id": "amazon-medium-system-design-001", "company": "Amazon", "difficulty": "medium", "topic": "System Design", "question": "How would you design a rate limiter for a distributed API?"},
    {"id": "amazon-hard-react-001", "company": "Amazon", "difficulty": "hard", "topic": "React", "question": "How do you optimize rendering performance in a large React application?"},
    {"id": "google-easy-oop-001", "company": "Google", "difficulty": "easy", "topic": "OOP", "question": "What are the four pillars of OOP?"},
    {"id": "google-medium-dbms-001", "company": "Google", "difficulty": "medium", "topic": "DBMS", "question": "Explain normalization and denormalization with use cases."},
    {"id": "google-hard-os-001", "company": "Google", "difficulty": "hard", "topic": "OS", "question": "Explain how virtual memory works and why it is needed."},
    {"id": "microsoft-easy-react-001", "company": "Microsoft", "difficulty": "easy", "topic": "React", "question": "What is the difference between props and state?"},
    {"id": "microsoft-medium-node-001", "company": "Microsoft", "difficulty": "medium", "topic": "Node", "question": "How does event loop work in Node.js?"},
    {"id": "microsoft-hard-cn-001", "company": "Microsoft", "difficulty": "hard", "topic": "CN", "question": "How would you troubleshoot packet loss in production?"},
    {"id": "tcs-easy-dbms-001", "company": "TCS", "difficulty": "easy", "topic": "DBMS", "question": "What is a primary key?"},
    {"id": "infosys-medium-dsa-001", "company": "Infosys", "difficulty": "medium", "topic": "DSA", "question": "Compare BFS and DFS."},
    {"id": "accenture-hard-node-001", "company": "Accenture", "difficulty": "hard", "topic": "Node", "question": "How would you scale a Node.js service under high traffic?"},
]


def build_company_question_index() -> dict[str, dict]:
    return {item["id"]: item for item in COMPANY_QUESTIONS}


def normalize_company_question(document: dict) -> dict:
    normalized = {
        "id": document.get("id") or build_question_id(document["company"], document["difficulty"], document["topic"], document["question"]),
        "company": document["company"],
        "difficulty": document["difficulty"],
        "topic": document["topic"],
        "question": document["question"],
    }
    return normalized


def build_question_id(company: str, difficulty: str, topic: str, question: str) -> str:
    fingerprint = hashlib.sha1(f"{company}|{difficulty}|{topic}|{question}".encode("utf-8")).hexdigest()[:8]
    return f"{company.lower()}-{difficulty.lower()}-{topic.lower()}-{fingerprint}"
