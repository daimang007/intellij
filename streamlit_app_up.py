import streamlit as st
from langchain import OpenAI
from langchain import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
# import openai


text ="너는 고객센터이다. 시스템 엔지니어게 문제나 질문을 해결할수 있도록 아래 형식으로 정보를 제공함.\
경우별 구분하여 표시, 인프라(Network, Database, Interface, 유관기관) 에러를 우선, \
장애등급이 1,2,3,4 중 작은숫자를 우선하여 조회 ,\
가능하면, 표를 사용하여 표시하고, \
관련 있는 3개 이상의 건을 표시하고 \
표시할 정보의 상세 항목은 아래와 같고 page 별로 표시 해줘  \
.장애번호:  \
.장애내용:  \
.장애유형:\
.담당자: \
.발생일시: \
.영향도: \
.고객사: \
 "

def generate_response(txt,text):
    # Instantiate the LLM model
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    # Split text
    # text_splitter = CharacterTextSplitter()
    text_splitter = CharacterTextSplitter(chunk_size=2048, chunk_overlap=0)
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap=0) 
    texts = text_splitter.split_text(txt)
    # Create multiple documents
    docs = [Document(page_content=t) for t in texts]


    print(f"len(docs) : {len(docs)}")
    print(f"docs : {docs}")
    # Text summarization

    prompt_template = """

    {text}

    """
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])

    # chain =load_summarize_chain(llm, chain_type="stuff", prompt=PROMPT) 
    # chain = load_summarize_chain(llm, chain_type="refine",verbose=True,refine_prompt=PROMPT)
    # chain = load_summarize_chain(llm, chain_type="map_reduce",map_prompt=PROMPT, combine_prompt=PROMPT)
    # chain = load_summarize_chain(llm, chain_type='map_reduce')
    #  return chain.run(docs)
    _question = f"{text}{'인증 지연 장애는 있었나요?'}"
    #chain = load_qa_chain(llm = llm , chain_type="stuff")
    chain = load_qa_chain(llm=llm, chain_type="stuff")
    print(f"LLM Question :{_question}")
    response = chain({"input_documents": docs, "question": _question }, return_only_outputs=True)

    return response

# Page title
st.set_page_config(page_title='🦜🔗 Text Summarization App')
st.title('🦜🔗 Text Summarization App')

# Text input
txt_input = st.text_area('Enter your text', '', height=200)
openai_api_org=""
openai_api_key="sk-"

# # Form to accept user's text input for summarization
result = []
with st.form('summarize_form', clear_on_submit=True):
    # openai_api_key = st.text_input('OpenAI API Key', type = 'password', disabled=not txt_input)
    submitted = st.form_submit_button('Submit')
    if submitted and openai_api_key.startswith('sk-'):
        with st.spinner('Calculating...'):
            response = generate_response(txt_input,text)
            result.append(response)
            del openai_api_key

if len(result):
    print(f"result : {result}")
    st.info(response)





system_message = {"role": "system", "content": text}
conversation = []
conversation.append(system_message)
conversation.append({"role": "user", "content": txt_input})

# openai.api_type = "Azure"
# openai.api_base = "https://poc-aitest-skt.openai.azure.com/"
# openai.api_key = "e7dda5bff0324b28bbb5457dd2979c42"
# openai.api_version = "2023-03-15-preview"
# completion = openai.ChatCompletion.create(
#               engine='gpt-35-turbo',
#               messages=conversation,
#               temperature=0.1
#             )


# print(completion['choices'][0]['message']['content'])
# st.info(completion['choices'][0]['message']['content'])

# st.text(completion['choices'][0]['message']['content'])

