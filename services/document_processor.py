from models.document_processor import DocumentProcessor as DocumentProcessorModel
from config import Config

class DocumentProcessor:
    @staticmethod
    def process_document(document_file):
        try:
            processor = DocumentProcessorModel(Config.OLLAMA_HOST, Config.OLLAMA_MODEL, Config.OLLAMA_SERVICE)
            result = processor.process_pdf(document_file)
            if result is None:
                return None, "Failed to process PDF document"
            return result, None
        except Exception as e:
            return None, str(e)