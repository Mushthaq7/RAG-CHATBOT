import requests

API_URL = "http://localhost:8000"


def chatbot_ask_products(question):
    resp = requests.get(f"{API_URL}/products",
                        params={"query": question, "top_k": 3})
    if resp.status_code == 200:
        data = resp.json()
        print(f"[User] {question}")
        print(f"[Bot] Top products:")
        for p in data['results']:
            print(f"  - {p['name']}: {p['desc']}")
        print(f"[Bot] Summary: {data['summary']}\n")
    else:
        print(f"[User] {question}")
        print(f"[Bot] Sorry, I couldn't retrieve product info.\n")


def chatbot_ask_outlets(question):
    resp = requests.get(f"{API_URL}/outlets", params={"query": question})
    if resp.status_code == 200:
        data = resp.json()
        print(f"[User] {question}")
        print(f"[Bot] SQL used: {data['sql']}")
        if data['results']:
            print(f"[Bot] Outlets:")
            for o in data['results']:
                print(
                    f"  - {o['name']} | {o['address']} | {o.get('hours', '')} | {o.get('services', '')}")
        else:
            print(f"[Bot] No outlets found matching your query.")
        print()
    else:
        print(f"[User] {question}")
        print(f"[Bot] Sorry, I couldn't retrieve outlet info.\n")


def run_demo():
    print("--- Product Endpoint Success ---")
    chatbot_ask_products("Show me the best ZUS tumbler for hot drinks.")
    print("--- Product Endpoint Failure (nonsense query) ---")
    chatbot_ask_products("asdkjhasd 123123")
    print("--- Outlets Endpoint Success ---")
    chatbot_ask_outlets("Which outlets are open after 8pm in Kuala Lumpur?")
    print("--- Outlets Endpoint Failure (invalid query) ---")
    chatbot_ask_outlets("DROP TABLE outlets;")


if __name__ == "__main__":
    run_demo()
