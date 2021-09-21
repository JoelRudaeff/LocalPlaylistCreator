from __future__ import unicode_literals
import subprocess 
import youtube_dl
from sys import argv
from os import path, remove
from pydub import AudioSegment

YDL_OPTS = {
    'outtmpl': "{output_dir_path}\\%(title)s.%(ext)s",
    'format': 'bestaudio/best',
    'noplaylist': 'true',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}


class Music(object):
    def download(self, url, output_dir_path):
        """
        url, str -> url of the video, "https://www.youtube.com/watch?v=1"
        output_dir_path, str -> the path to the output folder, r"c:\output_dir"
        """
        local_config = YDL_OPTS.copy()        
        local_config['outtmpl'] = local_config['outtmpl'].format(output_dir_path=output_dir_path)
        
        with youtube_dl.YoutubeDL(local_config) as ydl:
            title = ydl.extract_info(url, download = False)['title']
            ydl.download([url])
        return title
    
    def edit_audio(self, file_path, start_cut=None, end_cut=None):
        # Opening file and extracting segment
        song = AudioSegment.from_mp3(file_path)
        
        if start_cut and end_cut:
            start_time_hour, start_time_minute, start_time_second = list(map(int, start_cut.split(":"))) 
            end_time_hour, end_time_minute, end_time_second = list(map(int, end_cut.split(":")))

            # Time to miliseconds
            start_time = start_time_hour * 3600 * 1000 + start_time_minute * 60 * 1000 + start_time_second * 1000
            end_time = end_time_hour * 3600 * 1000 + end_time_minute * 60 * 1000 + end_time_second * 1000
            song = song[start_time:end_time]

        # Insert fade in and out
        song = song.fade_in(2000).fade_out(3000)
        
        # Saving
        remove(file_path)
        song.export(file_path, format="mp3")
    
    def run(self, base_dir):
        """
        Base dir, str -> directory in which all folders we need exist (tmp) and input.txt
        """
        url_list = []
        input_urls_file_path = path.join(base_dir, "input.txt")
        output_dir_path = path.join(base_dir, "tmp")
        
        with open(input_urls_file_path, "r") as input_list:
            url_list = input_list.readlines()
            
        # Remove duplicates
        url_list = list(dict.fromkeys(url_list))
            
        # Starting to iterate over the files
        for line in url_list:
            url = start_cut = end_cut = ""
            # More than one option - currently supports only two arguments
            if " " in line:
                url, start_cut, end_cut = line.split(" ")[0:3]
            else:
                url = line
            
            song_title = self.download(url, output_dir_path)
            #song_title = song_title.replace("|","").replace("/","").replace("\\","").replace(".","").replace("_","").replace("|","")
            file_path = path.join(output_dir_path, song_title) + ".mp3"
            self.edit_audio(file_path, start_cut, end_cut)
        
        # Delete the url_list list marking that we've finished
        remove(input_urls_file_path)
        open(input_urls_file_path, "a").close()


if __name__ == "__main__":
    Music().run()
