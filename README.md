# spotify-lyrics

A Python script that displays the lyrics to your current Spotify track in your terminal.

![Screenshot](./screenshots/1.png "Screenshot")


## Getting started

### Dependencies

This script requires Python 3.

### Installation and use

1. Save spotify-lyrics.py to a location of your choice (this is where you will run the script from):

    ```
    $ wget https://raw.githubusercontent.com/cjlh/spotify-lyrics/master/spotify-lyrics.py
    ```

2. *(Optional)* Set an alias in your shell for quick use. Examples:

   bash (\~/.bashrc) and zsh (\~/.zshrc):

    ```
    alias spotify-lyrics="python /path/to/spotify-lyrics.py"
    ```

   fish (\~/.config/fish/config.fish):

    ```
    alias spotify-lyrics "python /path/to/spotify-lyrics.py"
    ```

3. Run the script whilst playing music in Spotify -- the lyrics will automatically display as the song changes:

    ```
    $ python /path/to/spotify-lyrics.py
    ```

   Or if an alias is set:

    ```
    $ spotify-lyrics
    ```


## License

This project is licensed under the MIT License.

***
[https://github.com/cjlh/spotify-lyrics](https://github.com/cjlh/spotify-lyrics)
