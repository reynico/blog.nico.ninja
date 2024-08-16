#!/bin/bash

status_code=0
IMAGE_EXTENSIONS=("jpg" "jpeg" "png" "heic")

has_exif_data() {
    local image_path="$1"
    exiftool "$image_path" | grep -Ev '^(ExifTool Version Number|File Name|Directory|File Size|File Modification Date/Time|File Access Date/Time|File Inode Change Date/Time|File Permissions|File Type|File Type Extension|MIME Type|Image Width|Image Height|Encoding Process|Bits Per Sample|Color Components|Y Cb Cr Sub Sampling|Image Size|Megapixels|Blue|Green|Red|White|Interlace|Filter|Compression|Color|Bit)' &> /dev/null
}

remove_metadata() {
    local image_path="$1"
    exiftool -all= -overwrite_original "$image_path"
}

for file in $(git diff --cached --name-only --diff-filter=ACM); do
    file_extension=$(echo "${file##*.}" | tr '[:upper:]' '[:lower:]')
    
    if [[ "${IMAGE_EXTENSIONS[@]}" =~ $file_extension ]]; then
        if has_exif_data "$file"; then
            echo "Warning: Image '$file' has EXIF data. Removing data..."
            remove_metadata "$file"
            status_code=1
        fi
    fi
done

exit $status_code
