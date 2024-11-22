import os
import shutil

def move_small_files(source_dir, size_limit=100000):
    # 在当前工作目录下创建一个名为 .bin 的目标目录
    target_dir = os.path.join(os.getcwd(), '.bin')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created target directory: {target_dir}")

    # 遍历源目录中的所有文件
    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)

        # 确保它是一个文件而不是目录
        if os.path.isfile(source_path):
            # 获取文件大小
            file_size = os.path.getsize(source_path)

            # 如果文件小于设定的大小限制，则移动
            if file_size < size_limit:
                target_path = os.path.join(target_dir, filename)
                shutil.move(source_path, target_path)
                print(f"Moved {filename} to {target_dir}")



def main():
    # 指定源目录，你可以修改这里的路径
    source_directory = 'F:/arts'

    # 调用函数
    move_small_files(source_directory)

if __name__ == "__main__":
    main()