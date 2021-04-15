import zipfile
import os

# 含有压缩包的目录
root = 'D:\\code\\zouyongjia\\DEVISIGN_G'
# 解压缩位置
root_extract = 'D:\\code\\zouyongjia\\DEVISIGN_G_EXTRACT'
for path_people in sorted(os.listdir(os.path.join(root))):
    if not os.path.isdir(os.path.join(root, path_people)):
        continue
    for path_zip in os.listdir(os.path.join(root, path_people)):
        if zipfile.is_zipfile(os.path.join(root, path_people,path_zip)):                   # 是否是压缩包
            class_id = path_zip[:-8].split('_')[1]                                                        # 类别编号
            path1 = os.path.join(root_extract,class_id)                                            # 根据手语类别解压缩文件
            z = zipfile.ZipFile(os.path.join(root, path_people,path_zip),'r')
            z.extract(z.namelist()[0] + 'color.avi', path=path1, pwd=None)            # 提取压缩包中的文件
            z.extract(z.namelist()[0] + 'skeleton.dat', path=path1, pwd=None)
            z.extract(z.namelist()[0] + 'log.txt', path=path1, pwd=None)
            z.close()
