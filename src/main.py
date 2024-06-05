from md_to_html import markdown_to_html
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

def extract_title(markdown):
    heading = markdown.split("\n")[0]
    if heading.count("#") == 1:
        return heading.lstrip(r"#").lstrip(" ")
    else:
        raise Exception("No valid heading")

def read(filepath):
    with open(filepath) as file:
        return file.read()

def edit_template(template, title, content):
    html = template.replace("{{ Title }}", f"{title}") 
    html = html.replace("{{ Content }}", f"{content}")
    return html

def generate_page(src_path, template, dst_path):
    print(f"Generating page from {src_path} to {dst_path} using {template}")
    markdown = read(src_path)
    template = read(template)
    content = markdown_to_html(markdown)
    title = extract_title(markdown)
    html = edit_template(template, title, content)
    with open(dst_path, "w") as file:
        file.write(html)

def generate_pages(content_path, template, dest_path):
    for item in os.listdir(content_path):
        source = content_path+"/"+item
        if os.path.isfile(source):
            print(source)
            dest = dest_path+ "/" + item.replace(".md", ".html")
            generate_page(source, template, dest)
        else:
            dest = dest_path+"/"+item
            os.mkdir(dest)
            generate_pages(source, template, dest)

if __name__ == "__main__":
    base = os.getcwd().replace("/src","")
    content = f"{base}/content"
    public = f"{base}/public"
    css = f"{base}/assets/css"
    images = f"{base}/assets/images"
    template = f"{base}/assets/template.html"
    if os.path.exists(public):
        shutil.rmtree(public)
        os.mkdir(public)
    # add images
    copy_tree(images, public)
    # add css
    copy_tree(css, public)
    generate_pages(content, template, public)


