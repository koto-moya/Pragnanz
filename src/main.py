import os
import shutil
from md_to_html import markdown_to_html
def copy_tree(src_path, dst_path):
    for item in os.listdir(src_path):
        source = src_path+"/"+item
        dest = dst_path+"/"+item
        if os.path.isfile(source):
            shutil.copy(source,dest)
        else:
            os.mkdir(dest)
            copy_tree(source,dest)

def extract_title(markdown):
    heading = markdown.split("\n")[0]
    if heading.count("#") == 1:
        return heading.lstrip(r"#").lstrip(" ")
    else:
        raise Exception("No valid heading")

def read(filepath):
    with open(filepath) as file:
        return file.read()

def edit_template(tmplt_path, **kwargs):
    with open(htmlpath) as file:
        html = file.read()
        html.replace("{{ Title }}", f"{title}") 
        html.replace("{{ Content }}", f"{content}")

def generate_page(src_path, tmplt_path, dst_path):
    print(f"Generating page from {src_path} to {dst_path} using {tmplt_path}")
    markdown = read(src_path)
    template = read(tmplt_path)
    content = markdown_to_html(markdown)
    title = extract_title(markdown)
    edit_template(tmplt_path, title=title, content=content)

if __name__ == "__main__":
    #src_path = "/home/koto/build/hyde/static"
    #dst_path = "/home/koto/build/hyde/public"
    #if os.path.exists(src_path):
    #    if os.path.exists(dst_path):
    #        shutil.rmtree(dst_path)
    #    os.mkdir(dst_path)
    #   copy_tree(src_path, dst_path)
    src_path = "/home/koto/build/hyde/content/index.md"
    dst_path = "/home/koto/build/hyde/public"
    tmplt_path = "/home/koto/build/hyde/template.html"
    generate_page(src_path, tmplt_path, dst_path)
