
import os
from django.conf import settings
from django.http import HttpResponse,FileResponse
from django.shortcuts import render,redirect
import youtube_dl    
def youtube_video(request):
    if request.method == 'POST' and 'youtube_link' in request.POST:
        youtube_link = request.POST.get('youtube_link')
        if youtube_link:
            try:
                ydl_opts = {
                    'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                    'outtmpl': os.path.join(settings.MEDIA_ROOT, 'youtube_video.mp4'),
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }],
                    'retries': 10,
                    'format_sort': 'bestvideo[height<=1080]',
                }


                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                       
                       ydl.download([youtube_link])

                video_file_path = os.path.join(settings.MEDIA_ROOT, 'youtube_video.mp4')

                if os.path.exists(video_file_path):
                    return FileResponse(open(video_file_path, 'rb'), content_type='video/mp4',
                                        as_attachment=True, filename='downloaded_video.mp4')
                else:
                    error_message = "Error downloading video: Video file not found"
                    return HttpResponse(error_message, status=500)

            except Exception as e:
                error_message = f"Error downloading video: {str(e)}"
                return HttpResponse(error_message, status=500)

    return render(request,'youtube_video.html')  # Bad Request if incorrect form data or method


