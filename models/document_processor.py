from PyPDF2 import PdfReader
import tiktoken
from langchain.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_together import Together
from ollama import Client as OllamaClient
import os
import re
import json

class DocumentProcessor:
    def __init__(self, api_key_or_host, model_name, service='ollama'):
        self.service = service
        self.model_name = model_name
        if service == 'ollama':
            self.client = OllamaClient(host=api_key_or_host)
        elif service == 'together':
            os.environ["TOGETHER_API_KEY"] = api_key_or_host
            self.llm = Together(
                model=model_name,
                temperature=0.7,
                max_tokens=2000,
                top_k=1,
            )
        else:
            raise ValueError(f"Unsupported service: {service}")
        
        self.entity_output_schema_parser = self.setup_output_schema_parser()
        self.entity_prompt_template = self.setup_prompt_template()

    def setup_output_schema_parser(self):
        return StructuredOutputParser.from_response_schemas([
            ResponseSchema(name="application_domain", description="The application domain of the ontology described in the document."),
            ResponseSchema(name="summary", description="A brief summary or description of the ontology."),
            ResponseSchema(name="competency_questions", description="A list of competency questions related to the ontology.", many=True)
        ])

    def setup_prompt_template(self):
        return PromptTemplate.from_template("""
        Given the text content of a PDF document, extract the following information according to the format instructions:

        << FORMAT >>

        {format_instructions}

        Additional formatting instructions:

        - Use double quotes for all string values in the JSON output.
        - If a value is not available or not applicable, use an empty string with double quotes, e.g., "".
        - For the "competency_questions" field, provide a list of strings, with each string representing a competency question.
          - If no competency questions are provided or available, use an empty list, e.g., [].
        - Ensure the JSON output is valid and properly formatted.
        - Provide the JSON output without enclosing it in ```json code blocks.
        - just give me the JSON output, you don't need to provide any elaboration.

        << INPUT >>

        {pdf_content}

        << OUTPUT >>
        """)

    def get_completion(self, prompt):
        if self.service == 'ollama':
            response = self.client.chat(model=self.model_name, messages=[{'role': 'user', 'content': prompt}])
            return response['message']['content']
        elif self.service == 'together':
            response = self.llm.invoke(prompt)
            return response
        else:
            raise ValueError(f"Unsupported service: {self.service}")

    def count_tokens(self, text, encoding_name):
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(text))

    def extract_text_from_pdf(self, file):
        try:
            pdf_reader = PdfReader(file)
            return "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
        except Exception as e:
            print(f"Failed to extract text from PDF: {str(e)}")
            return None

    def truncate_content_if_necessary(self, content, max_tokens=7000):
        token_count = self.count_tokens(content, "cl100k_base")
        if token_count > max_tokens:
            encoding = tiktoken.get_encoding("cl100k_base")
            encoded_tokens = encoding.encode(content)
            truncated_tokens = encoded_tokens[:max_tokens]
            return encoding.decode(truncated_tokens)
        return content

    def clean_output(self, raw_output):
        cleaned = raw_output.strip()
        cleaned = re.sub(r'^```json\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned)
        cleaned = re.sub(r',\s*}', '}', cleaned)
        cleaned = re.sub(r',\s*]', ']', cleaned)
        return cleaned

    def process_pdf_raw(self, file):
        pdf_content = self.extract_text_from_pdf(file)
        if not pdf_content:
            return None

        pdf_content = self.truncate_content_if_necessary(pdf_content)

        entity_prompt = self.entity_prompt_template.format(
            pdf_content=pdf_content,
            format_instructions=self.entity_output_schema_parser.get_format_instructions()
        )

        raw_output = self.get_completion(entity_prompt)
        return self.clean_output(raw_output)

    def process_pdf(self, file):
        raw_output = self.process_pdf_raw(file)
        if raw_output is None:
            return None
        return self.entity_output_schema_parser.parse(raw_output)