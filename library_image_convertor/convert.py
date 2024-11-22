import os
from pathlib import Path
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# 提升图像像素处理的上限
Image.MAX_IMAGE_PIXELS = None  # 移除限制，但要小心处理非常大的图像


def convert_image_to_png(old_path, new_dir):
    file = os.path.basename(old_path)
    new_path = os.path.join(new_dir, Path(file).stem + '.png')
    # 检查目标文件是否已存在
    if os.path.exists(new_path):
        print(f"File already exists: {new_path}")
        return None  # 如果文件已存在，跳过转换
    
    try:
        with Image.open(old_path) as img:
            img.convert('RGBA').save(new_path, 'PNG')
            print(f"Converted and saved: {new_path}")
        return None  # 完成转换

    except Exception as e:
        print(f"Failed to convert {old_path}: {e}")
        return old_path  # 返回失败的文件路径以供记录

def convert_to_png(source_dir, target_dir):
    # 定义图片文件的后缀名集合
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.tif', '.TIF', '.psb', '.psd', '.PSD'}
    failed_files_path = os.path.join(target_dir, 'failed.txt')  # 定义记录失败文件的路径

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = []

        # 遍历源目录下的所有文件和子目录中的文件
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                old_path = os.path.join(root, file)
                extension = Path(file).suffix

                # 检查文件后缀是否在指定的图片后缀集合中
                if extension in image_extensions:
                    # 创建与源目录结构相同的目标目录结构
                    relative_path = os.path.relpath(root, source_dir)
                    new_dir = os.path.join(target_dir, relative_path)
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)

                    # 为每个文件创建一个转换任务
                    futures.append(executor.submit(convert_image_to_png, old_path, new_dir))

        # 处理转换结果和失败情况
        failed_files = [future.result() for future in futures if future.result() is not None]
        if failed_files:
            with open('failed_files.txt', 'w', encoding='utf-8') as f:
                f.writelines(f"{file}\n" for file in failed_files)



# 指定源目录和目标目录
source_directory =  'E:/字画'
target_directory =  'F:/arts'
log_file_path = 'E:/convert.log'

# 调用函数
convert_to_png(source_directory, target_directory)
