#Discord
import discord
from discord.ext import commands

#Request
import requests

#.env
import os
from dotenv import load_dotenv

#IA
import Ollama
import OpenAI


# Declarar que hara el bot
intents = discord.Intents.default()
intents.message_content = True           # Necesario para acceder al contenido de los mensajes
intents.members = True                   # Necesario para detectar nuevos miembros



#Crear bot
bot = commands.Bot(command_prefix="!", intents = intents)   # Creo un bot que respondera a los mensajes con el prefijo declarado


#Comandos
@bot.command()               #Decorador para ejecutar una funcion ante un comando
async def saludo(ctx, *args):
    respond=" ".join(args)
    await ctx.send(respond)


@bot.command()
async def DM(ctx, *args):
    # Obtener los últimos 10 mensajes del canal
    messages = [message async for message in ctx.channel.history(limit=10, oldest_first=True)]
    messages.pop(0)

    # Construir el historial de conversación
    conversation = ""
    for message in messages:
        role = "user" if message.author != bot.user else "assistant"
        conversation += f"<|{role}|>\n{message.content}\n"

    # Agregar el nuevo mensaje del usuario
    user_input = " ".join(args)
    conversation += f"<|user|>\n{user_input}\n<|assistant|>"

    
    aux = await ctx.send("espera un segundo...")

    #Generar respuesta
    respond = await Ollama.generateRespond(conversation, model = "nous-hermes")
    # respond = await OpenAI.generateRespond(conversation)


    # Eliminar el mensaje anterior
    await aux.delete()

    # Discord permite como máximo 2000 caracteres por mensaje
    MAX_LEN = 2000
    if len(respond) <= MAX_LEN:
        await ctx.send(respond)
    else:
        for i in range(0, len(respond), MAX_LEN):
            await ctx.send(respond[i:i+MAX_LEN])

@bot.command()
async def DM_plus(ctx, *args):
    # Obtener los últimos 10 mensajes del canal
    messages = [message async for message in ctx.channel.history(limit=10, oldest_first=True)]
    messages.pop(0)

    # Construir el historial de conversación
    interactions=0
    conversation = ""
    for message in messages:
        if message.author != bot.user:
            role = "user"
        else:
            role = "assistant"
            interactions+=1
        conversation += f"<|{role}|>\n{message.content}\n"

    if interactions >= 5:
        await ctx.send("Lo sentimos, esta conversacion ya no puede utilizar los modelos avanzados. Intenta con el comando !DM")
        return

    # Agregar el nuevo mensaje del usuario
    user_input = " ".join(args)
    conversation += f"<|user|>\n{user_input}\n<|assistant|>"

    
    aux = await ctx.send("espera un segundo...")

    #Generar respuesta
    # respond = await Ollama.generateRespond(conversation, model = "nous-hermes")
    respond = await OpenAI.generateRespond(conversation)


    # Eliminar el mensaje anterior
    await aux.delete()

    # Discord permite como máximo 2000 caracteres por mensaje
    MAX_LEN = 2000
    if len(respond) <= MAX_LEN:
        await ctx.send(respond)
    else:
        for i in range(0, len(respond), MAX_LEN):
            await ctx.send(respond[i:i+MAX_LEN])



@bot.command()
@commands.has_permissions(manage_messages=True)  # Solo admins/mods
async def limpiar(ctx, number=100):
    """Borra los últimos X mensajes (por defecto 100)"""
    await ctx.channel.purge(limit=number)



#Eventos
@bot.event #Decorador para ejecutar una funcion ante un evento
async def on_ready(): #Funcion que se desencadena cuando el bot se ejecuta
    print(f"estamos dentro {bot.user}")



@bot.event
async def on_member_join(member): #Al ingresar un nuevo miembro
    guild = member.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }

    # Buscar el rol de administrador por nombre
    admin_role = discord.utils.get(guild.roles, name="Administrador")
    # Si encontramos el rol de administrador, le damos permisos
    if admin_role:
        overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True)

    # Crear o ubicar categoría
    category = discord.utils.get(guild.categories, name="Chats privados")
    if category is None:
        category = await guild.create_category("Chats privados")

    # Crear canal
    channel_name = f"chat-{member.name}".lower().replace(" ", "-")
    private_channel = await guild.create_text_channel(
        name=channel_name,
        overwrites=overwrites,
        category=category,
        topic=f"Canal privado para {member.display_name}"
    )

    await private_channel.send(f"¡Hola {member.mention}! Este es tu canal privado con el bot 😊")




#Leer toke y ejecutar bot
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)

