import xml.dom.minidom
import json
import sys
import os

# input xml_file : parameter is first, xml_file1 is second (for test)
xml_file1 = ""
# xml_file1 = "files/hana009.xml"

def parse_xml(xml_file):
    # Parse the XML file
    dom = xml.dom.minidom.parse(xml_file)

    law_name = dom.getElementsByTagName('lawName')[0]
    doc_id, doc_title = get_doc_title_data(law_name)

    # Extract relevant data from the parsed XML
    sub_sections = dom.getElementsByTagName('subSection')

    # Get the base name of the XML file
    base_name = os.path.splitext(xml_file)[0]
    # Create the JSON file name based on the XML file name
    json_file = base_name + '.json'

    return doc_id, doc_title, sub_sections, json_file

def get_doc_title_data(law_name):
    # Extracts the document title and ID from the lawName element
    law_text = law_name.getElementsByTagName('text')[0].firstChild.data
    doc_id = law_text.split(' ')[0]
    doc_title = law_text.strip()

    return doc_id, doc_title

def get_title_data(sub_section):
    # Get the title text and title ID from the sub_section element
    title_text = sub_section.getElementsByTagName('text')[0].firstChild.data
    title_id = title_text.split(' ')[0]

    return {
        'sub_title': title_text,
        'sub_id': title_id,
        'article_datas': []
    }

def get_article_data(article):
    # Get the article ID, code, title, contexts, and table existence from the article element
    #article_id = article.getAttribute('ID')
    article_code = ((article.getElementsByTagName('text')[0].firstChild.data).split(' '))[0]
    article_title_text = article.getElementsByTagName('text')[0].firstChild.data
    #article_title = article_title_text.split(' ')[0]
    article_contexts = []

    for content in article.getElementsByTagName('content'):
        if not content.getElementsByTagName('tbl_group'):
            text_elements = content.getElementsByTagName('text')

            if text_elements and text_elements[0].firstChild is not None:
                context_text = text_elements[0].firstChild.data
            else:
                context_text = ""

            article_contexts.append(context_text.strip())

    table_exist = 'Y' if article.getElementsByTagName('tbl_group') else 'N'

    return {
        'article_id': article_code,
        'article_title': article_title_text,
        'article': ', '.join(article_contexts),
        'tableYN': table_exist
    }

def process_sub_sections(sub_sections):
    # Process the sub-sections and articles to generate the output data
    output_data = []

    for sub_section in sub_sections:
        sub_section_data = get_title_data(sub_section)

        articles = sub_section.getElementsByTagName('article')
        for article in articles:
            article_data = get_article_data(article)
            sub_section_data['article_datas'].append(article_data)

        output_data.append(sub_section_data)

    return output_data

def convert_to_json(doc_id, doc_title, output_data):
    # Converts the processed data to JSON format
    json_data = {
    'doc_id': doc_id,
    'doc_title': doc_title,
    'doc_contents': output_data
    }

    return json.dumps(json_data, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # Check if the XML file name is provided as a command-line argument
    if len(sys.argv) < 2:
        print('Usage: python create_hana_json_1.0.py inputfile.xml')
        #sys.exit(1)
        xml_file = xml_file1 
    else:
        xml_file = sys.argv[1]
    
    if xml_file =="":
        sys.exit(1)

    doc_id, doc_title, sub_sections, json_file = parse_xml(xml_file)
    output_data = process_sub_sections(sub_sections)
    json_data = convert_to_json(doc_id, doc_title, output_data)

    print(json_data)

    print("xml_file : " + xml_file)  
    print("json_file : " + json_file)   
    with open(json_file, "w", encoding="utf-8") as f:
        f.write(json_data)    