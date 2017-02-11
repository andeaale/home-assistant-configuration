# PLEXDEVICES
Displays and controls active and previously connected Plex streamers and clients

## Why not media_player.plex
A plex streamer is any device that streams from your plex server.  A plex client is a streamer but can also be remotely controlled.  The existing media_player.plex component only shows clients so you are missing out on things like remote users and PlexConnected Apple TV's (how gen 2 and 3 Apple TV's connect to Plex).

media_player.plex is also missing a bunch of meta data, doesn't let you control things like volume, and more.  There's also a ton of additional features only available in this PlexDevices component.

### Side by Side Comparison
media_player.plex  |  media_player.plexdevices
--|--
![](images/media_player_plex.png)  |  ![](images/media_player_plexdevices.png)

## Why not Plex WebHooks
Web hooks are good for simple action / reaction (media plays, turn on lights). I use something similar for my Blue Iris setup. If that's all you need, then use the web hooks.  This component not only allows you to do the same but it also:
1. Provides you with a visual map of what's occurring on your plex server (looks cool too)
2. Allows you to manually respond to events
3. Allows you to manually control players (i.e. a single page to remote control every client connected to your plex server)
4. Easier setup and maintenance (nothing to configure on your plex server, nothing new to learn/manage)
5. Doesn't require a plex pass subscription
6. Extensible - We can add functionality as needed

# Benefits
(compared to media_player.plex)
* Misc
  * Remote users - see what remote users are streaming
  * PlexConnect gen 2/3 Apple TV's - see whats streaming on your PlexConnect Apple TV devices
  * Speedy load (info displays in 0-1 second over media_player.plex 5-10 seconds)
  * Always art - display media art if thumbnail not available (good for items in Plex with no poster)
* Automations
  * A bunch of new attribute values to use in your automations:
    * ex. Raise the lights when volume low or muted:
      * Use volume_level and is_muted
    * ex. Alert when a remote user is streaming
      * Use friendly_name or entity name
    * ex. Alert when your child plays a video from the "Adult Movies" library)
      * Use friendly_name and app_name (Plex Library Name)
    * ex. Alert when your child plays a song from the "Adult Music" library)
      * Use friendly_name and app_name (Plex Library Name)
    * ex. Turn off the lights when playing a video from video libraries but never from music libraries
      * Use friendly_name and app_name (Plex Library Name)
    * ex. Alert you when you won't have time to finish watching a movie
      * Use media_duration (length of movie) and media_position (where you are in the movie) to calculate when the movie will finish / compare that to your calendar appointments, kid's bedtime, etc
    * Too many more to list
* Controls
  * On/Off: On does nothing but Off stops playing media (good to kick of unwanted users / kids past their bedtime)
  * Volume/Mute: Can set and mute (Plex client syncs with what HA tells it, not the other way around)
  * Progress: Display a media progress bar
  * PlayMedia: Make a plex client play a movie, tv show, or music playlist
* Movies
  * Display name as "Name (Year)", ex. Blair Witch (2016)
  * Display library name below movie title (ex. "Adult Movies")
* TV
  * Display episode and season numbers with leading 0's, ex 02, 05
  * Display "Show S##E##", ex. Rick and Morty S02E05
  * Display episode thumbnail instead of show thumbnail
* Music:
  * Display Artist (track artist, if not use album artist)
  * Set albumn name property

# Installation
1. Copy to your ha\custom_components\media_player directory
  * You may need to "chmod 777 plexdevices.py" on linux systems
2. Add it to your config:
    media_player:
      - platform: plexdevices
3. Create the same ha\plex.conf file media_player.plex uses or ha should display a configurator to create it for you

# Compatibility
Here's what I've tested it with so far:
* NVidia Shield
* PlexConnected Apple TV 3
* Plex Web Safari
* Plex Web Chrome
* Tivo Plex App
* iPhone Plex App

# Known Issues
* After speedy load, controls will not be available until regular load (5-10 seconds)
* PlexConnect Apple TV's (issues occur in HA and the Plex Now Playing web page)
  * No working controls (since they aren't full clients)
  * Playing music is not visible (likely because it plays as background music)
  * Playing a season only shows first episode
* NVidia Shield freezes with PlayMedia Music or Playlist (might just be my Shield)

# PlayMedia
You can test the PlayMedia service using the HA GUI (Services | Media_Player | PlayMedia)

## Music
```
{
    "entity_id" : "media_player.plex_bb72ed6a42aa26ea_com_plexapp_android",
    "media_content_id": "{ \"library_name\" : \"Jesse Music\", \"artist_name\" : \"Adele\", \"album_name\" : \"25\", \"track_name\" : \"hello\", \"shuffle\": \"0\" }",
    "media_content_type": "MUSIC"
}
```

## Playlists
```
{
    "entity_id" : "media_player.plex_bb72ed6a42aa26ea_com_plexapp_android",
    "media_content_id": "{\"playlist_name\" : \"The Best of Disco\", \"shuffle\": \"0\" }",
    "media_content_type": "PLAYLIST"
}
```

## Episodes
```
{
    "entity_id" : "media_player.plex_bb72ed6a42aa26ea_com_plexapp_android",
    "media_content_id": "{ \"library_name\" : \"Adult TV\", \"show_name\" : \"Rick and Morty\", \"episode_number\" : 15, \"shuffle\": \"0\" }",
    "media_content_type": "EPISODE"
}
```
## Video
```
{
    "entity_id" : "media_player.plex_bb72ed6a42aa26ea_com_plexapp_android",
    "media_content_id": "{ \"library_name\" : \"Adult Movies\", \"video_name\" : \"Blade\", \"shuffle\": \"0\" }",
    "media_content_type": "VIDEO"
}
```
