async def send_message(message: Message, user_message: str) -> None:
    if  not user_message:
        print('Message was empty because intents were not enabled probably')
        return
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]
    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        
        
@bot.event
async def on_message(message: Message) -> None:
    if message.author == bot.user:
        return
    username:str = str(message.author)
    userMessage: str = str(message.content)
    channel: str = str(message.channel)
    print(f'[{channel}] {username}: {userMessage}')
    await send_message(message, userMessage)