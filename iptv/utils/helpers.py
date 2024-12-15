import os


def load_channels():
    """Load channels from an M3U playlist file."""
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

        return channels

    except FileNotFoundError:
        print(f"Error: {m3u_file_path} not found.")  # File was not found
        return None
    except Exception as e:
        print(f"Error: {str(e)}")  # Catch any other errors
        return None
