from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib import messages
import os, time
import pandas as pd
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM,AutoModelForCausalLM
from transformers import pipeline
import torch
import base64
import textwrap
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA


# Global variable and models
# loading embedding model
embeddings = SentenceTransformerEmbeddings(model_name = "all-MiniLM-L6-v2")

checkpoint = '../libraries/ML_Model/LaMini-Flan-T5-783M'
# checkpoint = './libraries/ML_Model/LaMini-GPT-1.5B'
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint,device_map="auto",
                                              torch_dtype=torch.float32,offload_folder='offload_weights')

# Create your views here.
def upload_files(request):
    if request.session.get('user_email') is not None:
        if request.method == "POST":
            # Get a list of uploaded files using getlist
            uploaded_files = request.FILES.getlist('files')
            repo_type = request.POST.get('repoType')
            email = request.session.get('user_email')
            # Process each uploaded file
            
            # print("|"*50)
            # print(uploaded_files)
            
            try:
                for file in uploaded_files:
                    # print("|"*50)
                    # print(file)
                    text_splitter = RecursiveCharacterTextSplitter(
                        separators=["\n"],
                        chunk_size=300,
                        chunk_overlap=120,
                        length_function=len
                    )
                    with open('./media/uploadedFiles/' + file.name, 'wb+') as destination:
                                    for chunk in file.chunks():
                                        destination.write(chunk)
                    
                    loader = PyPDFLoader('./media/uploadedFiles/' + file.name)
                    pages = loader.load()
                    docs = text_splitter.split_documents(pages)
                    os.remove('./media/uploadedFiles/' + file.name)
                    
                    # comverting into db 
                    db = FAISS.from_documents(docs, embeddings)
                    
                    if repo_type == 'publicRepo':
                        # Handle each file here as needed
                        path = "./media/user/publicRepo/"
                        dir = os.listdir(path)
                        # Checking if the list is empty or not
                        if len(dir) == 0:
                            print('Creating The DB in public')
                            db.save_local('./media/user/publicRepo/publicDB')
                        else:
                            print('Merging The DB in public')
                            old_db = FAISS.load_local('./media/user/publicRepo/publicDB', embeddings)
                            old_db.merge_from(db)
                            old_db.save_local('./media/user/publicRepo/publicDB')                    
                    else:
                        # Handle each file here as needed
                        print('Creating The DB in private')
                        db.save_local('./media/user/privateRepo/' + email)

                messages.success(request, 'Successfully Uploaded! Please ask questions.')
                return redirect('user:upload_files')
            except Exception as e:
                print("|"*50)
                print("error while uploading the files: ", e)
                messages.error(request, 'Error! While uploading please try again.')
                return redirect('user:upload_files')
        return render(request, 'user/upload.html')
    else:
        return redirect('auths:index')

def select_repo(request):
    email = request.session.get('user_email')
    if request.session.get('user_email') is not None:
        if request.method=="POST":
            repo_type = request.POST.get("repotype")
            request.session['repo_type'] = repo_type
            if repo_type == 'publicRepo':
                # Handle each file here as needed
                path = "./media/user/publicRepo/"
                dir = os.listdir(path)
                # Checking if the list is empty or not
                if len(dir) == 0:
                    messages.error(request, 'Empty Repository! Please upload file.')
                    return redirect('user:upload_files')
                else:
                    return redirect('user:ask_question')
            else:
                try:
                    path = "./media/user/privateRepo/"+email+"/"
                    dir = os.listdir(path)
                    # Checking if the list is empty or not
                    if len(dir) == 0:
                        messages.error(request, 'Empty Repository! Please upload file.')
                        return redirect('user:upload_files')
                    else:
                        return redirect('user:ask_question')  
                except Exception as e:
                    messages.error(request, 'Empty Repository! Please upload file.')
                    return redirect('user:upload_files')
        return render(request, 'user/selectRepo.html')
    else:
        return redirect('auths:index')

