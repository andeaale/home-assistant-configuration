"""
Plex Clients - Media players for every connected Plex Client

Here are the advantages and disadvantages of this component over the HA
standard media_player.plex component

Advantages:
- No discovery needed (queries your plex server directly for connected players)
- Control volume (media_player.plex doesn't even show the volume control)
- Displays proper player names (i.e. Living Room Apple TV instead of Plex Web
Safari - This is because media_player.plex grabs the name from the session
instead of the player object)
- Works with all Plex Clients (media_player.plex never displays the below)
    - Mobile (iPhone, iPad, etc)
    - PlexConnect (How earlier generation Apple TV's can access Plex)
- Displays episode specific data (when playing a season, media_player.plex will
display the first episode name and show thumbnail)
    - Current episode thumbnail
    - Current show and episode name
    - Current season and episode number
- Shows disconnected clients as idle (when a player disconnects,
media_player.plex keeps the player as 'playing' and adds a hidden player as
'idle'.)
- No configurator, plex.conf, or plex token required (this probably works for
me because I've set Plex to NOT require authentication for my local LAN)

Disadvantages:
- Crappy, hardly tested, non-supported code

Here you can see a visual comparison between media_player.plex and this component:
https://github.com/JesseWebDotCom/home-assistant-configuration/blob/master/docs/images/plex_plexclients_comparison.png

To Do:
- Clean up code
- Resolve local names (i.e. "Jesse's Macbook" instead of "Plex Web (Safari)"")
- Dynamically create an HA group with all players
    - Separate the group between local and remote (using plex_client['player_location'])
- Remove playback control (ex. SUPPORT_PLEXCLIENT = None) per player type

Limitations:
- Can't retrieve current volume (but can set)
- No functional playback controls on PlexConnect clients
- No functional playback controls on web clients (probably same reason above)
- No functional playback controls on ios clients (apple thing?)


Feel free to improve this code and even incorporate into HA (which I do not have the
time to do) - I just ask that you let me know (so I can add your improvements or
migrate to something better).

Thanks

"""

import homeassistant.helpers.config_validation as cv
import logging
import voluptuous as vol
from datetime import timedelta
from homeassistant.util import Throttle

import homeassistant.util as util
from homeassistant.components.media_player import (
    MEDIA_TYPE_TVSHOW, MEDIA_TYPE_VIDEO, MEDIA_TYPE_MUSIC, SUPPORT_NEXT_TRACK,
    SUPPORT_PREVIOUS_TRACK, SUPPORT_PAUSE, SUPPORT_STOP, SUPPORT_VOLUME_SET,
    SUPPORT_PLAY, MediaPlayerDevice, PLATFORM_SCHEMA)
from homeassistant.const import (
    DEVICE_DEFAULT_NAME, STATE_IDLE, STATE_OFF, STATE_PAUSED, STATE_PLAYING,
    STATE_UNKNOWN, CONF_HOST, CONF_PORT)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import (track_utc_time_change)

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'plexclients'

SUPPORT_PLEXCLIENT = SUPPORT_PAUSE | SUPPORT_PREVIOUS_TRACK | SUPPORT_NEXT_TRACK | \
    SUPPORT_STOP | SUPPORT_PLAY | SUPPORT_VOLUME_SET

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 32400

MIN_TIME_BETWEEN_SCANS = timedelta(seconds=10)
MIN_TIME_BETWEEN_FORCED_SCANS = timedelta(seconds=1)


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST, default=DEFAULT_HOST): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
})

def get_plexresponse(url):
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    return requests.get(url, verify=False)

def get_plexclients(plex_server_url):
    clients_url =  '{}/status/sessions'.format(plex_server_url)

    _LOGGER.info('Getting plex clients: ' + clients_url)

    response = get_plexresponse(clients_url)

    import xml.etree.ElementTree as ET
    root = ET.fromstring(response.text)

    plex_clients = {}
    for session in root.iter('Video'):
        plex_client = {}

        plex_client['plex_server_url'] = plex_server_url
        plex_client['player_name'] = ''
        plex_client['player_state'] = ''
        plex_client['player_address'] = ''
        plex_client['player_location'] = ''
        plex_client['player_id'] = ''
        plex_client['tv_show_name'] = ''
        plex_client['tv_season_number'] = ''
        plex_client['tv_episode_name'] = ''
        plex_client['tv_episode_number'] = ''
        plex_client['media_type'] = ''
        plex_client['media_year'] = ''
        plex_client['media_name'] = ''
        plex_client['media_id'] = ''
        plex_client['media_thumbnail'] = ''

        plex_client['media_type'] = session.attrib['type']
        if plex_client['media_type'] == 'episode':
            plex_client['tv_show_name'] = session.attrib['grandparentTitle']
            plex_client['tv_season_number'] = session.attrib['parentIndex']
            plex_client['tv_episode_name'] = session.attrib['title']
            plex_client['tv_episode_number'] = session.attrib['index']

        plex_client['media_year'] = session.attrib['year']
        plex_client['media_duration'] = session.attrib['duration']
        plex_client['media_name'] = session.attrib['title']
        plex_client['media_id'] = session.attrib['ratingKey']
        plex_client['media_thumbnail'] = plex_client['plex_server_url'] + session.attrib['thumb']

        root_iter = session.getiterator()

        for element in root_iter:
            if element.tag =='Player':
                plex_client['player_name'] = element.attrib['title']
                plex_client['player_state'] = element.attrib['state']
                plex_client['player_address'] = element.attrib['address']
                plex_client['player_id'] = element.attrib['machineIdentifier']

            if element.tag =='Session':
                plex_client['player_location'] = element.attrib['location']

        plex_clients[plex_client['player_id']] = plex_client

    return plex_clients

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    # get and store config values

    host = config.get(CONF_HOST)
    port = str(config.get(CONF_PORT))

    setup_plexserver(host, port, hass, add_devices_callback)

