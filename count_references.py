import dspy, os, re
from langchain_community.document_loaders import PDFMinerLoader

# --- Configuration ---
# Ensure Ollama is running with llama3.1:latest
ollama_model = dspy.LM(api_key="", api_base='http://localhost:11434', model="ollama_chat/llama3.2:latest", max_tokens=2000)
dspy.configure(lm=ollama_model)

# --- PDF Processing Functions ---
def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts all text from a PDF file using LangChain's PDFMinerLoader."""
    try:
        docs = PDFMinerLoader(pdf_path, mode = "single",pages_delimiter = "",).load()
        return "".join(doc.page_content for doc in docs)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def get_references_section(full_text: str) -> str:
    """Extracts the "References" section using a simple regex heuristic."""
    match = re.search(r'(?i)(References|Bibliography|Works Cited)\s*\n', full_text)
    if not match:
        return ""
    start = match.end()
    # Find the next major section heading or end of document
    end_match = re.search(r'(?i)\n\s*(?!REFERENCES|BIBLIOGRAPHY|WORKS CITED)[A-Z][a-z]+(\s[A-Z][a-z]+){0,2}\s*\n', full_text[start:])
    end = start + end_match.start() if end_match else len(full_text)
    return full_text[start:end]

# --- DSPy Signatures ---
class ExtractReferences(dspy.Signature):
    """Extracts individual academic reference entries from a text block."""
    references_text_block: str = dspy.InputField(desc="A block of text potentially containing academic references")
    individual_references: str = dspy.OutputField(desc="List of individual references, each on a new line")

class CheckAuthorPresence(dspy.Signature):
    """Determines if a specific author's name is in a reference string."""
    reference_entry: str = dspy.InputField(desc="A single academic reference entry")
    author_to_find: str = dspy.InputField(desc="The name of the author to check for")
    is_present: bool = dspy.OutputField(desc="True if the author is present, False otherwise")

# --- DSPy Module ---
class ReferenceCounter(dspy.Module):
    def __init__(self):
        super().__init__()
        # Use ChainOfThought for better reasoning
        self.extract_refs = dspy.ChainOfThought(ExtractReferences)
        self.check_author = dspy.ChainOfThought(CheckAuthorPresence)

    def forward(self, pdf_text: str, target_author: str) -> int:
        # Get the references section, or fall back to the full text
        refs_text = get_references_section(pdf_text) or pdf_text
        
        # Use LLM to extract a clean list of references
        extracted = self.extract_refs(references_text_block=refs_text).individual_references
        if not extracted or extracted.lower() == "no references found.":
            return 0
        
        raw_references = [ref.strip() for ref in extracted.split('\n') if ref.strip()]
        
        # Count references by the target author using a concise sum and generator expression
        return sum(
            1 for ref in raw_references
            if self.check_author(reference_entry=ref, author_to_find=target_author).is_present
        )

# --- Main Execution ---
if __name__ == "__main__":
    # Change this to your PDF file path
    pdf_file_path = "Paper.pdf"
    # Change this to the author you are looking for
    author_to_find = "Lawrence"

    if os.path.exists(pdf_file_path):
        full_text = extract_text_from_pdf(pdf_file_path)
        if full_text:
            print(f"Searching for references by '{author_to_find}'...")
            counter = ReferenceCounter()
            try:
                ref_count = counter(pdf_text=full_text, target_author=author_to_find)
                print(f"Number of references by '{author_to_find}': {ref_count}")
            except Exception as e:
                print(f"An error occurred during DSPy processing: {e}")
        else:
            print("Could not extract text from the PDF.")
    else:
        print(f"PDF file not found at '{pdf_file_path}'.")
