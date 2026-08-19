import sys
import requests
from google import genai

API_KEY = "AQ.Ab8RN6J-uANsFqHt-Ju5MeGLpnyNmE8mxB-4_4tM1eOeY3HxfQ"


def search_wikipedia(query):
    url = "https://wikipedia.org"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "utf8": 1,
    }
    try:
        response = requests.get(url, params=params, timeout=5).json()
        search_results = response.get("query", {}).get("search", [])

        if not search_results:
            return "No matching Wikipedia articles found."

        snippet = search_results["snippet"]
        clean_text = snippet.replace('<span class="searchmatch">', "").replace(
            "</span>", ""
        )
        return clean_text
    except Exception:
        return "Local network blocked Wikipedia. Use your internal knowledge base to answer."


# Initialize the AI Client once outside the loop
client = genai.Client(api_key=API_KEY)

print("--- AI Agent Started (Type 'exit' or 'quit' to close) ---")
while True:
    print("\n" + "=" * 40)
    user_question = input("Ask your AI anything: ")

    if user_question.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    print("🔍 Searching the web for sources...")
    live_facts = search_wikipedia(user_question)

    prompt_with_context = f"""
    You are a helpful AI assistant. 
    Answer the user's question accurately. If the live facts say 'Local network blocked Wikipedia', answer using your own knowledge.

    Live Facts:
    "{live_facts}"

    User Question: {user_question}
    Answer:
    """

    print("🤖 AI is thinking...")
    print("\n✨ Response: ", end="")

    # generate_content_stream streams words live as they are built!
    response_stream = client.models.generate_content_stream(
        model="models/gemini-3.6-flash", contents=prompt_with_context
    )

    for chunk in response_stream:
        print(chunk.text, end="")
        sys.stdout.flush()

    print() 