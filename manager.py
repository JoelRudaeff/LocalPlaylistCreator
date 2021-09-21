# Python 3
import os

# OUTPUT_BASE_DIR = "D:\\CAR_SOUNDTRACK"
OUTPUT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(OUTPUT_BASE_DIR, "tmp")
TRASH_DIR = os.path.join(OUTPUT_BASE_DIR, "trash")
PYCACHE_DIR = os.path.join(OUTPUT_BASE_DIR, "__pycache__")

# "" means everyting, string otherwise
#INSERT_INTO_FLAG = ""
INSERT_INTO_FLAG = "playlist"

# To which folder we don't want to insert the new files
BLACKLIST = ["Running"]

# Output format of the new files
MEDIA_FILE_FORMAT = "mp3"


class Manager(object):
    def get_all_output_folders(self):
        output_list = [x[0] for x in os.walk(OUTPUT_BASE_DIR)]
        
        if INPUT_DIR in output_list:
            output_list.remove(INPUT_DIR)

        if TRASH_DIR in output_list:
            output_list.remove(TRASH_DIR)
        
        if PYCACHE_DIR  in output_list:
            output_list.remove(PYCACHE_DIR)

        output_list.remove(OUTPUT_BASE_DIR)
        
        for playlist in BLACKLIST:
            try:
                output_list.remove(OUTPUT_BASE_DIR + "\\" + playlist)
            except ValueError as e1:
                # Folder name which was on the BLACKLIST doesn't exists
                pass
        
        if INSERT_INTO_FLAG == "":
            print("Returning all available output dirs")
            return output_list
        
        else:
            if INSERT_INTO_FLAG not in output_list and not os.path.isdir(INSERT_INTO_FLAG):
                os.mkdir(INSERT_INTO_FLAG)
            return [INSERT_INTO_FLAG]

    def filter_destination_file_name(self, file_name):
        new_file_name = file_name
        new_file_name = new_file_name.replace("(", "").replace(")","").replace("[", "").replace("]", "").replace("Official","").replace("official","").replace("ft.","").replace("videoclip","").replace("Video","").replace("Clip","").replace("lyrics", "").replace("Lyrics", "").replace("HD","").replace("hd","").replace("HQ","").replace("hq","").replace("Copyright Free","")
        new_file_name =  new_file_name.replace("  "," ").replace(" {}".format(MEDIA_FILE_FORMAT),".{}".format(MEDIA_FILE_FORMAT))
        return new_file_name
                
    def run(self):
        # Files are present
        temp_files = os.listdir(INPUT_DIR)
        current_temp_file_path = ""
        destination_copy_file_path = ""
        output_folders = self.get_all_output_folders()
        
        if not temp_files:
            print("No files to copy!")
            return
        
        for current_temp_file in temp_files:
            new_temp_file_name = self.filter_destination_file_name(current_temp_file)
            current_temp_file_path = os.path.join(INPUT_DIR, current_temp_file)
            for current_output_folder in output_folders:
                destination_copy_file_path = os.path.join(current_output_folder, new_temp_file_name)
                
                # File exists already for some reasons
                if os.path.isfile(destination_copy_file_path):
                    print(current_temp_file, " already exists on: ", current_output_folder)
                    continue
                
                with open(current_temp_file_path,"rb") as f:
                    data = f.readlines()
                
                with open(destination_copy_file_path, "wb") as f:
                    f.writelines(data)
                
                print(new_temp_file_name, " was copied to: ", current_output_folder)
            
            try:
                os.rename(current_temp_file_path, os.path.join(TRASH_DIR, current_temp_file))
            except FileExistsError as e:
                print(new_temp_file_name, " already exists on trash bin!")
                os.remove(current_temp_file_path)
                
            print(new_temp_file_name, "Was removed from queue!")


if __name__ == "__main__":
    Manager().run()
