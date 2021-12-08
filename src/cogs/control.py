import asyncio
import logging

from nextcord.ext import commands

from src.config import configs
from src.utils.validator import validate_interval_settings
from src.utils import control_utils


class Control(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(configs['APP']['LOGGING_LEVEL'])

    @commands.command()
    async def start(self,
                    ctx: commands.Context,
                    pomodoro: int = None,
                    short_break: int = None,
                    long_break: int = None,
                    intervals: int = None):
        self.logger.debug(f'Received start command from server: {ctx.guild.name}')
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            asyncio.create_task(ctx.send('Please join a voice channel and try again!'))
            return

        interval_settings = {
            'pomodoro': pomodoro,
            'short_break': short_break,
            'long_break': long_break,
            'intervals': intervals
        }
        validate_interval_settings(interval_settings)

        asyncio.create_task(control_utils.start(ctx, interval_settings))

    @start.error
    async def handle_error(self, ctx: commands.Context, e: commands.CommandError):
        if isinstance(e, ValueError):
            asyncio.create_task(ctx.send("Use numbers between 0 and "
                                         f"{configs['PARAMETER']['MAX_INTERVAL_SETTINGS_VALUE']}."))


def setup(client):
    client.add_cog(Control(client))
