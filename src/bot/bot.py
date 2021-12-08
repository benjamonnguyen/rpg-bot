import os
import logging

from nextcord import Intents
from nextcord.ext.commands import AutoShardedBot

from src import configs

logger = logging.getLogger(__name__)
logger.setLevel(configs['APP']['LOGGING_LEVEL'])


def build() -> AutoShardedBot:
    bot = AutoShardedBot(command_prefix=configs['BOT']['CMD_PREFIX'],
                         help_command=None,
                         intents=_get_intents())
    _load_cogs(bot)

    @bot.event
    async def on_ready():
        logger.info(f'{bot.user} has connected to Discord!')
        logger.info(f'shard_count: {len(bot.shards)}')

    return bot


def _load_cogs(bot):
    for filename in os.listdir(configs['BOT']['COGS_PATH']):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            logger.info(f'Loaded cogs.{filename[:-3]}')


def _get_intents() -> Intents:
    return Intents(guilds=True,
                   reactions=True,
                   messages=True,
                   voice_states=True,
                   dm_messages=False,
                   dm_reactions=False)
