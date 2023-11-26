# 读取文件夹所有apk文件并打印其文件名

import os
import glob

folder_path = 'D:\\MC_00\\webdownload'

# 使用 glob 模块匹配文件夹中的所有 APK 文件
apk_files = glob.glob(os.path.join(folder_path, '*.apk'))

# 打印每个 APK 文件的文件名
for apk_file in apk_files:
    file_name = os.path.basename(apk_file).split('.apk')[0]
    print(file_name)