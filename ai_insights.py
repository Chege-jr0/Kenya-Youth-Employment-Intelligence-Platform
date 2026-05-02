import ollama
import json

#Defing the market context
# Converts market stats into a readble summary for the AI
def prepare_market_context(stats, city=None, prop_type=None):
    # Think of this as writing a brief note before asking the AI a question to refer to the data
    context = f"""
    Kenya Real Estate Market Summary (Q4 2024):

    Overall Market:
    - Avearage Property Price: KES {stats['avg_price']: ,}
    - Average Rental Yield: {stats['rental_yield']}%
    - Average Occupancy Rate: {stats['occupancy_rate']}%
    - Total Transactions: {stats['transactions']:,}
    - Top Performing City: {stats['top_city']}

"""
    
    if city:
        context += f"\nCurrently Viewing: {city}"
    if prop_type:
        context += f"\nProperty Type: {prop_type}"

    return context

#Asking tinyllama to generate market insights from the data
def generate_market_insights(stats, city=None, prop_type=None):

    context = prepare_market_context(stats, city, prop_type)

    prompt = f"""You are a proffessional real estate market analyst in Kenya.
    Based on the market data below, provide 3 clear and specifu investment insights.
    Be concise, mention specific numbers, and focus on actionable observations.

    {context}
     
     Provide exactly 3 insights in this format:
    1. [Insight about prices or gtowth]
    2. [Insight about rental yields or occupancy]
    3. [Inisght about investment opportunity]
    """

    try:
        response = ollama.chat(
            model = "tinyllama",
            messages = [{"role": "user", "content": prompt}]
        )
        return response["messages"]["content"]
    except Exception as e:
        print("AI insights unavailable. Make sure Ollama is working")

# The Question Answering Function
def ask_market_question(question, stats, city=None, prop_type=None):

    context = prepare_market_context(stats, city, prop_type)
    
    prompt = f""" You are a proffessional real estate market analyst in Kenya.
    Use the market data below to answer the question accurately.
    Be specific, mention numbers where relevant.
    If the answer is not in the data, say "I don't have information about that."

    {context}

    Question: {question}

   Answer: 
"""
    
    try:
        response = ollama.chat(
            model = "tinyllama",
            messages = [{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        print("AI insights unavailable. Make sure Ollama is working")