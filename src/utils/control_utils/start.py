import asyncio
from typing import Dict
import json
import random
import logging

import aiohttp
from nextcord.ext.commands.context import Context
from nextcord.message import Message

from src.utils import player
from src.enums import Link, AudioPath
from src.config import configs
from src.managers import rest_client_session_manager

logger = logging.getLogger(__name__)
logger.setLevel(configs['APP']['LOGGING_LEVEL'])
GREETINGS = ['Howdy howdy! Let\'s do this thang.',
             'Hey there! Let\'s get started!',
             'It\'s productivity o\'clock!',
             'Let\'s ketchup on some work!']
client_session = rest_client_session_manager.get_client_session(configs['REST_API']['BASE_URL'])


async def start(ctx: Context, interval_settings: Dict):
    msg = await ctx.send('Starting session...')
    payload = {
        'bindings': {
            'channel_id': ctx.channel.id,
            'voice_channel_id': ctx.author.voice.channel.id,
            'message_id': msg.id
        },
        'interval_settings': interval_settings
    }
    try:
        resp = await client_session.post('/session/start', json=payload)
        if resp.status == 409:
            asyncio.create_task(ctx.send('There is already a session in this channel.'))
            logger.debug(f'Session already exists for channel: {ctx.channel.name} (409)')
        else:
            resp.raise_for_status()
        json_obj = await resp.json()
        interval_settings = json_obj.get('interval_settings')

        msg = await _send_start_msg(ctx, interval_settings)  # edit initial msg
        asyncio.create_task(_play_start_audio(ctx))

        # queue_transition_request()

    except (aiohttp.ClientResponseError, KeyError) as e:
        asyncio.create_task(ctx.send('There seems to be a problem on the backend. Please try again later.\n\n'
                                     'If the problem persists, notify @Support in the support server!\n' + Link.SUPPORT))
        logger.critical(f'Bad response for start request: {json.dumps(payload, indent=4)}\n{e}')


# TODO message_builder.start_message()
async def _send_start_msg(ctx: Context, json_obj) -> Message:
    # await cleanup.pins(session)
    msg = await ctx.send(random.choice(GREETINGS) + '\n{}')
                         # embed=msg_builder.timer_status_embed(session, start=True))
    # await asyncio.gather(ctx.send(embed=msg_builder.settings_embed(session)), msg.pin())
    return msg


async def _play_start_audio(ctx: Context):
    vc = await ctx.author.voice.channel.connect()
    player.play(vc, AudioPath.POMO_START, 5.0)
    await ctx.send('Playing audio!')
