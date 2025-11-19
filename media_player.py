"""Platform for the KEF Wireless Speakers."""
import logging
import voluptuous as vol

from homeassistant.components.media_player import (
    PLATFORM_SCHEMA,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    STATE_OFF,
    STATE_ON,
    STATE_PLAYING,
    STATE_PAUSED,
    STATE_UNAVAILABLE
)
import homeassistant.helpers.config_validation as cv
import pykefcontrol

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the KEF platform."""
    host = config.get(CONF_HOST)
    add_entities([KEFMediaPlayer(host)], True)


class KEFMediaPlayer(MediaPlayerEntity):
    """Representation of a KEF Speaker."""

    def __init__(self, host):
        """Initialize the KEF device."""
        from pykefcontrol import KefConnector
        self._connector = KefConnector(host)
        self._name = self._connector.speaker_name + ' ' + self._connector.speaker_model
        self._volume = 0.0
        self._source = None
        self._source_list = ["wifi", "bluetooth", "tv", "optical", "coaxial", "analog"]
        self._state = MediaPlayerState.OFF
        self._media_title = None
        self._media_image_url = None

    @property
    def device_info(self):
        """Return device info."""
        return {
            "name": self._connector.speaker_name,
            "model": self._connector.speaker_model,
            "firmware": self._connector.firmware_version,
        }

    @property
    def device_class(self):
        return "speaker"

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the player."""
        return self._state

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return self._volume

    @property
    def is_volume_muted(self):
        """Boolean if volume is currently muted."""
        return self._volume == 0

    @property
    def source(self):
        """Name of the current input source."""
        return self._source

    @property
    def source_list(self):
        """List of available input sources."""
        return self._source_list

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        if self.state == MediaPlayerState.PLAYING or self.state == MediaPlayerState.PAUSED:
            return (
                MediaPlayerEntityFeature.VOLUME_SET
                | MediaPlayerEntityFeature.VOLUME_STEP
                | MediaPlayerEntityFeature.TURN_ON
                | MediaPlayerEntityFeature.TURN_OFF
                | MediaPlayerEntityFeature.SELECT_SOURCE
                | MediaPlayerEntityFeature.PLAY
                | MediaPlayerEntityFeature.PAUSE
                | MediaPlayerEntityFeature.NEXT_TRACK
                | MediaPlayerEntityFeature.PREVIOUS_TRACK
            )
        else:
            return (
                MediaPlayerEntityFeature.VOLUME_SET
                | MediaPlayerEntityFeature.VOLUME_STEP
                | MediaPlayerEntityFeature.TURN_ON
                | MediaPlayerEntityFeature.TURN_OFF
                | MediaPlayerEntityFeature.SELECT_SOURCE
            )

    @property
    def media_image_url(self):
        """Return the media image URL."""
        return self._media_image_url

    @property
    def media_title(self):
        """Return the media title."""
        return self._media_title

    def turn_on(self):
        """Turn the media player on."""
        self._connector.power_on()

    def turn_off(self):
        """Turn the media player off."""
        self._connector.power_off()

    def set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        self._connector.set_volume(int(volume * 100))
        self._volume = volume

    def select_source(self, source):
        """Select input source."""
        self._connector.source = source
        self._source = source

    def media_play(self):
        """Simulate play media player."""
        if self._state != MediaPlayerState.PLAYING:
            self._connector.toggle_play_pause()

    def media_pause(self):
        """Simulate pause media player."""
        if self._state == MediaPlayerState.PLAYING:
            self._connector.toggle_play_pause()

    def media_next_track(self):
        """Send next track command."""
        self._connector.next_track()

    def media_previous_track(self):
        """Send previous track command."""
        self._connector.previous_track()

    def update(self):
        """Get the latest details from the device."""
        self._volume = self._connector.volume / 100.0 if self._connector.volume else 0.0
        self._source = self._connector.source
        self._media_title = None
        self._media_image_url = None
        
        if self._connector.status == "powerOn":
            self._state = MediaPlayerState.ON
            song_info = self._connector.get_song_information()
            if self._source == "wifi" and song_info["title"] is not None:
                self._media_title = song_info["title"]
                self._media_image_url = song_info["cover_url"]
                if self._connector.is_playing:
                    self._state = MediaPlayerState.PLAYING
                elif self._media_title is not None:
                    self._state = MediaPlayerState.PAUSED
        if self._connector.status == "powerOff":
            self._state = MediaPlayerState.OFF
