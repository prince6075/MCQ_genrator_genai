import os
import PyPDF2
import json
import pandas as pd
import traceback
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv


load_dotenv()

key=os.getenv("OPENAI_API_KEY")
#print(key)

llm=ChatOpenAI(openai_api_key=key,model_name="gpt-3.5-turbo",temperature=0.7)

with open("C:/Users/princ/genrativeAi/genaiprojcet/MCQ_genrator_genai/Response.json", "r") as f:
    RESPONSE_JSON = json.load(f)


TEMPLATE= """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{RESPONSE_JSON}

"""

quiz_genration_prompt= PromptTemplate(
    input_variables=["text","number","subject","tone","RESPONSE_JSON"],
    template=TEMPLATE
)

## it connect the prompt and llm model
quiz_chain=LLMChain(llm=llm,prompt=quiz_genration_prompt,output_key="quiz",verbose="True")


TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt= PromptTemplate(
    input_variables=["subject","quiz"],
    template=TEMPLATE2
)

review_chain=LLMChain(llm=llm,prompt=quiz_evaluation_prompt,output_key="review",verbose="True")

# it connect both the chains
genrate_evaluation_chain=SequentialChain(chains=[quiz_chain,review_chain],input_variables=["text","number","subject","tone","RESPONSE_JSON"],output_variables=["quiz","review"],verbose=True)
