
import random


class MusicPlayer:
    """
    This is a class as a music player that provides to play, stop, add songs, remove songs, set volume, shuffle, and switch to the next or previous song.
    """

    def __init__(self):
        """
        Initializes the music player with an empty playlist, no current song, and a default volume of 50.
        """
        self.playlist = []
        self.current_song = None
        self.volume = 50

    def add_song(self, song):
        """
        Adds a song to the playlist.
        :param song: The song to add to the playlist, str.
        >>> musicPlayer = MusicPlayer()
        >>> musicPlayer.add_song("song1")
        >>> musicPlayer.playlist
        ['song1']

        """
        self.playlist.append(song)
        if not self.current_song:
            self.current_song = song

    def remove_song(self, song):
        """
        Removes a song from the playlist.
        :param song: The song to remove from the playlist, str.
        >>> musicPlayer = MusicPlayer()
        >>> musicPlayer.playlist = ["song1", "song2"]
        >>> musicPlayer.remove_song("song1")
        >>> musicPlayer.playlist
        ['song2']

        """
        if song in self.playlist:
            self.playlist.remove(song)
            if song == self.current_song:
                if self.playlist:
                    self.current_song = self.playlist[0]
                else:
                    self.current_song = None

    def play(self):
        """
        Plays the current song in the playlist.
        :return: The current song in the playlist, or False if there is no current song.
        >>> musicPlayer = MusicPlayer()
        >>> musicPlayer.playlist = ["song1", "song2"]
        >>> musicPlayer.current_song = "song1"
        >>> musicPlayer.play()
        'song1'

        """
        return self.current_song if self.current_song else False

    def stop(self):
        """
        Stops the current song in the playlist.
        :return: True if the current song was stopped, False if there was no current song.
        >>> musicPlayer = MusicPlayer()
        >>> musicPlayer.playlist = ["song1", "song2"]
        >>> musicPlayer.current_song = "song1"
        >>> musicPlayer.stop()
        True

        """
        if self.current_song:
            self.current_song = None
            return True
        return False

    def switch_song(self):
        """
        Switches to the next song in the playlist.
        :return: True if the next song was switched to, False if there was no next song.
        >>> musicPlayer = MusicPlayer()
        >>> musicPlayer.playlist = ["song1", "song2"]
        >>> musicPlayer.current_song = "song1"
        >>> musicPlayer.switch_song()
        True

        """
        if self.current_song and self.playlist.index(self.current_song) < len(self.playlist) - 1:
            self.current_song = self.playlist[self.playlist.index(
                self.current_song) + 1]
            return True
        return False

    def previous_song(self):
        """
        Switches to the previous song in the playlist.
        :return: True if the previous song was switched to, False if there was no previous song.
        >>> musicPlayer = MusicPlayer()
        >>> musicPlayer.playlist = ["song1", "song2"]
        >>> musicPlayer.current_song = "song2"
        >>> musicPlayer.previous_song()
        True

        """
        if self.current_song and self.playlist.index(self.current_song) > 0:
            self.current_song = self.playlist[self.playlist.index(
                self.current_song) - 1]
            return True
        return False

    def set_volume(self, volume):
        """
        Sets the volume of the music player,ifthe volume is between 0 and 100 is valid.
        :param volume: The volume to set the music player to,int.
        :return: True if the volume was set, False if the volume was invalid.
        >>> musicPlayer = MusicPlayer()
        >>> musicPlayer.set_volume(50)
        >>> musicPlayer.volume
        50

        """
        if 0 <= volume <= 100:
            self.volume = volume
            return True
        return False

    def shuffle(self):
        """
        Shuffles the playlist.
        :return: True if the playlist was shuffled, False if the playlist was empty.
        >>> musicPlayer = MusicPlayer()
        >>> musicPlayer.playlist = ["song1", "song2"]
        >>> musicPlayer.shuffle()
        True

        """
        if self.playlist:
            random.shuffle(self.playlist)
            if self.current_song in self.playlist:
                self.current_song = self.playlist[self.playlist.index(
                    self.current_song)]
            else:
                self.current_song = self.playlist[0]
            return True
        return False


def main():
    musicPlayer = MusicPlayer()
    musicPlayer.add_song("song1")
    print(musicPlayer.playlist)
    musicPlayer.playlist = ["song1", "song2"]
    musicPlayer.remove_song("song1")
    print(musicPlayer.playlist)
    musicPlayer.playlist = ["song1", "song2"]
    musicPlayer.current_song = "song1"
    print(musicPlayer.play())
    print(musicPlayer.stop())
    musicPlayer.playlist = ["song1", "song2"]
    musicPlayer.current_song = "song1"
    print(musicPlayer.switch_song())
    musicPlayer.playlist = ["song1", "song2"]
    musicPlayer.current_song = "song2"
    print(musicPlayer.previous_song())
    musicPlayer.set_volume(50)
    print(musicPlayer.volume)
    musicPlayer.playlist = ["song1", "song2"]
    print(musicPlayer.shuffle())


if __name__ == "__main__":
    main()
