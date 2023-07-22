import xml.dom.minidom
import json
import sys
import os
import argparse
from pprint import pprint
from xml.dom import minidom

class CreateJson:
    def parse_xml(self,xml_file):
        # Parse the XML file
        dom = xml.dom.minidom.parse(xml_file)
        
        law_name = dom.getElementsByTagName('lawName')[0]
        doc_id, doc_title = self.get_doc_title_data(law_name)

        # Extract relevant data from the parsed XML
        sub_sections = dom.getElementsByTagName('subSection')

        # Get the base name of the XML file
        base_name = os.path.splitext(xml_file)[0]
        # Create the JSON file name based on the XML file name
        json_file = base_name + '.json'

        return doc_id, doc_title, sub_sections, json_file

    def get_doc_title_data(self,law_name):
        # Extracts the document title and ID from the lawName element
        law_text = law_name.getElementsByTagName('text')[0].firstChild.data
        doc_id = law_text.split(' ')[0]
        doc_title = law_text.strip()

        return doc_id, doc_title

    def get_title_data(self,sub_section):
        # Get the title text and title ID from the sub_section element
        title_text = sub_section.getElementsByTagName('text')[0].firstChild.data
        title_id = title_text.split(' ')[0]

        return {
            'sub_title': title_text,
            'sub_id': title_id,
            'article_datas': []
        }


    def get_contexts_data_(self,article):
        article_contexts = []
        i = 0
        for content in article.getElementsByTagName('content'):
            i = i + 1
            # print ("content count get_contexts_data : " + str(i))
            text_elements = content.getElementsByTagName('text')

            context_text = ""
            for text_element in text_elements:
                if text_element.firstChild is not None:
                    context_text += text_element.firstChild.data

            article_contexts.append(context_text.strip())

        return ', '.join(article_contexts)

    def get_contexts_data(self,article):
        article_contexts = []
        i = 0
        for content in article.getElementsByTagName('content'):
            i = i + 1
            # print ("content count  " + str(i))
            # is_child = False
            # if content.parentNode == article:
            #     is_child = True
            #     print ( "is_child = True : is_parent = " + str(is_parent(article,content)))
            # else:
            #     print ( "is_child = False : is_parent = " + str(is_parent(article,content)))
            #     continue # article 의 child content 가 아니면 다음으로 진행
            text_elements = content.getElementsByTagName('text')

            context_text = ""
            if not content.getElementsByTagName('tbl_group'):  # tbl_group 을 포함하고 있지 않으면 text 로 만든다.
                for text_element in text_elements:
                    if text_element.firstChild is not None:   
                        context_text += text_element.firstChild.data


            article_contexts.append(context_text.strip()) 
            # else: # tbl_group 을 포함하고 있는 content는 xml로 붙인다.
            #     for tbl_group in content.getElementsByTagName('tbl_group'):
            #         tableStr = tbl_group.toxml().replace('\n', '').replace('\t', '').strip()
            #         print ("tbl_group = " + tableStr)
            #         article_contexts.append(tableStr)
        
        return  ', '.join(article_contexts)


    def process_sub_sections_str(self,sub_sections,split_number, overlap_number):
        # Process the sub-sections and articles to generate the output data
        output_data = []
        #split_number = 8000
        #overlap_number = 100
        article_contexts = []

        for sub_section in sub_sections:
            sub_section_data = self.get_title_data(sub_section)

            articles = sub_section.getElementsByTagName('article')
            for article in articles:
                # article_contexts = get_contexts_data(article)
                article_contexts_str = self.get_contexts_data(article) 
                # article_data = self.get_article_data_range_str(article_contexts_str, article,0,0,1)

                
                #print("article_contexts : " +  article_contexts_str)
                #print("article_contexts : " +  str(article_contexts))

                if len(article_contexts_str) > split_number: #if len(article.toxml()) > split_number:
                    # Split the article into multiple articles
                    articles_list = []
                    start_index = 0
                    end_index = 0
                    i = 0
                    while end_index !=  len(article_contexts_str):  #start_index   < len(article.toxml()):   
                        i = i + 1                 
                        end_index = min(start_index + split_number, len(article_contexts_str))
                        
                        #articles_list.append(article.toxml()[start_index:end_index])
                        articles_list.append({"order_seq": i ,"start_index": start_index, "end_index": end_index})
                        #print("order === :   i " + str(i) + " : " + str(start_index) + " : " + str(end_index))
                        start_index = end_index - overlap_number # - duplicated_num
                        

                    # Recursively call get_article_data for each split article
                    for range_item  in articles_list:
                        article_data = self.get_article_data_range_str(article_contexts_str,article,range_item["start_index"], range_item["end_index"],range_item["order_seq"])
                        sub_section_data['article_datas'].append(article_data)
                else:
                    #검증 print("get_article_data_range_str 1 >>>> " )
                    article_data = self.get_article_data_range_str(article_contexts_str, article,0,0,1)
                    sub_section_data['article_datas'].append(article_data)
            #print("sub_section_data ----------------------")
            #pprint(sub_section_data)
            output_data.append(sub_section_data)

        return output_data


    def get_article_data_range_str(self,article_str,article,start_index ,end_index, order_seq):
        #article_xml = article.toxml()
        #xml_length = len(str(article))

        # Split the article into separate paragraphs with a maximum length of 1000 characters

        if end_index != 0:
            paragraph = article_str[start_index:end_index]
        else:
            paragraph = article_str

        return self.get_article_data_paragraph_str(article_str, article ,paragraph,order_seq)

    def is_parent(self, parent, child):
    
        #print ( "parent = " + str(parent[0].tagname) + " : child = "+ child[0].tagname )
        if parent == child:
            return True
        else:
            return self.is_parent(parent, child.parentNode) if child.parentNode else False

    def is_tableChild(self, child):
        #print ( "parent = " + str(parent[0].tagname) + " : child = "+ child[0].tagname )
        if child.nodeName == "tbl_group":
            return True
        else:
            return self.is_tableChild(child.parentNode) if child.parentNode else False


    def get_article_data_paragraph_str(self, article_str,article, paragraph,order_seq):

        #article_xml = article_xml.replace("\t", "")
        #article_xml = article_xml.replace("\n", "")
        article_code = ((article.getElementsByTagName('text')[0].firstChild.data).split(' '))[0]
        article_title_text = article.getElementsByTagName('text')[0].firstChild.data
        #article_title = article_title_text.split(' ')[0]
        article_contexts = []
    # xml_length = len(str(paragraph))


    # Remove 'style' attribute from all elements in the article
        elements = article.getElementsByTagName('*')
        for element in elements:
            if element.hasAttribute('style'):
                element.removeAttributeNode(element.getAttributeNode('style'))


        #article_xml = article.toxml()
        article_xml = article.toxml()
        article_xml = article_xml.replace('\n', '').replace('\t', '')
        article_xml_str = ""
        
        doc = xml.dom.minidom.Document()
        text_elements = article.getElementsByTagName('text')   
        for text_element in text_elements: 
           if text_element.firstChild is not None:
                if text_element.childNodes[0].nodeType == 4:
                #    print("test")

                    new_element = doc.createElement("text")
                    new_element_content = doc.createTextNode(text_element.firstChild.nodeValue)
                    new_element.appendChild(new_element_content)
                    text_element.parentNode.replaceChild(new_element, text_element)


        #print("article_xml ===============: " + str(article_xml))

    # article_xml_Str = str (article_xml)
        #article_xml_Str= article_xml_Str.replace('\\?', '?')
        table_exist = 'Y' if article.getElementsByTagName('tbl_group') else 'N'
        #table_exist = 'Y : '+ str(xml_length) if article.getElementsByTagName('tbl_group') else 'N'

        if table_exist:
            article_xml_str =  self.get_article_data_xml(article)

        return {
            'article_id': article_code,
            'article_title': article_title_text,
            'article_seq': order_seq,
            'article': article_xml_str ,
            'article_text': paragraph , # #'article': ', '.join(article_contexts),
            'article_original': str(article_xml) ,
            'tableYN': table_exist
        }

    def get_article_data_xml(self, article):
        article_xml_contexts = []

        i = 0
        for content in article.getElementsByTagName('content'):
            i = i + 1
            #print ("content count  " + str(i))
            is_articleFirstChild = False
            #if content.parentNode == article: # article 의 first child content 인지 확인 -> 아래로 대체
            is_tableChild = self.is_tableChild(content)
            if  is_tableChild == False:  # content 가 tbl_group의 child 가 아닐때
                is_articleFirstChild = True
                #print ( "is_articleFirstChild = True : is_parent = " + str(is_parent(article,content)))
                #print ( "is_articleFirstChild = True : is_tableChild = " + str(is_tableChild(content)) + " : article_id : " + article.getAttribute('ID'))
                
            else:
                #print ( "is_articleFirstChild = False : is_parent = " + str(is_parent(article,content)))
                #print ( "is_articleFirstChild = False : is_tableChild = " + str(is_tableChild(content))+ " : article_id : " + article.getAttribute('ID'))
                continue # article 의 child content 가 아니면 다음으로 진행

            if is_articleFirstChild == is_tableChild:
                print ( "is_articleChild == is_tableChild *********************************************************************** article_id : " + article.getAttribute('ID'))
            
            text_elements = content.getElementsByTagName('text')

            context_text = ""
            if not content.getElementsByTagName('tbl_group'):  # tbl_group 을 포함하고 있지 않으면 text 로 만든다.
                for text_element in text_elements:
                    if text_element.firstChild is not None:
                        context_text += text_element.firstChild.data

                article_xml_contexts.append(context_text.strip()) 
            else: # tbl_group 을 포함하고 있는 content는 xml로 붙인다.
                for tbl_group in content.getElementsByTagName('tbl_group'):
                    tableStr = tbl_group.toxml().replace('\n', '').replace('\t', '').strip()
                    #print ("tbl_group = " + tableStr)
                    article_xml_contexts.append(tableStr)
        
        return  ', '.join(article_xml_contexts)

    def get_article_data_paragraph(self, article, paragraph,order_seq):
        article_code = ((article.getElementsByTagName('text')[0].firstChild.data).split(' '))[0]
        article_title_text = article.getElementsByTagName('text')[0].firstChild.data
        #article_title = article_title_text.split(' ')[0]
        article_contexts = []
    # xml_length = len(str(paragraph))
        for content in article.getElementsByTagName('content'):
            if not content.getElementsByTagName('tbl_group'):
                text_elements = content.getElementsByTagName('text')

                if text_elements and text_elements[0].firstChild is not None:
                    context_text = text_elements[0].firstChild.data
                else:
                    context_text = ""

                article_contexts.append(context_text.strip())

        table_exist = 'Y' if article.getElementsByTagName('tbl_group') else 'N'
        #table_exist = 'Y : '+ str(xml_length) if article.getElementsByTagName('tbl_group') else 'N'

        return {
            'article_id': article_code,
            'article_title': article_title_text,
            'article_num': order_seq,
            'article': ', '.join(article_contexts),
            'article_original': paragraph,
            'tableYN': table_exist
        }


    def convert_to_json(self,doc_id, doc_title, output_data):
        # Converts the processed data to JSON format
        json_data = {
        'doc_id': doc_id,
        'doc_title': doc_title,
        'doc_contents': output_data
        }
        #print("convert_to_json ---------------------------------------------")
        #pprint(json_data)
        #return json.dumps(json_data)
        return json.dumps(json_data, ensure_ascii=False, indent=4)
    
    def __init__(self, xml_file,split_number,overlap_number):
        self.doc_id, self.doc_title, self.sub_sections, self.json_file = self.parse_xml(xml_file)
        self.output_data = self.process_sub_sections_str(self.sub_sections,split_number, overlap_number)
        #print("output_data : ==========================================================") 
        #pprint(output_data)
        #print("output_data : " + output_data)  
        json_data = self.convert_to_json(self.doc_id, self.doc_title, self.output_data)
        #print("json_data -------------------------------------------------------------")
        #json_data = json_data.replace('\\', '') # 쌍따옴표 제거하면 입력시 오류 발생
    
    #   print(json_data)

        print("xml_file : " + xml_file)  
        print("json_file : " + self.json_file)   
        with open(self.json_file, "w", encoding="utf-8") as f:
            f.write(json_data)   

if __name__ == '__main__':
    # Check if the XML file name is provided as a command-line argument
    if len(sys.argv) < 4:
        print(str(len(sys.argv) )+ ' : Usage: python create_json.py --target_file="inputfile.xml" --split_number=8000 --overlap_number=100')
        sys.exit(1)
    else:
        #xml_file = sys.argv[1]
        # Parse the arguments.
        parser = argparse.ArgumentParser()
        parser.add_argument("--target_file", type=str)
        parser.add_argument("--split_number", type=int, default=8000)
        parser.add_argument("--overlap_number", type=int, default=100)
        args = parser.parse_args()
        xml_file = args.target_file
 

    create_json = CreateJson(xml_file, args.split_number, args.overlap_number)
        # xml_file = xml_file1 
        # if xml_file =="":
        #     sys.exit(1)


        

  
