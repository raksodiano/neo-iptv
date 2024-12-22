from concurrent.futures import ThreadPoolExecutor

import requests
from iptv.models.database.channel import Channel


def is_url_responsive(channel):
    """
    Checks if a channel is responsive within a timeout period.
    :param channel: The channel to test.
    :return: True if the URL is responsive, False otherwise.
    """
    try:
        response = requests.head(channel.url, timeout=5)  # Perform a HEAD request

        # Determine the color based on the status_code
        if response.status_code == 200:
            color = "\033[32m"  # Green for status_code 200
        else:
            color = "\033[31m"  # Red for any other status_code

        # Reset the color for subsequent text
        reset_color = "\033[0m"

        print(f"Status Code: {response.status_code}, Ping: {color}{getattr(channel, 'name', 'Unknown')}{reset_color}")

        return response.status_code == 200  # Check if the status code indicates success
    except requests.RequestException:
        return False  # Any exception or timeout means the URL is not responsive


def filter_responsive_channels(channels):
    """
    Filters out non-responsive channels by checking their URLs in parallel,
    and updates the 'tuned' status of non-responsive channels.

    :param channels: List of channels.
    :return: List of responsive channels.
    """

    def check_channel(channel):
        if not is_url_responsive(channel):
            # If not responsive, update 'tuned' to False and return None
            print(f"Offline channel: {channel.name}")
            Channel.update_channel(channel.id, {"tuned": False})
            return None

    # Use ThreadPoolExecutor to check channels in parallel
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(check_channel, channels))

    # Return only the channels that are responsive (i.e., not None)
    return [channel for channel in results if channel is not None]
