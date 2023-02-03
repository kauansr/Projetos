from pytube import YouTube, Playlist
import os
from time import sleep

print('''Digite sua opcao de dowload:
1 - Download de apenas um video pelo link.
2 - Download de apenas uma musica pelo link.
3 - Download de uma playlist musica pelo link.
4 - Download de uma playlist video pelo link.
0 - Para sair.
''')
print()
pasta = 'caminho dos arquivos'

while True:
    try:
        op = int(input("Digite sua opcao: "))

        if op > 4:
            print('Apenas entre 1 e 4.')
            sleep(1)

        if op == 0:
            sleep(1)
            print('Obrigado por usar.')
            break

        if op == 1:
            url = input('digite a url do video: ')
            yt = YouTube(url)

            print('Titulo:', yt.title)
            video = yt.streams.get_highest_resolution()
            video.download(output_path=pasta)
            print('Download concluido!')

        elif op == 2:
            
            url = input(str('Digite sua url: '))

            
           
            
            ys = YouTube(url)
            
            print('Titulo:', ys.title, 'Baixando...')
            musica = ys.streams.get_audio_only()
            baixa = musica.download(
                output_path=pasta)
            base, ext = os.path.splitext(baixa)
            novo_arquivo = base + '.mp3'
            os.rename(baixa, novo_arquivo)
        
            print(ys.title, 'Download completo!')

            

        elif op == 3:
            
            url = input(str('Digite sua url da playlist de musica: '))
            yt = Playlist(url)


            for musicas in yt.video_urls:
                ys = YouTube(musicas)
                print('Titulo:', ys.title, 'Baixando...')
                musica = ys.streams.get_audio_only()
                baixa = musica.download(
                    output_path=pasta)
                base, ext = os.path.splitext(baixa)
                novo_arquivo = base + '.mp3'
                os.rename(baixa, novo_arquivo)
        

                print(ys.title, 'Download completo!')

        elif op == 4:
            url = input('Digite sua url da playlist de videos: ')
            yt = Playlist(url)

            for videos in yt.video_urls:
                ys = YouTube(videos)
                print('Titulo:', ys.title, 'Baixando...')
                video = ys.streams.get_highest_resolution()
                baixa = video.download(
                    output_path=pasta)
                print(ys.title, 'Download completo!')
    except ValueError:
        print('Apenas entre 1 e 4.')
