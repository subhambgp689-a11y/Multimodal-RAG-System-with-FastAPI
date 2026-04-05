import os
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def is_llm_ready():
    return bool(OPENAI_API_KEY and OPENAI_API_KEY.strip())


def generate_answer(query, context):
    lower_query = query.lower()
    table_keywords = ["table", "tabular", "rows", "columns", "compare", "list", "matrix", "overview"]
    should_force_table = any(keyword in lower_query for keyword in table_keywords)

    system_prompt = (
        "You are an automotive assistant. Answer using ONLY the provided context. "
        "If the user asks for tabular data, respond with a valid markdown table. "
        "Do not wrap the markdown table in code fences, and do not include any extra prose outside the table. "
        "If a table is not appropriate, answer concisely in plain text."
    )

    user_prompt = f"""
    Context:
    {context}

    Question:
    {query}
    """

    if should_force_table:
        user_prompt = (
            "If the question can be answered with tabular data, return a valid markdown table only. "
            "If the information is not tabular, still answer using the context.\n\n" + user_prompt
        )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
        max_tokens=700,
    )

    return response.choices[0].message.content.strip()