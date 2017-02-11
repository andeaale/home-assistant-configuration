"""
PLEXDEVICES
Displays and controls active and previously connected Plex streamers and clients

Why this over media_player.plex
A plex streamer is any device that streams from your plex server.  A plex client
is a streamer but can also be remotely controlled.  The existing media_player.plex
component only shows clients so you are missing out on things like remote users
and PlexConnected Apple TV's (how gen 2 and 3 Apple TV's connect to Plex).

media_player.plex is also missing a bunch of meta data, doesn't let you control
things like volume, and more.  There's also a ton of additional features only
available in this PlexDevices component.

Overall Benefits:
    - Misc:
        - Remote users - see what remote users are streaming
        - PlexConnect gen 2/3 Apple TV's - see whats streaming on your PlexConnect Apple TV devices
        - Speedy load (info displays in 0-1 second over media_player.plex 5-10 seconds)
        - Always art - display media art if thumbnail not available (good for items in Plex with no poster)
        - Distinguish between Web browser clients - i.e. Any name starting with "Plex Web" get username@ip appended
            - Ex. "Plex Web (Safari)" is shown as "Plex Web (Safari) - jesse@192.168.1.10"
            - Customize with friendly names for a better experience:
                homeassistant:
                    customize:
                        media_player.plex_r06sa6ozi98:
                          friendly_name: Jesse's Laptop
        - Unique entity ID name - they are now media_player.plex_{id}, where {id} is the unique player ID
            - This avoids ambuguity issues like media_player.plex_web_safari, media_player.plex_web_safari2
                - Scenario: Imagine you had an automation based on an entity name (ex. media_player.plex_web_safari)
                    - The first system that ever connects over safari gets this entity name
                    - Now you have a timing issue to ensure the right system gets the right name
                    - You also may have a different issue if the wrong syste gets the name and kicks off your automation
    - Automations:
        - A bunch of new attribute values to use in your automations:
            - ex. Raise the lights when volume low or muted:
                - Use volume_level and is_muted
            - ex. Alert when a remote user is streaming
                - Use friendly_name or entity name
            - ex. Alert when your child plays a video from the "Adult Movies" library)
                - Use friendly_name and app_name (Plex Library Name)
            - ex. Alert when your child plays a song from the "Adult Music" library)
                - Use friendly_name and app_name (Plex Library Name)
            - ex. Turn off the lights when playing a video from video libraries but never from music libraries
                - Use friendly_name and app_name (Plex Library Name)
            - ex. Alert you when you won't have time to finish watching a movie
                - Use media_duration (length of movie) and media_position (where you are in the movie) to calculate when the movie will finish / compare that to your calendar appointments, kid's bedtime, etc
            - Too many more to list

    - Controls:
        - On/Off: On does nothing but Off stops playing media (good to kick of unwanted users / kids past their bedtime)
        - Volume/Mute: Can set and mute (Plex client syncs with what HA tells it, not the other way around)
        - Progress: Display a media progress bar
        - PlayMedia: Make a plex client play a movie, tv show, or music playlist
    - Movies:
        - Display name as "Name (Year)", ex. Blair Witch (2016)
        - Display library name below movie title (ex. "Adult Movies")
    - TV:
        - Display episode and season numbers with leading 0's, ex 02, 05
        - Display "Show S##E##", ex. Rick and Morty S02E05
        - Display episode thumbnail instead of show thumbnail
    - Music:
        - Display Artist (track artist, if not use album artist)
        - Set albumn name property

Installation:
- Copy to your ha\custom_components\media_player directory
- You may need to "chmod 777 plexdevices.py" on linux systems
- Add it to your config:
    media_player:
      - platform: plexdevices
- Create the same ha\plex.conf file media_player.plex uses or ha should display
a configurator to create it for you

Compatibility:
- Here's what I've tested it with so far:
    - NVidia Shield
    - PlexConnected Apple TV 3
    - Plex Web Safari
    - Plex Web Chrome
    - Tivo Plex App
    - iPhone Plex App

Known Issues:
- After speedy load, controls will not be available until regular load (5-10 seconds)
- PlexConnect Apple TV's (issues occur in HA and the Plex Now Playing web page)
    - No working controls (since they aren't full clients)
    - Playing music is not visible (likely because it plays as background music)
    - Playing a season only shows first episode
- NVidia Shield freezes with PlayMedia Music or Playlist (might just be my Shield)

PlayMedia - You can test using the HA GUI (Services | Media_Player | PlayMedia):
    MUSIC:
    {
        "entity_id" : "media_player.plex_bb72ed6a42aa26ea_com_plexapp_android",
        "media_content_id": "{ \"library_name\" : \"Jesse Music\", \"artist_name\" : \"Adele\", \"album_name\" : \"25\", \"track_name\" : \"hello\", \"shuffle\": \"0\" }",
        "media_content_type": "MUSIC"
    }

    PLAYLIST:
    {
        "entity_id" : "media_player.plex_bb72ed6a42aa26ea_com_plexapp_android",
        "media_content_id": "{\"playlist_name\" : \"The Best of Disco\", \"shuffle\": \"0\" }",
        "media_content_type": "PLAYLIST"
    }

    Note: Episode number starts at 0 and increments to the total episode count in all seasons (i.e. no season numbers, just episode indexes)
    EPISODE:
    {
        "entity_id" : "media_player.plex_bb72ed6a42aa26ea_com_plexapp_android",
        "media_content_id": "{ \"library_name\" : \"Adult TV\", \"show_name\" : \"Rick and Morty\", \"episode_number\" : 15, \"shuffle\": \"0\" }",
        "media_content_type": "EPISODE"
    }

    VIDEO:
    {
        "entity_id" : "media_player.plex_bb72ed6a42aa26ea_com_plexapp_android",
        "media_content_id": "{ \"library_name\" : \"Adult Movies\", \"video_name\" : \"Blade\", \"shuffle\": \"0\" }",
        "media_content_type": "VIDEO"
    }
"""
# Required to get a web response from Plex and ignore HTTPS warnings
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Required to parse the xml web response from Plex
# If available, use the C implementation: its faster and consumes less memory
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import asyncio
import json
import logging
import os
from datetime import timedelta
from urllib.parse import urlparse

