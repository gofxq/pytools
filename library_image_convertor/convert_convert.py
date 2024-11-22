import os
from pathlib import Path
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

# 提升图像像素处理的上限
Image.MAX_IMAGE_PIXELS = None  # 移除限制，但要小心处理非常大的图像



def compress_image(file_path, output_path):
    # 打开图像并获取其分辨率
    with Image.open(file_path) as img:
        width, height = img.size
    
        # Adjust the compression by changing the image mode, if applicable
        if img.mode != 'P':  # Convert non-palette images to a palette-based image
            img = img.convert('P', palette=Image.ADAPTIVE)
                
            
        # 调整图像保存参数以压缩文件大小
        quality = 85  # 初始质量设置为85，可以根据需求调整
        while True:
            img.save(output_path, format='PNG', quality=quality)
            if os.path.getsize(output_path) > 10 * 1024 * 1024:  # 文件仍然大于10MB
                quality -= 5  # 降低质量
                if quality < 10:
                    break  # 避免质量过低
            else:
                break


def convert_image_to_png(old_path, new_dir):
    file = os.path.basename(old_path)
    new_path = os.path.join(new_dir, Path(file).stem + '.png')

    # 检查目标文件是否已存在
    if os.path.exists(new_path):
        print(f"File already exists: {new_path}")
        return None  # 如果文件已存在，跳过转换
    
    try:
        compress_image(old_path,new_path)

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
source_directory =   'F:/arts'
target_directory =  'F:/arts_compress'
log_file_path = 'F:/compress.log'

# 调用函数
convert_to_png(source_directory, target_directory)
