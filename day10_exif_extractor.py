import sys
from typing import Dict, Any

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
except ImportError:
    print("Error: Pillow library is required. Run 'pip install Pillow'.")
    sys.exit(1)

class ExifExtractor:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def extract(self) -> Dict[str, Any]:
        metadata = {}
        try:
            with Image.open(self.filepath) as img:
                if not hasattr(img, '_getexif'):
                    return metadata
                    
                exif_data = img._getexif()
                if not exif_data:
                    return metadata

                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    
                    if tag_name == "GPSInfo" and isinstance(value, dict):
                        gps_data = {}
                        for gps_tag_id in value:
                            gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            gps_data[gps_tag_name] = value[gps_tag_id]
                        metadata[tag_name] = gps_data
                    else:
                        metadata[tag_name] = value
        except IOError:
            pass
            
        return metadata

if __name__ == "__main__":
    target_file = ""
    
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        try:
            target_file = input("Enter image filepath: ").strip()
        except KeyboardInterrupt:
            sys.exit(1)
            
    if not target_file:
        sys.exit(1)

    extractor = ExifExtractor(target_file)
    results = extractor.extract()
    
    if not results:
        print("No EXIF metadata found or unsupported file format.")
        sys.exit(0)
        
    for key, val in results.items():
        if isinstance(val, dict):
            print(f"{key}:")
            for sub_key, sub_val in val.items():
                print(f"  {sub_key}: {sub_val}")
        else:
            print(f"{key}: {val}")
