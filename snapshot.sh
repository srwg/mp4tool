for i in *.mp4; do
  ffmpeg -i $i -ss 00:00:30 -vframes 1 $i.jpg
done
