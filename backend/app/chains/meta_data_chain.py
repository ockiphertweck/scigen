import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from typing import List, Optional
from langchain_core.prompts import PromptTemplate
from typing import List
from pydantic import BaseModel, SecretStr
from langchain_core.output_parsers import JsonOutputParser

from langchain_openai import ChatOpenAI


load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

llm = ChatOpenAI(model="gpt-4",
                 temperature=0)  # type: ignore


class MetaData(BaseModel):
    title: str
    keywords: List[str]


meta_data_ouptut_parser = JsonOutputParser(pydantic_object=MetaData)


meta_data_prompt_template = """
Provide the Title and Keywords for the document below:

{context}

Only output the generated Meta Daa, no additional information.
{format_instructions}
"""


meta_data_prompt = PromptTemplate.from_template(meta_data_prompt_template, partial_variables={
                                                "format_instructions": meta_data_ouptut_parser.get_format_instructions()},)


chain = (meta_data_prompt | llm | meta_data_ouptut_parser)
