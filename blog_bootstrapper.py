import json
import datetime

##########################################################
#
## Generate Json Config File
#
def get_sub_list():
    #Function to get sub-list items for points
    num_sub_lists = int(input("\nEnter the number of sub-list items (0 if none): "))
    sub_list = []
    for i in range(num_sub_lists):
        sub_item = input(f"\nEnter sub-list item {i + 1}: ")
        sub_list.append(sub_item)
    return sub_list

def get_content():
    #Function to get content details from the user.
    num_content = int(input("number of content items for this section: "))
    content_list = []
    
    for i in range(num_content):
        print(f"\nContent Item {i + 1}:")
        
        # Get content type
        content_type = input("Enter content type (points or paragraph): ").strip().lower()
        if content_type not in ["points", "paragraph"]:
            print("Invalid content type. Defaulting to 'paragraph'.")
            content_type = "paragraph"
        
        # Get content text
        content_text = input("text for this content item: ")
        
        # Check if the content has nested points
        has_points = input("Does this content have nested points? (yes or no): ").strip().lower()
        
        if has_points == "yes":
            num_points = int(input("number of points: "))
            points_list = []
            for j in range(num_points):
                point_text = input(f"Enter point {j + 1}: ")
                sub_list = get_sub_list()
                points_list.append({
                    "list": point_text,
                    "sub_list": sub_list
                })
            content_list.append({
                "type": content_type,
                "para": content_text,
                "para_content": points_list
            })
        else:
            content_list.append({
                "type": content_type,
                "para": content_text,
                "para_content": []
            })
        
    return content_list

def get_section():
    #Function to get section details from the user.
    sec_title = input("section title: ")
    
    # Check if the section has an image
    image = input("Does this section have an image? (yes or no): ").strip().lower()
    sec_img = []
    if image == "yes":
        image_url = input("image CDN link: ")
        sec_img.append(image_url)
    
    # Get content for the section
    sec_content = get_content()
    
    return {
        "sec_title": sec_title,
        "sec_img": sec_img,
        "sec_content": sec_content
    }

def generate_section(num_highlights):
    num_sections = num_highlights
    sections = []
    
    for i in range(num_sections):
        print(f"\nSection {i + 1}:")
        section = get_section()
        sections.append(section)
    
    # Save the sections to a JSON file
    # with open("form_data.json", "w") as f:
    #     json.dump({"sections": sections}, f, indent=4)
    return  sections


##########################################################
#
## Generate HTML File using JSON file
#
def generate_hightlight(blogs_map):
    generate_hightlight_str = ''
    highlight_list = [highlights_anchor.replace("[[HIGHLIGHT_SECTION]]","section"+str(idx+1)).replace("[[HIGHLIGHT_NAME]]",highlights) for idx,highlights in enumerate(blogs_map)]
    ordered_highlight_list = "<ol>" + "".join(highlight_list)+"</ol>"
    generate_hightlight_str =  generate_hightlight_str + highlights_header + ordered_highlight_list
    generate_hightlight_str = div_highlight_container.replace("[[KEY_HIGHLIGHT]]",generate_hightlight_str)
    return generate_hightlight_str


def generate_sections(blogs_map):
    generate_section_str = []
    index = 0

    for sections in blogs_map:

        index += 1
        sect_header = section_header.replace("[[SECTION_NAME]]",sections["sec_title"]).replace("[[SECTION_NO]]",str(index))
        sect_img = "".join([section_img.replace("[[SECTION_IMAGE]]",img_url) for img_url in sections.get("sec_img") ]) if sections.get("sec_img") else "" 
        
        final = ''

        for sect_details in sections["sec_content"]:
            para_str ,point_para_str,inner_list ,para_content_str, outer_lst='','','' , '', ''

            if sect_details["type"] == "paragraph":
                para_str =  "<p>"+sect_details["para"]+ "</p>"
                if sect_details.get("para_content"):
                    for points_list in  sect_details.get("para_content"):
                        if points_list.get("list") :
                            outer_lst  = "<li>"+points_list.get("list")+"</li>"
                        if points_list.get("sub_list") :
                            inner_list = "<ul><li>" + "</li><li>".join(points_list.get("sub_list"))+ "</li></ul>"
                        para_content_str =para_content_str + section_point_list_tag.replace("[[UL_TAG_PARA]]",outer_lst + inner_list)
                para_str = para_str + para_content_str

            if sect_details["type"] == "points" :
                point_para_str = '<li>' +sect_details["para"] +'</li>'
                if sect_details.get("para_content"):
                    for points_list in  sect_details.get("para_content"):
                        if points_list.get("list") :
                            outer_lst  = "<li>"+points_list.get("list")+"</li>"
                        if points_list.get("sub_list") :
                            inner_list = "<ul><li>" + "</li><li>".join(points_list.get("sub_list"))+ "</li></ul>"
                        para_content_str =para_content_str + '<ul>'+outer_lst + inner_list+'</ul>'
                point_para_str = section_point_para_str.replace("[[COMBINE_NAME]]",point_para_str + para_content_str)
            
                  
            final = final + para_str + point_para_str 
        generate_str =  sect_header + sect_img + final
        generate_section_str.append(generate_str)
        
    return generate_section_str


