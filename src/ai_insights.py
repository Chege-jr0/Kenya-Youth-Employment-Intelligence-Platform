# This file connects to TinyLlama  via Ollama and generates policy insights and answers questions that the user asks anything about youth employment.

import ollama

def prepare_employment_context(context: dict) -> str:
    """
    Convert employment statistics into a readable brief for the AI
    """
    
    return f"""
    Kenya Youth Employment Intelligence Brief ({context['selected_year']}):

    National Overview:
    - National Youth Unemployment rate: {context['national_rate']}%
    - Year on year change: {context['year_on_year']}%

    County Analysis:
    - Highest unemployment: {context['worst_county']} at {context['worst_rate']}%
    - Lowest unemployment: {context['best_county']} at {context['best_rate']}%

    Gender Analysis:
    - Average gender gap: {context['avg_gender_gap']}%
    - Female unemployment consistently higher than male
"""

def generate_employment_insights(context: dict) -> str:
    """
    Generate AI powered policy insights from Kenya employment data.
    """
    brief = prepare_employment_context(context)

    prompt = f"""You are a senior policy analyst at a development organisation working on youth Employment in Kenya.

    Based on the data brief below, provide exactly 4  specific policy insights and recommendations.

    Focus on:
    - Which populations need most urgent intervention.
    - What policy actions could reduce unemployment
    - Which sectors or counties show most opportunity
    - What does the gender gap data suggest for policy

    {brief}

   Provide exactly 4 insights in this format:
   1. [Finding]: [Specific observation from the data]
      [Recommendation]: [Concerete policy action]

   2. [Finding]: [Specific observation from the data]
      [Recommendation]: [Concrete policy action]

   3. [Finding]: [Specific observation from the data]
      [Recommendation]: [Concrete policy action]

   4. [Finding]: [Specific observation from the data]
      [Recommendation]: [Concrete policy action]    
"""
    # Gives the AI a specific professional identity with the prompt
    # This is called role prompting, without this, it would respond like a general chatbot
    # else return an error
    try:
        response = ollama.chat(
            model = "tinyllama",
            messages = [{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"AI unavailable. Make sure ollama is running: {str(e)}"  

def ask_employment_question(question: str, context: dict) -> str:
    """
    Answer a specific question about
    Kenya youth employment data.
    """
    brief = prepare_employment_context(context)

    prompt = f"""You are a senior policy analyst specialising 
in Kenya youth employment and labour markets.

Use the data brief below to answer the question accurately.
Be specific — mention county names, percentages and trends.
If the answer requires data not in the brief, say:
"This requires additional data beyond the current brief."

{brief}

Question: {question}

Answer:"""

    try:
        response = ollama.chat(
            model="tinyllama",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]

    except Exception as e:
        return f" Could not get answer. Make sure Ollama is running.\nError: {str(e)}"
    

if __name__ == "__main__":
    test_context = {
        "national_rate": 13.9,
        "year_on_year": -0.8,
        "worst_county": "Mandera",
        "worst_rate": 48.2,
        "best_county": "Nairobi",
        "best_rate": 18.5,
        "avg_gender_gap": 4.2,
        "selected_year": 2024
    }

    print("Testing AI insights...")
    print("=" * 50)
    insights = generate_employment_insights(test_context)
    print(insights)
    print("=" * 50)
    answer = ask_employment_question(
        "Which county needs the most urgent intervention?",
        test_context
    )
    print(answer)