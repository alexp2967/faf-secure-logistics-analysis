import ollama

response = ollama.chat(
    model="phi3",
    messages=[
        {
            "role": "user",
            "content": """You are a freight data analyst assistant.
Summarize this data in exactly 2 clear sentences for a military logistics analyst:
- Truck carries 63% of US freight by weight
- Air carries 0.03% by weight but has 95x higher value per ton
- Rail carries 7% of freight at the lowest value per ton"""
        }
    ]
)

print(response["message"]["content"])