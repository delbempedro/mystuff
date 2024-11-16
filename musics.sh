clear
echo "Album Name: "
read album_name
echo "Youtube Link: "
read album_link

yt-dlp -x --audio-format mp3 -o "%(playlist_index)s - %(title)s.%(ext)s" --playlist-start 1 --ignore-errors $album_link