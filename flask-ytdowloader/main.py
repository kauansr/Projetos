from app import app
from pytube import YouTube, Playlist
from flask import render_template, redirect, url_for, request
import os
import time

@app.route('/', methods=['GET','POST'])
def home():

    if request.method == 'POST':
        if request.form['uma_musica']:
            try:
                url = request.form['uma_musica']
                ys = YouTube(url)
                musica = ys.streams.get_audio_only()
                baixa = musica.download(
                    output_path="C:/Users/ADM/Music")
                base, ext = os.path.splitext(baixa)
                novo_arquivo = base + '.mp4'
                os.rename(baixa, novo_arquivo)
                        
            except:
                raise('O link deve ser de apenas uma musica')
        
        
        elif request.form['um_video']:
            try:
                url = request.form['um_video']
                yt = YouTube(url)
                video = yt.streams.get_highest_resolution()
                video.download(output_path="C:/Users/ADM/Downloads")
            
            except:
                raise('O link deve ser de apenas um video')
       
        
    

        elif request.form['playlist_musica']:
            try:
                url = request.form['playlist_musica']
                yt = Playlist(url)

                for musicas in yt.video_urls:
                    ys = YouTube(musicas)
                    musica = ys.streams.get_audio_only()
                    baixa = musica.download(
                        output_path="C:/Users/ADM/Music")
                    base, ext = os.path.splitext(baixa)
                    novo_arquivo = base + '.mp4'
                    os.rename(baixa, novo_arquivo)
            
            except:
                raise('O link deve ser de apenas uma playlist de musica')
        

        elif request.form['playlist_video']:
            try:
                url = request.form['playlist_video']
              
                yt = Playlist(url)

                for videos in yt.video_urls:
                    ys = YouTube(videos)
                    video = ys.streams.get_highest_resolution()
                    baixa = video.download(
                        output_path="C:/Users/ADM/Downloads")
            
            except:
                raise('O link deve ser de uma playlist de apenas videos')
        else:
            return redirect(url_for('home'))

    return render_template('home.html')







if __name__ == '__main__':
    app.run(debug=True)