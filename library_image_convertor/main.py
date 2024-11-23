import os
from pathlib import Path



# 定义图片文件的后缀名集合
image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg',
                    '.tif', '.psb', '.psd', '.eps'}



# 定义一个函数来统计后缀名
def count_file_extensions(directory):
    # 定义一个字典来存储后缀名和相应的计数
    extension_count = {}

    # 遍历目录下的所有文件和子目录中的文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 获取文件的后缀名
            extension = Path(file).suffix.lower

            # 统计后缀名的数量
            if extension in extension_count:
                extension_count[extension] += 1
            else:
                extension_count[extension] = 1

    return extension_count 

# 指定要检查的目录路径
directory_path = 'E:/library_arts'

# 获取后缀名统计结果
extensions = count_file_extensions(directory_path)

# 过滤出非图片文件的后缀
non_image_extensions = {ext: count for ext, count in extensions.items() if ext not in image_extensions}

# 打印结果
print("Non-image file extensions and their counts:")


import os
from pathlib import Path

# 遍历目录下的所有文件和子目录中的文件
for root, dirs, files in os.walk(directory_path):
    for file in files:
        # 获取文件的完整路径
        full_path = os.path.join(root, file)
        # 获取文件的后缀名
        extension = Path(file).suffix

        # 检查后缀名是否在图片后缀集合中
        if extension.lower() not in image_extensions:
            print(full_path)
