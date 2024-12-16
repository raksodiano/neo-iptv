from concurrent.futures import ThreadPoolExecutor
import os
import requests


def load_channels():
    """Load channels from an M3U playlist file and filter out non-responsive URLs."""
    current_dir = os.path.dirname(__file__)  # Get the current directory
    database_dir = os.path.join(current_dir, '..', 'database')  # Go one level up and access the 'database' folder
    m3u_file_path = os.path.join(database_dir, 'index.m3u')  # Full path to the M3U file

    channels = []
    current_channel = {}

    try:
        # Open the M3U file and read line by line
        with open(m3u_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue  # Skip empty lines

                # Handle M3U metadata (for example, #EXTINF)
                if line.startswith('#EXTINF:'):
                    # Extract channel metadata (duration, channel name)
                    metadata = line[8:].split(',', 1)
                    current_channel['duration'] = metadata[0]  # Duration in seconds
                    current_channel['name'] = metadata[1] if len(metadata) > 1 else 'Unknown'
                    continue

                # If a URL or file path is found, assume it's the stream URL for the channel
                if line and 'url' not in current_channel:
                    current_channel['url'] = line
                    # Only add the channel if it has a valid 'name'
                    if 'name' in current_channel and current_channel['name']:
                        channels.append(current_channel)  # Add channel to the list
                    current_channel = {}  # Reset for the next channel

        # Remove the first channel if it contains the URL '#EXTM3U' (header)
        if channels and channels[0]['url'] == '#EXTM3U':
            channels.pop(0)

        # Filter out non-responsive URLs
        channels = filter_responsive_channels(channels)
        return channels

    except FileNotFoundError:
        print(f"Error: {m3u_file_path} not found.")  # File was not found
        return None
    except Exception as e:
        print(f"Error: {str(e)}")  # Catch any other errors
        return None


def is_url_responsive(url):
    """
    Checks if a URL is responsive within a timeout period.
    :param url: The URL to test.
    :return: True if the URL is responsive, False otherwise.
    """
    try:
        print(f"Ping: {url}")
        response = requests.head(url, timeout=3)  # Perform a HEAD request
        return response.status_code == 200  # Check if the status code indicates success
    except requests.RequestException:
        return False  # Any exception or timeout means the URL is not responsive


def filter_responsive_channels(channels):
    """
    Filters out non-responsive channels by checking their URLs in parallel.
    :param channels: List of channels.
    :return: List of responsive channels.
    """

    def check_channel(channel):
        return channel if is_url_responsive(channel['url']) else None

    with ThreadPoolExecutor(max_workers=50) as executor:  # Use 50 threads
        results = list(executor.map(check_channel, channels))

    return [channel for channel in results if channel is not None]  # Remove None values


def get_channel_index_by_url(channels, current_channel_url):
    """
    Finds the index of a channel in the list based on its URL.

    :param channels: List of channels (each channel is a dictionary or an object).
    :param current_channel_url: URL of the current channel to search for.
    :return: Index of the found channel, or -1 if it does not exist.
    """
    return next(
        (i for i, channel in enumerate(channels) if channel['url'] == current_channel_url), -1
    )