import homeassistant.util as util
from homeassistant.components.media_player import (
    MEDIA_TYPE_TVSHOW, MEDIA_TYPE_VIDEO, MEDIA_TYPE_MUSIC, SUPPORT_NEXT_TRACK,
    SUPPORT_PREVIOUS_TRACK, SUPPORT_PAUSE, SUPPORT_STOP, SUPPORT_VOLUME_SET,
    SUPPORT_PLAY, SUPPORT_VOLUME_MUTE, SUPPORT_TURN_OFF, SUPPORT_SEEK,
    MediaPlayerDevice)
from homeassistant.const import (
    DEVICE_DEFAULT_NAME, STATE_IDLE, STATE_OFF, STATE_PAUSED, STATE_PLAYING,
    STATE_UNKNOWN)
from homeassistant.loader import get_component
from homeassistant.helpers.event import (track_utc_time_change)

REQUIREMENTS = ['plexapi==2.0.2']
MIN_TIME_BETWEEN_SCANS = timedelta(seconds=10)
MIN_TIME_BETWEEN_FORCED_SCANS = timedelta(seconds=1)

PLEX_CONFIG_FILE = 'plex.conf'

# Map ip to request id for configuring
_CONFIGURING = {}
_LOGGER = logging.getLogger(__name__)

SUPPORT_PLEX = SUPPORT_PAUSE | SUPPORT_PREVIOUS_TRACK | SUPPORT_NEXT_TRACK | \
    SUPPORT_STOP | SUPPORT_VOLUME_SET | SUPPORT_PLAY | SUPPORT_VOLUME_MUTE | \
    SUPPORT_SEEK | SUPPORT_TURN_OFF

def dump(obj):
    """DELETE ME - THIS IS FOR TROUBLESHOOTING ONLY"""
    for attr in dir(obj):
        if hasattr( obj, attr ):
            print( "obj.%s = %s" % (attr, getattr(obj, attr)))

def get_xml_attrib_value(element, attrib_name):
    """Get an XML element attribute or return '' if it doesn't exist"""
    value = element.attrib[attrib_name] if attrib_name in element.attrib else ''
    if value is None:
        value = ''
    return value

