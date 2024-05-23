from md_to_html import markdown_to_html
def extract_title(markdown):
    heading = markdown.split("\n")[0]
    if heading.count("#") == 1:
        return heading.lstrip(r"#").lstrip(" ")
    else:
        raise Exception("No valid heading")

def read(filepath):
    with open(filepath) as file:
        return file.read()

def edit_template(tmplt_path, title, content):
    with open(tmplt_path) as file:
        html = file.read()
        html = html.replace("{{ Title }}", f"{title}") 
        html = html.replace("{{ Content }}", f"{content}")
    return html

def generate_page(src_path, tmplt_path, dst_path):
    print(f"Generating page from {src_path} to {dst_path} using {tmplt_path}")
    markdown = read(src_path)
    template = read(tmplt_path)
    content = markdown_to_html(markdown)
    title = extract_title(markdown)
    html = edit_template(tmplt_path, title, content)
    with open(dst_path+"/" +"index.html", "w") as file:
        file.write(html)

if __name__ == "__main__":
    src_path = "/home/koto/build/hyde/content/index.md"
    dst_path = "/home/koto/build/hyde/static"
    tmplt_path = "/home/koto/build/hyde/template.html"
    generate_page(src_path, tmplt_path, dst_path)

