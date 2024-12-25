import asyncio
import random
import time
from concurrent.futures import ThreadPoolExecutor

import aiohttp
import requests

from iptv.models.database.channel import Channel


def is_url_responsive(channel, timeout=5):
    """
    Checks if a channel's URL is responsive within the specified timeout period.

    :param channel: The channel object that contains the URL to test.
    :param timeout: Timeout in seconds for the HTTP request (default is 5 seconds).
    :return: True if the URL is responsive (status code 200), False otherwise.
    """
    try:
        # Perform a HEAD request to check the URL without downloading the content
        response = requests.head(channel.url, timeout=timeout)

        # Check if the response code indicates success (200)
        return response.status_code == 200

    except requests.RequestException as e:
        # If there's any exception (timeout, connection error, etc.), the channel is considered offline
        print(f"Error checking channel '{getattr(channel, 'name', 'Unknown')}': {e}")
        return False


def filter_responsive_channels(channels):
    """
    Filters out non-responsive channels by checking their URLs in parallel,
    and updates the 'tuned' status of non-responsive channels.

    :param channels: List of channels.
    :return: List of responsive channels.
    """

    # Limiting the max number of threads to 100
    batch_size = 100
    max_workers = min(batch_size, len(channels))

    # Process channels in batches of 100
    for i in range(0, len(channels), batch_size):
        batch = channels[i:i + batch_size]
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(check_channel, batch))

    return [channel for channel in results if channel is not None]


def check_channel(channel):
    """
    Checks if a channel is responsive and updates its 'tuned' status.

    :param channel: The channel to test.
    :return: The channel if responsive, None if not.
    """
    if not is_url_responsive(channel):
        print(f"Offline channel: {channel.name}")
        Channel.update_channel(channel.id, {"tuned": False})
        return None
    else:
        print(f"Online channel: {channel.name}")
        Channel.update_channel(channel.id, {"tuned": True})

    # Introduce a small delay between requests
    time.sleep(random.uniform(0.1, 0.5))  # Random delay between 100ms to 500ms

    return channel


async def check_channel_async(channel, session):
    """
    Asynchronously checks if a channel is responsive and updates its 'tuned' status.

    :param channel: The channel to test.
    :param session: The aiohttp session to make the HTTP request.
    :return: None
    """
    async with session.get(channel.url) as response:
        if response.status != 200:
            Channel.update_channel(channel.id, {"tuned": False})
        else:
            Channel.update_channel(channel.id, {"tuned": True})


async def filter_responsive_channels_async(channels):
    """
    Filters out non-responsive channels asynchronously by checking their URLs in parallel,
    and updates the 'tuned' status of non-responsive channels.

    :param channels: List of channels.
    :return: None
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for channel in channels:
            tasks.append(check_channel_async(channel, session))
        await asyncio.gather(*tasks)
