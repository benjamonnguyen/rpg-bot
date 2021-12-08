from typing import Dict
import asyncio
import logging

from aiohttp import ClientSession

from src import configs

logger = logging.getLogger(__name__)
logger.setLevel(configs['APP']['LOGGING_LEVEL'])
_client_sessions: Dict[str, ClientSession] = {}


def get_client_session(base_url: str) -> ClientSession:
    if client_session := _client_sessions.get(base_url):
        return client_session
    _client_sessions[base_url] = ClientSession(base_url, loop=asyncio.get_event_loop())
    return _client_sessions.get(base_url)


async def close_all():
    logger.info('Closing all client sessions')
    aws = []
    for session in _client_sessions.values():
        aws.append(session.close())

    await asyncio.gather(*aws)