def get_streamers(plexserver):
    """Get systems that are streaming but not clients"""

    streamers_url = plexserver.url('/status/sessions')
    response = requests.get(streamers_url, verify=False)
    tree = ET.fromstring(response.text)

    streamers = {}
    for MediaContainer in tree:
        if MediaContainer.tag in ['Video', 'Track']:
            streamer = {}

            streamer['app_name'] = plexserver.library.sectionByID(get_xml_attrib_value(MediaContainer, 'librarySectionID')).title

            # use art if thumbnail cannot be found
            streamer['media_image_url'] = plexserver.url(get_xml_attrib_value(MediaContainer, 'thumb'))
            thumb_response = requests.get(streamer['media_image_url'], verify=False)
            if thumb_response.status_code != 200:
                streamer['media_image_url'] = plexserver.url(get_xml_attrib_value(MediaContainer, 'art'))

            streamer['media_title'] = get_xml_attrib_value(MediaContainer, 'title')
            streamer['media_year'] = get_xml_attrib_value(MediaContainer, 'year')
            media_duration = get_xml_attrib_value(MediaContainer, 'duration')
            streamer['media_duration'] = int(media_duration) if media_duration != '' else 0
            media_position = get_xml_attrib_value(MediaContainer, 'viewOffset')
            streamer['media_position'] = int(media_position) if media_position != '' else 0
            streamer['media_content_id'] = get_xml_attrib_value(MediaContainer, 'ratingKey')

            # type
            media_content_type = get_xml_attrib_value(MediaContainer, 'type')
            if media_content_type == 'episode':
                streamer['media_content_type'] = MEDIA_TYPE_TVSHOW
            elif media_content_type == 'movie':
                streamer['media_content_type'] =  MEDIA_TYPE_VIDEO
            elif media_content_type == 'track':
                streamer['media_content_type'] =  MEDIA_TYPE_MUSIC
            else:
                streamer['media_content_type'] =  None

            # music
            streamer['media_album_artist'] = get_xml_attrib_value(MediaContainer, 'grandparentTitle')
            if get_xml_attrib_value(MediaContainer, 'originalTitle') != '':
                streamer['media_artist'] = get_xml_attrib_value(MediaContainer, 'originalTitle')
            else:
                streamer['media_artist'] = streamer['media_album_artist']
            streamer['media_album_name'] = get_xml_attrib_value(MediaContainer, 'parentTitle')
            streamer['media_track'] = get_xml_attrib_value(MediaContainer, 'index')

            # episode
            streamer['media_series_title'] = get_xml_attrib_value(MediaContainer, 'grandparentTitle')
            streamer['media_season'] = get_xml_attrib_value(MediaContainer, 'parentIndex').zfill(2) # leading zero, ex 02
            streamer['media_episode'] = get_xml_attrib_value(MediaContainer, 'index').zfill(2) # leading zero, ex 02

            # movie
            if media_content_type == MEDIA_TYPE_VIDEO:
                streamer['media_title'] = '{} ({})'.format(streamer['media_title'],streamer['media_year'])

            for Player in MediaContainer.iterfind('Player'):
                streamer['unique_id'] = get_xml_attrib_value(Player, 'machineIdentifier')
                streamer['name'] = get_xml_attrib_value(Player, 'title')
                #streamer['device'] = get_xml_attrib_value(Player, 'device')

                state = get_xml_attrib_value(Player, 'state')
                if state == 'playing':
                    streamer['state'] = STATE_PLAYING
                elif state == 'paused':
                    streamer['state'] = STATE_PAUSED
                else:
                    streamer['state'] = STATE_IDLE
                streamer['address'] = get_xml_attrib_value(Player, 'address')

            for User in MediaContainer.iterfind('User'):
                streamer['username'] = get_xml_attrib_value(User, 'title')

            # for Session in MediaContainer.iterfind('Session'):
            #     streamer['location'] = get_xml_attrib_value(Session, 'location')

            streamers[streamer['unique_id']] = streamer

    return streamers

def config_from_file(filename, config=None):
    """Small configuration file management function."""
    if config:
        # We're writing configuration
        try:
            with open(filename, 'w') as fdesc:
                fdesc.write(json.dumps(config))
        except IOError as error:
            _LOGGER.error('Saving config file failed: %s', error)
            return False
        return True
    else:
        # We're reading config
        if os.path.isfile(filename):
            try:
                with open(filename, 'r') as fdesc:
                    return json.loads(fdesc.read())
            except IOError as error:
                _LOGGER.error('Reading config file failed: %s', error)
                # This won't work yet
                return False
        else:
            return {}


