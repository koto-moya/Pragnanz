import os
import shutil
def copy_tree(src_path, dst_path):
    for item in os.listdir(src_path):
        source = src_path+"/"+item
        dest = dst_path+"/"+item
        if os.path.isfile(source):
            shutil.copy(source,dest)
        else:
            os.mkdir(dest)
            copy_tree(source,dest)
if __name__ == "__main__":
    src_path = "/home/koto/build/hyde/static"
    dst_path = "/home/koto/build/hyde/public"
    if os.path.exists(src_path):
        if os.path.exists(dst_path):
            shutil.rmtree(dst_path)
        os.mkdir(dst_path)
        copy_tree(src_path, dst_path)
