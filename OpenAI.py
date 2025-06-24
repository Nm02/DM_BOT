import aiohttp
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # o ponelo directamente si es solo de prueba

async def generateRespond(prompt, system_prompt=None, model = "gpt-4.1"):
    if not system_prompt:
        # Prompt del sistema (para definir el comportamiento del asistente)
        with open(r"AdvancedSystemPrompt.txt", "r") as file:
            system_prompt = file.read()

    # Formato para la API de OpenAI
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    async with aiohttp.ClientSession() as session:
        async with session.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,  # o "gpt-3.5-turbo"
                "messages": messages,
                "temperature": 0.7,
                "stream": False
            }
        ) as resp:
            if resp.status != 200:
                error = await resp.text()
                raise Exception(f"OpenAI API error: {resp.status} - {error}")
            data = await resp.json()
            return data["choices"][0]["message"]["content"]
