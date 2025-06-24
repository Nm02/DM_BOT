import aiohttp


async def generateRespond(prompt, system_prompt = None, model = "phi3"):
    if not system_prompt:
        # Prompt del sistema (para definir el comportamiento del asistente)
        with open(r"SystemPrompt.txt","r") as file:
            system_prompt = file.read()

    # Prompt del usuario (simula la duda del usuario)
    user_prompt = prompt
    full_prompt = f"<|system|>\n{system_prompt}\n{user_prompt}"


    # Hacemos la llamada a Ollama con el modelo mistral
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://localhost:11434/api/generate',
            json={
                "model": model,
                "prompt": full_prompt,
                "stream": False
            }
        ) as resp:
            data = await resp.json()
            return data["response"]

    # Mostrar respuesta
    return response.json()["response"]