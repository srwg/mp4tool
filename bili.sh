for i in *; do cd $i/64; ffmpeg  -i video.m4s -i audio.m4s  -c:v copy -c:a copy -strict experimental ../../$i.mp4; cd ../..; done
