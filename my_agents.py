import asyncio
import os
import requests
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat

# --- TOOLS ---

async def fetch_market_data(query: str) -> str:
    """Fetches real-time market data for a given query."""
    # In a real scenario, you'd use a real API key here. 
    # For this demo, we simulate a real-time API response.
    print(f" [System] Fetching live data for: {query}...")
    return "Real-time API Report: Current AI Market is $210 billion with an annual growth rate of 22%."

async def calculate_ai_growth(current_market_size: float, growth_rate: float, years: int) -> str:
    """Calculates projected market size using compound growth. Returns value in billions."""
    raw_projected = current_market_size * ((1 + growth_rate) ** years)
    # Bulletproof conversion to billions
    final_value = raw_projected / 1_000_000_000 if raw_projected > 1_000_000 else raw_projected
    return f"The projected market size after {years} years is ${final_value:.2f} billion."

async def verify_against_doc(fact: str) -> str:
    """Verifies a fact against the official company internal document."""
    try:
        with open("market_data.txt", "r") as f:
            doc_content = f.read()
        if fact.lower() in doc_content.lower():
            return "MATCHED: This fact is verified by the internal document."
        return "MISMATCH: The internal document does not support this claim."
    except FileNotFoundError:
        return "Error: Internal document 'market_data.txt' not found."

async def main():
    # Setup LLM
    model_client = OpenAIChatCompletionClient(
        model="gemma4:31b-cloud",
        base_url="http://host.docker.internal:11434/v1",
        api_key="ollama",
        model_info={"vision": False, "function_calling": True, "json_output": True, "family": "llama3", "structured_output": False}
    )

    # --- AGENTS ---
    
    researcher = AssistantAgent(
        name="Researcher",
        model_client=model_client,
        system_message="You are a Tech Researcher. 1. Fetch live data using tools. 2. Calculate projections. 3. Provide a detailed report. Always be precise with units (Billions).",
        tools=[fetch_market_data, calculate_ai_growth],
    )

    fact_checker = AssistantAgent(
        name="FactChecker",
        model_client=model_client,
        system_message="You are a Compliance Officer. Your ONLY job is to verify the Researcher's numbers against the internal document. If a number is wrong, state exactly what it should be.",
        tools=[verify_against_doc],
    )

    writer = AssistantAgent(
        name="Writer",
        model_client=model_client,
        system_message="You are a Content Creator. Create a catchy headline based on verified research. Only write the headline.",
    )

    reviewer = AssistantAgent(
        name="Reviewer",
        model_client=model_client,
        system_message="""You are a Strict Senior Editor. 
        Your goal is 100% accuracy. 
        1. Compare the Headline against the Research.
        2. Check if the numbers match exactly.
        3. If there is ANY error, respond with 'REJECTED: [Reason]' and ask the Writer to fix it.
        4. Only if it is perfect, respond with 'APPROVED: [Final Headline]'.""",
    )

    # --- THE LOOP (Group Chat) ---
    # RoundRobin means: Researcher -> FactChecker -> Writer -> Reviewer -> (Repeat)
    team = RoundRobinGroupChat([researcher, fact_checker, writer, reviewer], max_turns=10)

    print("### Starting the Agentic Loop... ###")
    # We use the Console UI to watch the a-ha moments in real time
    await Console(team.run_stream(task="Find the current AI market size, project it for 5 years, verify it against the internal doc, and create a catchy headline."))

if __name__ == "__main__":
    # Create a dummy doc for the FactChecker to read
    with open("market_data.txt", "w") as f:
        f.write("Internal Document: The AI market is currently valued at 210 billion dollars.")

    asyncio.run(main())