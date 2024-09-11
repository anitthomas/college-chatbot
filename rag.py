import json
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone
pc = Pinecone(api_key="136639f2-8514-4dea-b63a-f77b9e614cf2")

# Create or connect to an index
index_name = "cone-hello"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # Dimension for 'all-MiniLM-L6-v2' model
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index(index_name)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load data from JSON file
with open('fee_structure.json', 'r') as file:
    data = json.load(file)

# Create embeddings and upload
for i, item in enumerate(data):
    # Assuming each item in the JSON is a dictionary with a 'text' field
    # Adjust the key if your JSON structure is different
    chunk = item['text']
    embedding = model.encode(chunk).tolist()
    index.upsert(vectors=[(str(i), embedding, {"text": chunk})])

print(f"Uploaded {len(data)} items to RAG system")