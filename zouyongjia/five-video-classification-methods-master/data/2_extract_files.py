"""
After moving all the files using the 1_ file, we run this one to extract
the images from the videos and also create a data file we can use
for training and testing later.
在使用1文件移动所有文件之后，我们运行这个文件从视频中提取图像，并创建一个数据文件，我们可以在以后的训练和测试中使用。
"""
import csv
import glob
import os
import os.path
from subprocess import call

def extract_files():
    """After we have all of our videos split between train and test, and
    all nested within folders representing their classes, we need to
    make a data file that we can reference when training our RNN(s).
    This will let us keep track of image sequences and other parts
    of the training process.

    We'll first need to extract images from each of the videos. We'll
    need to record the following data in the file:

    [train|test], class, filename, nb frames

    在我们把所有的视频分成训练集和测试集两部分之后
    它们都嵌套在代表它们的类的文件夹中，我们需要这样做
    制作一个训练RNN(s)时可以参考的数据文件。
    这将让我们跟踪图像序列和其他部分
    训练过程。
    我们首先需要从每个视频中提取图像。我们会
    需要在文件中记录以下数据:

    [train|test], class, filename, nb frames

    Extracting can be done with ffmpeg:
    `ffmpeg -i video.mpg image-%04d.jpg`
    """
    data_file = []
    # folders = ['train', 'test']
    root = "D:\code\zouyongjia\DEVISIGN_G_EXTRACT"

    folders = glob.glob(os.path.join(root, '*'))

    for folder in folders:
        class_folders = glob.glob(os.path.join(folder, '*'))

        for class_folder in class_folders:
            # class_files = glob.glob(os.path.join(class_folder, '*'))

            # Get the parts of the file.
            video_parts = get_video_parts(class_folder)

            train_or_test, class_name, filename_no_ext, filename, pic_path = video_parts

            # Only extract if we haven't done it yet. Otherwise, just get
            # the info.
            if not check_already_extracted(class_folder, video_parts):
                # Now extract it.
                src = os.path.join(class_folder, "color.avi")
                dest = os.path.join(class_folder, "pic", class_name + '-%04d.jpg')
                call(["ffmpeg", "-i", src, dest])

            # Now get how many frames it is.
            nb_frames = get_nb_frames_for_video(os.path.join(class_folder, "pic"), video_parts)

            data_file.append([train_or_test, class_name, filename_no_ext, nb_frames, pic_path])

            print("Generated %d frames for %s\\video.avi" % (nb_frames, class_folder))

    with open('data_file.csv', 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(data_file)

    print("Extracted and wrote %d video files." % (len(data_file)))

def get_nb_frames_for_video(vid_dep_skele_path, video_parts):
    """Given video parts of an (assumed) already extracted video, return
    the number of frames that were extracted."""
    train_or_test, classname, filename_no_ext, _, _ = video_parts
    generated_files = glob.glob(os.path.join(vid_dep_skele_path, classname + '*.jpg'))
    return len(generated_files)

def get_video_parts(video_path):
    """Given a full path to a video, return its parts.给定一个视频的完整路径，返回它的part。"""
    parts = video_path.split(os.path.sep)
    filename = parts[5]
    name = filename.split('_')[0]    # 视频录取人编号
    class_name = parts[4]            # 类别
    train_or_test = filename.split('_')[2]      # 每个人录取的视频编号

    return train_or_test, class_name, name, filename, os.path.join(video_path, "pic")

def check_already_extracted(path, video_parts):
    """Check to see if we created the -0001 frame of this file."""
    if bool(os.path.exists(os.path.join(path, "pic"))):
        return True
    else:
        os.mkdir(os.path.join(path, "pic"))
        return False

def main():
    """
    Extract images from videos and build a new file that we
    can use as our data input file. It can have format:

    [train|test], class, filename, nb frames
    """
    extract_files()

if __name__ == '__main__':
    main()





