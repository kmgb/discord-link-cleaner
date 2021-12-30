import hikari
from dotenv import load_dotenv
import utils

import os

load_dotenv()
bot = hikari.GatewayBot(token=os.environ.get('TOKEN'))


def construct_reply(cleaned_urls) -> str:
    list_str = "\n".join('<'+x+'>' for x in cleaned_urls)
    return f"I have sanitized the link(s) in your message:\n{list_str}"


@bot.listen()
# Respond only to GuildMessages, ignore DMs
async def receive_guild_message(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return

    url_list = utils.find_urls(event.content)

    # Clean the URLs and ensure they aren't the same as the original
    cleaned_urls = {y for x in url_list if (y := utils.clean_url(x)) and y not in url_list}

    if cleaned_urls:
        await event.message.respond(construct_reply(cleaned_urls), reply=True)


bot.run()
