from pathlib import Path
from datetime import datetime

from PIL import Image
from pillow_heif import register_heif_opener

#supported file types
PHOTO_TYPES = {
    ".jpg", ".jpeg",   
    ".heic", ".heif",  
    ".png",            
    ".webp",           
    ".gif",
    ".bmp", ".tif", ".tiff",
    ".dng",            
}

VIDEO_TYPES = {
    ".mp4",            
    ".mov",            
    ".m4v",            
    ".3gp",            
    ".avi", ".wmv", ".mkv",  
}

MEDIA_TYPES = PHOTO_TYPES | VIDEO_TYPES

def get_date(f):
    try: # try to get original date from photos EXIF data 
        img = Image.open(f)
        taken = img.getexif().get_ifd(0x8769).get(36867) #0x8769 is section of exif holding cam info 36867 is where date taken is stored

        if taken:
            return(datetime.strptime(taken,"%Y-%m-%d_%I-%M %p")) # exif dates alway in this format 2026:07:04 18:22:10
    except Exception:
        pass
    #Otherwise use the older date between modified time and birthtime
    info = f.stat()
    return datetime.fromtimestamp(min(info.st_mtime,info.st_birthtime))

def main():
    folder = Path(input("Folder path: ").strip('"'))

    for f in folder.iterdir():
        if not f.is_file() or f.suffix.lower() not in MEDIA_TYPES:
            continue
        
        
        
        file_made_date= get_date(f)
        new_file_name = file_made_date.strftime("%Y-%m-%d--[%I-%M%p]")
        new_file_path = f.with_name(new_file_name + f.suffix) # store the new path with original file suffix
        
        # if for some reason two or more files have same exact date add a number to end 
        count = 1
        while new_file_path.exists():
            new_file_path = f.with_name(f"{new_file_name}_{count}{f.suffix}")
            count += 1


        print(f"Renaming {f.name} to {new_file_name}")
        f.rename(new_file_path)
        

if __name__=="__main__":
    main()
