from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb


# Load AI model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Create ChromaDB client
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="resume_job_matching"
)


def extract_text(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def create_embedding(text):

    embedding = model.encode(text)

    return embedding.tolist()


def calculate_similarity(resume_text, job_description):

    resume_embedding = model.encode(resume_text)
    job_embedding = model.encode(job_description)

    similarity = model.similarity(
        resume_embedding,
        job_embedding
    )

    score = float(similarity[0][0])

    score = max(0, min(score, 1))

    return round(score * 100, 2)


def store_resume(resume_text):

    embedding = create_embedding(resume_text)

    collection.add(
        ids=["uploaded_resume"],
        documents=[resume_text],
        embeddings=[embedding]
    )