def setup_plexserver(host, port, hass, add_devices_callback):

    plex_server_url = 'http://{}:{}'.format(host, port)

    all_clients = {}
    track_utc_time_change(hass, lambda now: update_clients(), second=30)

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_FORCED_SCANS)
    def update_clients():

        current_clients = get_plexclients(plex_server_url)

        new_clients = []
        for client_id, client in current_clients.items():
            if client_id not in all_clients:
                # create a new client
                new_client = PlexClient(client, update_clients)
                all_clients[client_id] = new_client
                new_clients.append(new_client)
            else:
                # update existing client
                all_clients[client_id].set_client(client)

        if new_clients:
            add_devices_callback(new_clients)

        # Make old clients idle
        for client_id, client in all_clients.items():
            if client_id not in current_clients:
                client._client_player_state = ''

    update_clients()


class PlexClient(MediaPlayerDevice):
    """Representation of a PLEXCLIENT client device."""

    def __init__(self, client, update_clients):
        """Initialize the PLEXCLIENT device."""
        self.update_clients = update_clients
        self.set_client(client)

    def set_client(self, client):
        """Set the client property."""
        self._client = client
        self._client_player_state = str(client['player_state'])

    @property
    def unique_id(self):
        """Return the id of this plex client."""
        return self._client['player_id']

    @property
    def name(self):
        """Return the name of the device."""
        return self._client['player_name']

    @property
    def state(self):
        """Return the state of the player."""
        if self._client_player_state == 'playing':
            return STATE_PLAYING
        elif self._client_player_state == 'paused':
            return STATE_PAUSED
        else:
            return STATE_IDLE

    @property
    def _active_media_plexapi_type(self):
        """Get the active media type required by PlexAPI commands."""
        if self.media_content_type is MEDIA_TYPE_MUSIC:
            return 'music'
        else:
            return 'video'

    @property
    def media_content_id(self):
        """Content ID of current playing media."""
        return self._client['media_id']

    @property
    def media_content_type(self):
        """Content type of current playing media."""
        if self._client['media_type'] == 'episode':
            return MEDIA_TYPE_TVSHOW
        elif self._client['media_type'] == 'movie':
            return MEDIA_TYPE_VIDEO
        elif self._client['media_type'] == 'track':
            return MEDIA_TYPE_MUSIC
        return None

    @property
    def media_title(self):
        """Title of current playing media."""
        if self._client['media_type'] == 'episode':
            return self._client['media_name']
        elif self._client['media_type'] == 'movie':
            return '{} ({})'.format(self._client['media_name'], self._client['media_year'])
        elif self._client['media_type'] == 'track':
            return self._client['media_name']
        return None

    @property
    def media_season(self):
        """Season of curent playing media (TV Show only)."""
        return self._client['tv_season_number']

    @property
    def media_series_title(self):
        """The title of the series of current playing media (TV Show only)."""
        return self._client['tv_show_name']

    @property
    def media_episode(self):
        """Episode of current playing media (TV Show only)."""
        return self._client['tv_episode_number']

    @property
    def media_duration(self):
        """Duration of current playing media in seconds."""
        return self._client['media_duration']

    @property
    def media_image_url(self):
        """Image url of current playing media."""
        return self._client['media_thumbnail']

    @property
    def supported_media_commands(self):
        """Flag of media commands that are supported."""
        return SUPPORT_PLEXCLIENT

    def set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        str_volume = str(int(volume * 100))
        print("volume=" + str_volume)
        _LOGGER.info("volume=" + str_volume)
        self._playback('setParameters?volume='+str_volume)

    def _playback(self, command):
        url = '{}/system/players/{}/playback/{}'.format(self._client['plex_server_url'], self._client['player_address'], command)
        self.get_plexresponse(url)

    def media_play(self):
        """Send play command."""
        self._playback('play')

    def media_pause(self):
        """Send pause command."""
        self._playback('pause')

    def media_stop(self):
        """Send stop command."""
        self._playback('stop')

    def media_next_track(self):
        """Send next track command."""
        self._playback('skipNext')

    def media_previous_track(self):
        """Send previous track command."""
        self._playback('skipPrevious')

    @property
    def volume_level(self):
        """Return the volume level."""
        #return self._client.volume / 100
        return 100

    @property
    def is_volume_muted(self):
        """Volume muted."""
        #return self._client.muted
        return False

    def update(self):
        """Get the latest details."""
        self.update_clients(no_throttle=True)

    def get_plexresponse(self, url):
        import requests
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        return requests.get(url, verify=False)
