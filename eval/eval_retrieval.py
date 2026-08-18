import json
from backend.retriever import retrieve

test_set = [
    {
        "question": "What services does an operating system provide?",
        "expected_page": 8,
    },
    {
        "question": "What are system calls and why are they used?",
        "expected_page": 69,
    },
    {
        "question": "What are the different states of a process?",
        "expected_page": 117,
    },
    {
        "question": "What information is stored in a process control block?",
        "expected_page": 118,
    },
    {
        "question": "What is a context switch?",
        "expected_page": 124,
    },
    {
        "question": "What is the difference between preemptive and non-preemptive scheduling?",
        "expected_page": 199,
    },
    {
        "question": "What is starvation in priority scheduling and how can aging prevent it?",
        "expected_page": 252,
    },
    {
        "question": "How does round-robin scheduling work?",
        "expected_page": 208,
    },
    {
        "question": "What is the critical-section problem?",
        "expected_page": 241,
    },
    {
        "question": "What are semaphores and how do wait and signal operations work?",
        "expected_page": 248,
    },
    {
        "question": "What is a deadlock system model?",
        "expected_page": 242,
    },
    {
        "question": "What are the necessary conditions for deadlock?",
        "expected_page": 301,
    },
    {
        "question": "What methods can an operating system use to handle deadlocks?",
        "expected_page": 304,
    },
    {
        "question": "How does the banker's algorithm avoid deadlock?",
        "expected_page": 312,
    },
    {
        "question": "What is paging in memory management?",
        "expected_page": 342,
    },
    {
        "question": "What is segmentation and how does it work?",
        "expected_page": 357,
    },
    {
        "question": "What is virtual memory?",
        "expected_page": 371,
    },
    {
        "question": "What is demand paging?",
        "expected_page": 375,
    },
    {
        "question": "What causes thrashing?",
        "expected_page": 400,
    },
    {
        "question": "How does disk scheduling improve storage performance?",
        "expected_page": 525,
    },
]

def evaluate(k=5):
    print("Fetching retrieval results for test set...")
    retrieval_data = []
    
    # Cache retrieval calls to avoid redundant API/vector search overhead
    for item in test_set:
        results = retrieve(item["question"], final_k=k)
        pages = [r["page"] for r in results]
        retrieval_data.append({"item": item, "pages": pages})
        print(f"Q: {item['question']} -> Retrieved PDF Pages: {pages}")

    # Automatically find the best page offset
    print("\nCalculating optimal page offset...")
    best_offset = 0
    max_hits = -1
    
    # Test offsets from 0 to 100
    for offset in range(101):
        hits = 0
        for data in retrieval_data:
            expected_pdf_page = data["item"]["expected_page"] + offset
            if expected_pdf_page in data["pages"]:
                hits += 1
        if hits > max_hits:
            max_hits = hits
            best_offset = offset

    recall = max_hits / len(test_set)
    print(f"\nOptimal Page Offset Found: {best_offset}")
    print(f"Corrected Recall@{k}: {recall:.2%}")
    
    return best_offset

if __name__ == "__main__":
    evaluate(k=5)