#import subprocess
#def convert720p(source):
    #new_file_name = source + 'tiny_720p.mp4'
   # cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    #subprocess.run(cmd, capture_output=True)
    
    

# videos/tasks.py
import subprocess
from pathlib import Path

def convert720p(src: str) -> None:
    """
    Konvertiert eine Videodatei nach 720p und speichert sie als *_720p.mp4.
    """
    src_path = Path(src)
    dst_path = src_path.with_stem(src_path.stem + "_720p").with_suffix(".mp4")

    cmd = [
        "ffmpeg",
        "-i", str(src_path),
        "-s", "hd720",
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "aac", "-strict", "-2",
        str(dst_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