def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Setup the Plex platform."""
    config = config_from_file(hass.config.path(PLEX_CONFIG_FILE))
    if len(config):
        # Setup a configured PlexServer
        host, token = config.popitem()
        token = token['token']
    # Via discovery
    elif discovery_info is not None:
        # Parse discovery data
        host = urlparse(discovery_info[1]).netloc
        _LOGGER.info('Discovered PLEX server: %s', host)

        if host in _CONFIGURING:
            return
        token = None
    else:
        return

    setup_plexserver(host, token, hass, add_devices_callback)


def setup_plexserver(host, token, hass, add_devices_callback):
    """Setup a plexserver based on host parameter."""
    import plexapi.server
    import plexapi.exceptions

    try:
        plexserver = plexapi.server.PlexServer('http://%s' % host, token)
    except (plexapi.exceptions.BadRequest,
            plexapi.exceptions.Unauthorized,
            plexapi.exceptions.NotFound) as error:
        _LOGGER.info(error)
        # No token or wrong token
        request_configuration(host, hass, add_devices_callback)
        return

    # If we came here and configuring this host, mark as done
    if host in _CONFIGURING:
        request_id = _CONFIGURING.pop(host)
        configurator = get_component('configurator')
        configurator.request_done(request_id)
        _LOGGER.info('Discovery configuration done!')

    # Save config
    if not config_from_file(
            hass.config.path(PLEX_CONFIG_FILE),
            {host: {'token': token}}):
        _LOGGER.error('failed to save config file')

    _LOGGER.info('Connected to: http://%s', host)

    all_devices = {}
    all_sessions = {}
    track_utc_time_change(hass, lambda now: update_clients_streamers(), second=30)

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_FORCED_SCANS)
    def update_clients_streamers():
        """Update the client and streamer objects."""

        # Get streamers
        active_streamers = get_streamers(plexserver)

        new_streamers = []
        for unique_id, active_streamer in active_streamers.items():
            #dump(active_streamer)
            if unique_id not in all_devices:
                # add new streamer
                new_streamer = PlexDevice(None, active_streamer, all_sessions, update_clients_streamers,
                                        update_sessions)
                all_devices[unique_id] = new_streamer
                new_streamers.append(new_streamer)
            else:
                # update if not a client
                #if all_devices[unique_id].is_streamer:
                all_devices[unique_id].reset(None, active_streamer)

        if new_streamers:
            add_devices_callback(new_streamers)

        # Make old devices idle
        for unique_id, device in all_devices.items():
            if not (unique_id  in active_streamers):
                device.set_state('idle')

        # Get clients
        try:
            active_clients = plexserver.clients()
        except plexapi.exceptions.BadRequest:
            _LOGGER.exception('Error listing plex devices')
            return
        except OSError:
            _LOGGER.error(
                'Could not connect to plex server at http://%s', host)
            return

        active_client_ids = []
        new_clients = []
        for active_client in active_clients:
            #dump(active_client)

            # For now, let's allow all deviceClass types
            if active_client.deviceClass in ['badClient']:
                continue

            active_client_ids.append(active_client.machineIdentifier)

            if active_client.machineIdentifier not in all_devices:
                # add new clients
                new_client = PlexDevice(active_client, None, all_sessions, update_clients_streamers,
                                        update_sessions)
                all_devices[active_client.machineIdentifier] = new_client
                new_clients.append(new_client)
            else:
                # update existing clients
                all_devices[active_client.machineIdentifier].reset(active_client, None)

        if new_clients:
            add_devices_callback(new_clients)


    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_FORCED_SCANS)
    def update_sessions():
        """Update the sessions objects."""
        try:
            sessions = plexserver.sessions()
        except plexapi.exceptions.BadRequest:
            _LOGGER.exception('Error listing plex sessions')
            return

        all_sessions.clear()
        for session in sessions:
            all_sessions[session.player.machineIdentifier] = session

    update_clients_streamers()
    update_sessions()


def request_configuration(host, hass, add_devices_callback):
    """Request configuration steps from the user."""
    configurator = get_component('configurator')

    # We got an error if this method is called while we are configuring
    if host in _CONFIGURING:
        configurator.notify_errors(
            _CONFIGURING[host], 'Failed to register, please try again.')

        return

    def plex_configuration_callback(data):
        """The actions to do when our configuration callback is called."""
        setup_plexserver(host, data.get('token'), hass, add_devices_callback)

    _CONFIGURING[host] = configurator.request_config(
        hass, 'Plex Media Server', plex_configuration_callback,
        description=('Enter the X-Plex-Token'),
        entity_picture='/static/images/logo_plex_mediaserver.png',
        submit_caption='Confirm',
        fields=[{'id': 'token', 'name': 'X-Plex-Token', 'type': ''}]
    )

class PlexDevice(MediaPlayerDevice):
    """Representation of a Plex device."""

    # pylint: disable=attribute-defined-outside-init
    def __init__(self, client, streamer, all_sessions, update_clients_streamers, update_sessions):
        """Initialize the Plex device."""
        from plexapi.utils import NA

        self.na_type = NA

        client_unique_id = self._convert_na_to_none(client.machineIdentifier) if client else ''
        streamer_unique_id = streamer['unique_id'] if streamer else client_unique_id
        self._unique_id = streamer_unique_id

        # rename the entity
        # self.entity_id = "%s.%s_%s" % (
        #     'media_player', 'plex', self._unique_id.lower().replace('-','_'))

        #client_username = self._convert_na_to_none(client.machineIdentifier) if client else ''
        streamer_username = streamer['username'] if streamer else '' #client_username
        self._username = streamer_username

        #client_address = self._convert_na_to_none(client.machineIdentifier) if client else ''
        streamer_address = streamer['address'] if streamer else '' #client_address
        self._address = streamer_address

        client_name = self._convert_na_to_none(client.title) if client else ''
        streamer_name = streamer['name'] if streamer else client_name
        # if streamer_name.lower().startswith('plex web'):
        #     streamer_name = streamer_name + " - " + self._username + "@" + self._address
        self._name = streamer_name

        self.client = None
        self.streamer = None
        self.all_sessions = all_sessions
        self.update_clients_streamers = update_clients_streamers
        self.update_sessions = update_sessions
        self._season = None
        self._volume_level = 1 # since we can't retrieve volume remotely
        self._previous_volume_level = 1 # Used in fake muting
        self._volume_muted = False # since we can't retrieve mute state remotely
        self.reset(client, streamer)

    def reset(self, client, streamer):
        """reset the device."""
        if client:
            self.client = client
        if streamer:
            self.streamer = streamer

        self._media_position_updated_at = util.dt.utcnow()

        client_state = self._convert_na_to_none(self.session.player.state) if self.session and self.session.player else 'idle'
        streamer_state = self.streamer['state'] if self.streamer else client_state
        self.set_state(streamer_state)

        client_duration = self._convert_na_to_none(self.session.duration) if self.session else 0
        streamer_duration = self.streamer['media_duration'] if self.streamer else client_duration
        self._media_duration = streamer_duration

        client_position = self._convert_na_to_none(self.session.duration) if self.session else 0
        streamer_position = self.streamer['media_position'] if self.streamer else client_position
        self._media_position = streamer_position

        # SEASON
        if self.media_content_type is MEDIA_TYPE_TVSHOW:
            if self.is_streamer:
                self._season = self.streamer['media_season']
            else:
                self._season = str(self.session.parentIndex).zfill(2) # leading zero, ex 02

        if self._season is not None:
            self._season = str(self._season)

    def set_state(self, state):
        """Set the state property."""
        if state == 'playing':
            self._state = STATE_PLAYING
        elif state == 'paused':
            self._state = STATE_PAUSED
        elif state == 'idle':
            self._state = STATE_IDLE
        elif state == 'off':
            self._state = STATE_OFF
        else:
            self._state = STATE_UNKNOWN

    @property
    def is_streamer(self):
        """Return true if streamer, false if client"""
        return (self.streamer is not None)

    @property
    def unique_id(self):
        """Return the id of this plex client."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the client."""
        return self._name

    @property
    def app_name(self):
        """Library name of playing media"""
        if self.is_streamer:
            return self.streamer['app_name']

        if self.session:
            section = self.session.server.library.sectionByID(self.session.librarySectionID)
            return section.title

    @property
    def session(self):
        """Return the session, if any."""
        if not self.is_streamer:
            return self.all_sessions.get(self.client.machineIdentifier, None)

    @property
    def state(self):
        """Return the state of the client."""
        return self._state

    def update(self):
        """Get the latest details."""

        self.update_clients_streamers(no_throttle=True)
        self.update_sessions(no_throttle=True)

    # pylint: disable=no-self-use, singleton-comparison
    def _convert_na_to_none(self, value):
        """Convert PlexAPI _NA() instances to None."""
        # PlexAPI will return a "__NA__" object which can be compared to
        # None, but isn't actually None - this converts it to a real None
        # type so that lower layers don't think it's a URL and choke on it
        if value is self.na_type:
            return None
        else:
            return value

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
        if self.is_streamer:
            return self.streamer['media_content_id']

        if self.session:
            return self._convert_na_to_none(self.session.ratingKey)

    @property
    def media_content_type(self):
        """Content type of current playing media."""
        if self.is_streamer:
            return self.streamer['media_content_type']

        if self.session is None:
            return None
        media_type = self.session.type
        if media_type == 'episode':
            return MEDIA_TYPE_TVSHOW
        elif media_type == 'movie':
            return MEDIA_TYPE_VIDEO
        elif media_type == 'track':
            return MEDIA_TYPE_MUSIC
        return None

    @property
    def media_artist(self):
        """Artist of current playing media, music track only."""
        if self.media_content_type is MEDIA_TYPE_MUSIC:
            if self.is_streamer:
                return self.streamer['media_artist']

            if self.media_content_type is MEDIA_TYPE_MUSIC:
                # use album artist if track artist is missing
                if self._convert_na_to_none(self.session.originalTitle) is not None:
                    return self._convert_na_to_none(self.session.originalTitle)
                else:
                    return self._convert_na_to_none(self.session.grandparentTitle)

    @property
    def media_album_name(self):
        """Album name of current playing media, music track only."""
        if self.media_content_type is MEDIA_TYPE_MUSIC:
            if self.is_streamer:
                return self.streamer['media_album_name']

            if self.media_content_type is MEDIA_TYPE_MUSIC:
                return self._convert_na_to_none(self.session.parentTitle)

    @property
    def media_album_artist(self):
        if self.media_content_type is MEDIA_TYPE_MUSIC:
            if self.is_streamer:
                return self.streamer['media_album_artist']

            if self.media_content_type is MEDIA_TYPE_MUSIC:
                return self._convert_na_to_none(self.session.grandparentTitle)

    @property
    def media_track(self):
        """Track number of current playing media, music track only."""
        if self.media_content_type is MEDIA_TYPE_MUSIC:
            if self.is_streamer:
                return self.streamer['media_track']

            if self.media_content_type is MEDIA_TYPE_MUSIC:
                return self._convert_na_to_none(self.session.index)

    @property
    def media_duration(self):
        """Duration of current playing media in seconds."""
        return self._media_duration

    @property
    def media_image_url(self):
        """Image url of current playing media."""
        if self.is_streamer:
            return self.streamer['media_image_url']

        if self.session:
            if self.media_content_type is MEDIA_TYPE_TVSHOW:
                thumb_url = self.session.server.url(self.session.thumb)
            else:
                thumb_url = self._convert_na_to_none(self.session.thumbUrl)
            if str(self.na_type) in thumb_url:
                # Audio tracks build their thumb urls internally before passing
                # back a URL with the PlexAPI _NA type already converted to a
                # string and embedded into a malformed URL
                thumb_url = None
            return thumb_url

    @property
    def media_title(self):
        """Title of current playing media."""
        if self.is_streamer:
            return self.streamer['media_title']

        # find a string we can use as a title
        if self.session:
            # append year for movies
            if self.media_content_type is MEDIA_TYPE_VIDEO:
                if self._convert_na_to_none(self.session.title) is not None \
                and self._convert_na_to_none(self.session.year) is not None:
                    return '{} ({})'.format(self.session.title, self.session.year)

            return self._convert_na_to_none(self.session.title)

    @property
    def media_season(self):
        """Season of curent playing media (TV Show only)."""
        return self._season

    @property
    def media_series_title(self):
        """The title of the series of current playing media (TV Show only)."""
        if self.is_streamer:
            return self.streamer['media_series_title']

        if self.media_content_type is MEDIA_TYPE_TVSHOW:
            return self._convert_na_to_none(self.session.grandparentTitle)

    @property
    def media_episode(self):
        """Episode of current playing media (TV Show only)."""
        if self.is_streamer:
            return self.streamer['media_episode']

        if self.media_content_type is MEDIA_TYPE_TVSHOW:
            if self._convert_na_to_none(self.session.index) is not None:
                return str(self.session.index).zfill(2) # leading zero, ex 03

    @property
    def media_duration(self):
        """Duration of current playing media in seconds."""
        return self._media_duration

    @property
    def media_position(self):
        """Position of current playing media in seconds."""
        return self._media_position

    @property
    def media_position_updated_at(self):
        """When was the position of the current playing media valid."""
        return self._media_position_updated_at

    @property
    def supported_media_commands(self):
        """Flag of media commands that are supported."""
        #return SUPPORT_PLEX
        if self.client is None: # or self.state == STATE_UNKNOWN or self.state == STATE_IDLE:
            return None
        else:
            return SUPPORT_PLEX

    def set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        if self.client:
            self.client.setVolume(int(volume * 100),
                              self._active_media_plexapi_type)
            self._volume_level = volume

    @property
    def volume_level(self):
        """Return the volume level of the client (0..1)."""
        if self.client:
            return self._volume_level

    @property
    def is_volume_muted(self):
        """Return boolean if volume is currently muted."""
        if self.client:
            return self._volume_muted

    @asyncio.coroutine
    def async_turn_off(self):
        """Turn the client off."""
        if self.client:
            self.media_stop() # Fake it since we can't turn the client off

    def mute_volume(self, mute):
        """Mute the volume.
        Since we can't actually mute, we'll:
        - On mute, store volume and set volume to 0
        - On unmute, set volume to previously stored volume
        """
        if self.client:
            self._volume_muted = mute
            if mute:
                self._previous_volume_level = self._volume_level
                self.set_volume_level(0)
            else:
                self.set_volume_level(self._previous_volume_level)

    @asyncio.coroutine
    def async_media_play(self):
        """Send play command."""
        if self.client:
            self.client.play(self._active_media_plexapi_type)

    @asyncio.coroutine
    def async_media_pause(self):
        """Send pause command."""
        if self.client:
            self.client.pause(self._active_media_plexapi_type)

    @asyncio.coroutine
    def async_media_stop(self):
        """Send stop command."""
        if self.client:
            self.client.stop(self._active_media_plexapi_type)

    def media_next_track(self):
        """Send next track command."""
        if self.client:
            self.client.skipNext(self._active_media_plexapi_type)

    def media_previous_track(self):
        """Send previous track command."""
        if self.client:
            self.client.skipPrevious(self._active_media_plexapi_type)

    @asyncio.coroutine
    def async_play_media(self, media_type, media_id, **kwargs):
        # MUSIC, TVSHOW, VIDEO, EPISODE, CHANNEL or PLAYLIST
        if self.client:
            src = json.loads(media_id)

            media = None
            if media_type == 'MUSIC':
                media = self.client.server.library.section(src['library_name']).get(src['artist_name']).album(src['album_name']).get(src['track_name'])
            elif media_type == 'EPISODE':
                episode_number = int(src['episode_number']) + 1
                media = self.client.server.library.section(src['library_name']).get(src['show_name']).episodes()[episode_number]
            elif media_type == 'PLAYLIST':
                media = self.client.server.playlist(src['playlist_name'])
            elif media_type == 'VIDEO':
                media = self.client.server.library.section(src['library_name']).get(src['video_name'])

            if media:
                self.playMedia(media,shuffle=src['shuffle'])

    '''

    '''

    def playMedia(self, media, **params):
        if self.client:
            import plexapi.playqueue
            server_url = media.server.baseurl.split(':')
            playqueue = plexapi.playqueue.PlayQueue.create(self.client.server,media,**params)
            self.client.sendCommand('playback/playMedia', **dict({
                'machineIdentifier': self.client.server.machineIdentifier,
                'address': server_url[1].strip('/'),
                'port': server_url[-1],
                'key': media.key,
                'containerKey': '/playQueues/%s?window=100&own=1' % playqueue.playQueueID,
            }, **params))
