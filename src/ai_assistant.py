import ollama

MODEL_NAME = "llama3.2"


def ask_ai(question, business_data):
    """
    Ask the local Llama model to analyze business data.

    The AI is strictly instructed to:
    - use only supplied data
    - avoid unsupported assumptions
    - distinguish revenue from profit
    - clearly identify missing information
    """

    prompt = f"""
You are an AI Business Analyst.

You are analyzing a business analytics dashboard.

Your job is to answer the user's question using ONLY the
business data provided below.

================ BUSINESS DATA ================

{business_data}

================ USER QUESTION ================

{question}

================ STRICT DATA RULES ================

RULE 1:
Use ONLY facts, numbers, names, and relationships explicitly
present in the BUSINESS DATA.

RULE 2:
NEVER invent or assume information.

RULE 3:
Revenue does NOT automatically mean:
- high demand
- popularity
- customer preference
- customer satisfaction
- market demand
- product quality
- profitability
- high margin

Do NOT make any of these claims unless the BUSINESS DATA
explicitly contains evidence supporting them.

RULE 4:
Do NOT invent reasons or causes.

For example, if Laptop has the highest revenue, you may say:

" Laptop generated the highest revenue."

You may NOT say:

"Laptop generated the highest revenue because customers
prefer it."

unless customer preference is explicitly present in the data.

RULE 5:
Do NOT confuse revenue with profit.

Revenue = sales generated.

Profit requires cost information.

RULE 6:
Do NOT calculate a percentage, growth rate, margin,
average, comparison, or other derived metric unless the
required numbers are explicitly available in the data.

RULE 7:
If required information is missing, say:

"The available business data is not sufficient to determine this."

Do NOT guess.

RULE 8:
Do not describe correlation or causation unless it is
explicitly supported by the provided data.

RULE 9:
When answering questions about a product, customer,
category, or region, report only what the supplied data
actually shows.

RULE 10:
If the question asks for something that cannot be determined
from the supplied data, clearly state that limitation.

================ ANSWER FORMAT ================

### 📊 Finding

State the direct factual finding from the data.

### 🔎 Analysis

Explain what the finding means ONLY using information
supported by the data.

Do not add assumptions about demand, popularity,
preferences, causes, or reasons.

### 💡 Recommendation

Give a practical recommendation based only on the
available evidence.

If the data is insufficient for a meaningful recommendation,
say so.

================ FINAL SELF-CHECK ================

Before answering, check your response.

REMOVE any unsupported statement involving:

- demand
- popularity
- preference
- satisfaction
- quality
- market behavior
- reasons
- causes
- profitability
- profit margin
- customer behavior

unless the BUSINESS DATA explicitly supports it.

Also check:

1. Did I use only supplied data?
2. Did I invent any number?
3. Did I invent a reason?
4. Did I confuse revenue with profit?
5. Did I make an unsupported claim about customers?
6. Did I calculate something without the required numbers?

If YES to any of these, remove that statement before
returning the final answer.

Return ONLY the final Business Analyst answer.
"""

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.1
            }
        )

        answer = response["message"]["content"]

        return answer

    except Exception as e:
        return (
            "### ⚠️ AI Assistant Error\n\n"
            f"Unable to generate the AI analysis: {str(e)}"
        )