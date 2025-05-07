from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
from markdown_html import *
import re
import shutil
import os
import sys

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
basepath = "/"

def main(argv):
    global basepath

    if len(argv) > 1:
        basepath = argv[1]
    
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_static_content(dir_path_static, dir_path_public)

    generate_page_recursive(dir_path_content, template_path)


    #textnode = TextNode("Testi",TextType.BOLD)

    #print(textnode)


def copy_static_content(sourcedir, destinationdir):

    if not os.path.exists(destinationdir):
        os.mkdir(destinationdir)

    objects = os.listdir(sourcedir)
    for object in objects:
        if os.path.isfile(os.path.join(sourcedir, object)):
            print(f"Copying {os.path.join(sourcedir, object)} to {shutil.copy(os.path.join(sourcedir, object), os.path.join(destinationdir, object))}")
        elif os.path.isdir(os.path.join(sourcedir, object)):
            copy_static_content(os.path.join(sourcedir, object),os.path.join(destinationdir, object))



def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        markdown = file.read()
        file.close()

    with open(template_path, 'r') as file:
        template = file.read()
        file.close()

    node = markdown_to_html_node(markdown)
    html = node.to_html()

    title = extract_title(markdown)

    full_html = template.replace(r"{{ Title }}", title)
    full_html = full_html.replace(r"{{ Content }}", html)

    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')


    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as f:
        f.write(full_html)


def generate_page_recursive(source, template_path):
    global basepath
    objects = os.listdir(source)
    for object in objects:
        #print(os.path.join(source, object))
        if is_markdown(os.path.join(source, object)):
            from_path = os.path.join(source, object)
            dest_path = from_path.replace("content", "docs")
            dest_path = dest_path.replace("md", "html")
            generate_page(from_path, template_path, dest_path, basepath)
        elif os.path.isdir(os.path.join(source, object)):
            #print("start recursion")
            generate_page_recursive(os.path.join(source, object), template_path)


def is_markdown(file):
    #print("is_markdown?: " + file)
    #print(file[-3:])
    if os.path.isfile(file) and file[-3:] == ".md":
        #print(f"{file} is markdown!")
        return True
    return False








main(sys.argv)