import asyncio
import logging

from nextcord.ext import commands, tasks

from src.config import configs
from src.managers import rest_client_session_manager


class TaskLooper(commands.Cog):

    def __init__(self, client):
        self.client = client
        # self.transition_sessions.start()
        self.client_session = rest_client_session_manager.get_client_session(configs['REST_API']['BASE_URL'])
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(configs['APP']['LOGGING_LEVEL'])

    @tasks.loop(seconds=5.0)
    async def transition_sessions(self):
        response = await self.client_session.put('/updater/transition')
        json_obj = await response.json()
        aws = []

        def transition(s):
            return
        for session in json_obj['sessions']:
            aws.append(transition(session))

        self.logger.debug(f'Transitioning {len(aws)} sessions')
        await asyncio.gather(*aws)

    @transition_sessions.before_loop
    async def before(self):
        self.logger.info('Starting transition_sessions loop.')
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(TaskLooper(client))