##########################################################
#
## STATIC VARIABLES
#
default_css = '''
<style>
    <!--
    .blog-img {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-top:20px;
        margin-bottom:20px;

    }

    .blog-img span {
        text-align: center;
    }

    html {
        scroll-behavior: smooth;
    }

    ol li {
        list-style: none;
        position: relative;
    }

    ol li::before {
        content: '';
        left: -13px;
        top: 13px;
        position: absolute;
        height: 5px;
        width: 5px;
        border-radius: 50%;
        background-color: #9F4A17;
    }

    .blog-content ol li::before {
        top: 19px;
    }

    .highlight-container {
        border: 1px solid #9F4A17;
        padding: 10px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .highlight-container h1 {
        margin: 10px 0px;
    }

    p {
        text-align: justify;
    }

    ul li {
        list-style: none;
        text-align: justify;
    }

    ul li .list-content {
        padding-left: 15px;
        text-align: justify;
    }

    .numerical-list {
        list-style: auto !important;
    }

    h3 {
        font-size: 25px !important;
    }

    .product-list li::before {
        top: 41px;
    }
    -->
</style>
'''

### DIV class variable 
# static variable
div_blog_container = '''<div class="blog-container">[[INNER_ELEMENT]]</div>'''
div_highlight_container  = '''<div class="highlight-container">[[KEY_HIGHLIGHT]]</div>'''
div_blog_img = '''<div class="blog-img">'''
div_point = '''<div class="point">'''
# dynamic variable
div_section_id =  '''<div class="s[[SECTION_ID]]">'''


### HIGHLIGHT
highlights_header = '''<h1><b>Highlights</b></h1>'''
highlights_anchor= '''<li><a href="#[[HIGHLIGHT_SECTION]]">[[HIGHLIGHT_NAME]]</a></li>'''

### SECTIONS
section_div_class = '''<div class="s[[SECTION_ID]]">[[SECTION_DETAIL]]</div>'''
section_header = '''<h2 style="margin-top: 25px; margin-bottom: 10px" id="section[[SECTION_NO]]"><b>[[SECTION_NAME]]</b></h2>'''
section_points_para = '''<div class="point"><ul>[[SECTION_POINT_PARA]]</ul></div>'''
section_img = '''<div class="blog-img"><img src="[[SECTION_IMAGE]]"/></div>'''
## Point List Section
section_point_para_str = '<ul style="list-style-type: disc">[[COMBINE_NAME]]</ul>'
section_point_list_tag = '''<ul style="list-style-type: disc">[[UL_TAG_PARA]]</ul>'''

##########################################################
#
## Final Run
#
def main():
    # ENTER METADATA ABOUT THE BLOG  
    blog_id = int(input("Blog ID: "))
    blog_created_at = input("Blog Created Date (YYYY-MM-DD): ") 
    blog_updated_at = input("Blog Updated Date (YYYY-MM-DD): ") 
    blog_status = input("Blog Status (approved or disapproved): ")
    blog_title = input("Blog Title: ")
    meta_title = input("Meta Title: ")
    meta_description = input("Meta Description: ")

    #dictionary
    form_data = {
        "blog_id": blog_id,
        "blog_created_at": blog_created_at, 
        "blog_updated_at": blog_updated_at,
        "blog_status": blog_status,
        "blog_title": blog_title,
        "meta_title": meta_title,
        "meta_description": meta_description
    }

    #saving dict in json
    with open("form_data.json", "w") as f:
        json.dump(form_data, f)


    #loading data and checking if there is no json
    try:
        with open("form_data.json", "r") as f:
            form_data = json.load(f)
    except FileNotFoundError:
        form_data = {}

    #entering number of key highlights
    num_highlights = int(input("\nnumber of section key highlights: "))

    #collecting inputs
    highlights = []
    for i in range(num_highlights):
        highlight = input(f"\nEnter section highlight {i + 1}: ")
        highlights.append(highlight)

    form_data["key_highlights"] = highlights

    # Run the main function
    form_data["sections"] = generate_section(num_highlights)

    #saving dict in json 
    with open("form_data.json", "w") as f:
        json.dump(form_data, f, indent=4)
    
    with open("form_data.json", "r") as f:
        form_data = json.load(f)

    json_data = json.dumps(form_data, indent=4)


    print("\nDictionary saved successfully\n")
    #output
    print("Output JSON:")
    print(json_data)


    json_file = 'form_data.json'

    with open(json_file, 'r') as file:
        blogs_map = json.load(file)
    # blogs_map  = json.loads(json_file)

    # Generate file
    if blogs_map["blog_status"] == "approved":
        html_file_name = blogs_map["blog_title"].replace(" ","_")+".html"
        html_file = open(html_file_name, "w")
        html_file.write(default_css)

        # final editing

        # Generate Key Highlights
        hightlight_str = generate_hightlight(blogs_map["key_highlights"])
        # Generate Sections
        sections_str = "".join(generate_sections(blogs_map["sections"]))
        
        merge_all_elmt=  hightlight_str + sections_str
        
        final_html= div_blog_container.replace("[[INNER_ELEMENT]]",merge_all_elmt)
        
        print("EXPORTED :" + html_file_name )
        html_file.write(final_html)

        # print(json.dumps(blogs_map,indent=2))

# print(read_mongo())

if __name__ == "__main__":
    main()