def ask_question(request):
    if request.session.get('user_email') is not None:
        # load csv and send QnA to UI
        # Specify the path to your CSV file
        email = request.session.get('user_email')
        file_name = "./media/user/QnA/"+email+".csv"
        
        qna_df = pd.read_csv(file_name)
        ques_list = qna_df['Question'].tolist()
        ans_list = qna_df['Answer'].tolist()
        source_list = qna_df['Source'].tolist()
        page_list = qna_df['Page'].tolist()
        line_list = qna_df['Line'].tolist()
        qna_list = zip(ques_list, ans_list, source_list, page_list, line_list)
        
        if request.session.get('repo_type') == "privateRepo":
            repo_type = "Private Repository"
        else:
            repo_type = "Public Repository"
        context = {'qna_list' : qna_list, 'repo_type' : repo_type}
        return render(request, 'user/askQues.html', context)
    else:
        return redirect('auths:index')
    
def send_answer(request):
    if request.session.get('user_email') is not None:
        question = request.GET.get('question')
        email = request.session.get('user_email')

        # Get Anwser
        if request.session.get('repo_type') == "privateRepo":
            # answer = '''Sorry, I am in development phase.
            # You have selected private repository'''
            db_loc = './media/user/privateRepo/' + email
        else:
            # answer = '''Sorry, I am in development phase.
            # You have selected public repository'''
            db_loc = './media/user/publicRepo/publicDB'
        answer, generated_output = process_answer(question, db_loc)
        line = set()
        page = set()
        source = set()
        for i in range(len(generated_output['source_documents'])):
            a = generated_output['source_documents'][i].page_content.replace("\n", " ")
            a = a.replace("-\n", "")
            line.add(a)
            # line.add(x['source_documents'][i].page_content)
            source.add(generated_output['source_documents'][i].metadata['source'])
            page.add(str(generated_output['source_documents'][i].metadata['page']+1))

        save_line = "/\n/".join(line)
        save_page = "; ".join(page)
        save_source = "; ".join(source)
        ajax_line = "<br>".join(line)

        # Updating QnA in csv
        # Specify the path to your CSV file
        file_name = "./media/user/QnA/"+email+".csv"
        qna_df = pd.read_csv(file_name)
        
        # Check the number of rows
        if len(qna_df) < 10:
            # Add new data to the DataFrame
            new_row = pd.Series({'Question': question, 'Answer': answer, 'Source':save_source, 'Page':save_page, 'Line':save_line})
            qna_df = pd.concat([qna_df, new_row.to_frame().T], ignore_index=True)
        else:
            # Remove the 1st row and add new data to the 10th row
            qna_df = qna_df.iloc[1:]
            new_row = pd.Series({'Question': question, 'Answer': answer, 'Source':save_source, 'Page':save_page, 'Line':save_line})
            qna_df = pd.concat([qna_df, new_row.to_frame().T], ignore_index=True)
        # Write the modified DataFrame back to the CSV file
        qna_df.to_csv(file_name, index=False)
        
        # print('|'*100)
        # print(answer)
        # print('|'*100)
        # print(generated_output)
        # Sending answer to UI
        context = {
            'answer': answer,'source':save_source, 'page':save_page, 'line':ajax_line,
        }
        return JsonResponse(context)   
    else:
        return redirect('auths:index')
    


def llm_pipeline():
    pipe = pipeline(
        'text2text-generation',
        # 'text-generation',
        model=base_model,
        tokenizer=tokenizer,
        max_length = 512,
        do_sample=True,
        temperature=1.8,
        top_p=0.80,
        # repetition_penalty=1.2
    )
    local_llm = HuggingFacePipeline(pipeline=pipe)
    return local_llm

# @st.cache_resource
def qa_llm(db_loc):
    llm = llm_pipeline()
    db = FAISS.load_local(db_loc, embeddings)
    # retriever = db.as_retriever(search_type='similarity',k=4)    
    retriever = db.as_retriever(search_type="mmr", search_kwargs={'k': 5})  
    
    qa = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type= "stuff", #map-reduce,Refine,map-rerank
        retriever=retriever,
        return_source_documents = True
    )
    return qa #,retriever.metadata

def process_answer(instruction, db_loc):
    response = ''
    instruction = instruction
    qa = qa_llm(db_loc)
    generated_text = qa(instruction)
    answer = generated_text['result']
    return answer, generated_text #,metadata