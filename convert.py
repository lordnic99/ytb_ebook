import os
from PIL import Image
import sys
import logging
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_mobi_to_txt(file_path, output_path):
    txt_name = os.path.basename(file_path).rsplit(r'.', 1)[0] + ".txt"
    txt_out_path = os.path.join(output_path, txt_name)
    command = f"ebook-convert.exe {file_path} {txt_out_path}"
    completed_process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if completed_process.returncode == 0:
        return
    else:
        output = completed_process.stdout.decode('utf-8')
        print(output)
        logging.error(f"Failed to convert MOBI to TXT: {os.path.basename(file_path)}")
    
def convert_image_to_jpg(file_path, output_path):
    image = Image.open(file_path)
    jpg_name = os.path.basename(file_path).rsplit(r'.', 1)[0] + ".jpg"
    jpg_out_path = os.path.join(output_path, jpg_name)
    image.save(jpg_out_path, "JPEG")
    
def process_files(folder_path, output_path):
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.endswith(".mobi") or filename.endswith(".epub"):
                logging.info(f"Chuyển MOBI sang TXT: {filename}")
                convert_mobi_to_txt(file_path, output_path)

            elif not filename.endswith(".jpg"):
                try:
                    logging.info(f"Chuyển image sang JPG: {filename}")
                    convert_image_to_jpg(file_path, output_path)
                except (IOError, OSError):
                    logging.info(f"Bỏ qua, ko phải file ảnh: {file_path}")
                
if len(sys.argv) > 1:
    folder_path = sys.argv[1].strip()
else:
    folder_path = input("Nhập thư mục cần chuyển: ")

output_path = os.path.join(folder_path, "output")
os.makedirs(output_path, exist_ok=True)
process_files(folder_path, output_path)