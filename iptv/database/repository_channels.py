from iptv.database.database_manager import DatabaseManager


class Channel:
    """Represents a channel with its id, name, and URL."""

    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url

    def __repr__(self):
        return f"Channel(id={self.id}, name='{self.name}', url='{self.url}')"

    def __getitem__(self, key):
        """Allow accessing attributes using dictionary-style indexing."""
        if key == 'id':
            return self.id
        elif key == 'name':
            return self.name
        elif key == 'url':
            return self.url
        else:
            raise KeyError(f"'{key}' not found in Channel")


class RepositoryChannel:
    def __init__(self, db_file):
        """Initialize the ChannelCRUD class with a DatabaseManager."""
        self.db_file = db_file

    def create(self, name, url):
        """Create a new channel in the 'channels' table."""
        query = "INSERT INTO channels (name, url) VALUES (?, ?)"
        params = (name, url)
        with DatabaseManager(self.db_file) as db:
            db.execute_query(query, params)
        print(f"Channel '{name}' created successfully.")

    def get_channels(self):
        """Fetch all channels from the 'channels' table and return them as Channel objects."""
        query = "SELECT id, name, url FROM channels"
        with DatabaseManager(self.db_file) as db:
            rows = db.fetch_all(query)

            # Convertir cada fila a un objeto Channel
            channels = [Channel(id=row[0], name=row[1], url=row[2]) for row in rows]
        return channels

    def get_channel_by_id(self, channel_id):
        """Fetch a channel by its ID and return it as a Channel object."""
        query = "SELECT id, name, url FROM channels WHERE id = ?"
        params = (channel_id,)
        with DatabaseManager(self.db_file) as db:
            rows = db.fetch_all(query, params)

            # Si se encuentra el canal, crear un objeto Channel, sino devolver None
            if rows:
                row = rows[0]  # Solo hay un resultado, ya que buscamos por ID
                channel = Channel(id=row[0], name=row[1], url=row[2])
                return channel
            else:
                return None

    def update(self, channel_id, new_name, new_url):
        """Update a channel's name and URL by its ID."""
        query = "UPDATE channels SET name = ?, url = ? WHERE id = ?"
        params = (new_name, new_url, channel_id)
        with DatabaseManager(self.db_file) as db:
            db.execute_query(query, params)
        print(f"Channel ID {channel_id} updated successfully.")

    def delete(self, channel_id):
        """Delete a channel by its ID."""
        query = "DELETE FROM channels WHERE id = ?"
        params = (channel_id,)
        with DatabaseManager(self.db_file) as db:
            db.execute_query(query, params)
        print(f"Channel ID {channel_id} deleted successfully.")
