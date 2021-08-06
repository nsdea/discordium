import channel
import exceptions
import http_manager

class Guild:
    def __init__(self, guild_id):
        data = http_manager.get_request(f'guilds/{guild_id}', params={'with_counts': True})

        self.data = data
        try:
            self.name = data['name']
        except KeyError:
            raise exceptions.GuildNotFound(guild_id) 

        self.id = guild_id
        self.member_count = data['approximate_member_count']
        self.online_coint = data['approximate_presence_count']
        self.boost_tier = data['premium_tier']

    def create_channel(self, name: str, text: bool=True):
        request = http_manager.post_request(f'guilds/{self.id}/channels', json_data={'name': name, 'type': 0 if type else 2})

        return channel.Channel(request['id'])

    def __str__(self) -> str:
        return self.name