import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()


api_key = os.getenv("GROQ_API_KEY")


client = Groq(api_key=api_key)

def get_summary(content: str):
    """
    Sends the note content to Llama 3 and returns a concise summary.
    """
    if not content:
        return "No content to summarize."
        
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes notes concisely."
                },
                {
                    "role": "user",
                    "content": f"Please summarize this note in one sentence: {content}",
                }
            ],
            model="llama-3.3-70b-versatile", # Using Llama 3 
        )
        
        # Extract the summary text
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Summary unavailable."