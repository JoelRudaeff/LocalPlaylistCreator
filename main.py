import os
from music import Music
from manager import Manager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def init_folder():
    """
    Returns False if the input.txt file doesn't exist or empty
    """
    os.makedirs(os.path.join(BASE_DIR, "tmp"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "trash"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "playlist"), exist_ok=True)
    
    input_urls_file_path = os.path.join(BASE_DIR,"input.txt")
    open(input_urls_file_path, "a").close()
    return os.path.isfile(input_urls_file_path) and os.path.getsize(input_urls_file_path) > 0

    
def main():
    if not init_folder():
        print("# Error #\nPlease create a file named: input.txt on the script's folder\nAfterwards fill it with at least one line: [URL] [HH:MM:SS] [HH:MM:SS]")
        print("\n# Exmaple #\nhttps://www.youtube.com/watch?v=1 00:00:00 00:03:01")
        return
        
    Music().run(BASE_DIR)
    input("Press any key to starting ordering the music...")
    Manager().run()


if __name__ == "__main__":
    main()