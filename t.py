print(
	'Started...'
)
import pytube
from pytube import YouTube
for link in 'https://youtu.be/1BVgpX4w0Wk'.split():
	video = YouTube(link)
	print('Retrieved video...')
	print(video)
	print(dir(video))
	for stream in video.fmt_streams:
		print(stream)
	print(
		'Done!'
	)