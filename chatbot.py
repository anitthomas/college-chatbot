import streamlit as st
import google.generativeai as genai
import json
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# Set up Gemini API
genai.configure(api_key="AIzaSyBsaDGXpE-hrJpIuzOUf8_UDDIlACgihUs")

# Initialize Pinecone
pc = Pinecone(api_key="136639f2-8514-4dea-b63a-f77b9e614cf2")
index = pc.Index("cone-hello")

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize global variables
fee_structure_data = None
residential_data = None

def load_fee_structure():
    """Load fee structure data from JSON file."""
    global fee_structure_data
    try:
        with open('fee_structure.json', 'r') as file:
            fee_structure_data = json.load(file)
    except FileNotFoundError:
        st.error("Fee structure file not found.")
    except json.JSONDecodeError:
        st.error("Error decoding the JSON file.")

def load_residential_data():
    """Load residential facility data from JSON file."""
    global residential_data
    try:
        with open('residential_facilities.json', 'r') as file:
            residential_data = json.load(file)
    except FileNotFoundError:
        st.error("Residential data file not found.")
    except json.JSONDecodeError:
        st.error("Error decoding the residential data JSON file.")

def get_relevant_context(query, top_k=3):
    """Retrieve relevant context from Pinecone."""
    query_embedding = model.encode(query).tolist()
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    context = "\n".join([match['metadata']['text'] for match in results['matches']])
    return context

def generate_response_gemini(query, context):
    """Generate response using Gemini API with fee structure and residential data."""
    global fee_structure_data, residential_data
    
    if "fee" in query.lower() and "structure" in query.lower():
        fee_structure_markdown = """
# College Fee Structure

| Year | Admission Fee | Caution Deposit | Tuition Fee | Value Added Courses | Other University Fees | Exam Fees | Conveyance Charges | PTA Fees | Total |
|------|---------------|-----------------|-------------|---------------------|----------------------|-----------|-------------------|----------|-------|
| I YEAR | 500 | 10000 | 37500 | 5000 | 1500 | 1700 | 56200 | 7500 | 119900 |
| II YEAR | - | - | 37500 | 5000 | 1700 | 44200 | 7500 | 2500 | 98400 |
| III YEAR | - | - | 37500 | 5000 | 1700 | 44200 | 7500 | 2500 | 98400 |
| IV YEAR | - | - | 37500 | 5000 | 1700 | 44200 | 7500 | 2500 | 98400 |

*Note:* All amounts are in INR (Indian Rupees).

## Fee Structure Highlights:

- *Admission Fee* and *Caution Deposit* are one-time payments in the first year.
- *Tuition Fee* remains constant at 37,500 INR per year.
- *Value Added Courses* fee is consistent at 5,000 INR annually.
- *Exam Fees* increase significantly after the first year.
- *Conveyance Charges* decrease after the first year.
- *PTA Fees* are higher in the first year.

The total cost for all four years of study is approximately 415,100 INR.

For any specific queries about the fee structure or payment options, please contact the college's finance department.
"""
        return fee_structure_markdown
    
    # Format the data for inclusion in the prompt
    formatted_fee_structure = json.dumps(fee_structure_data, indent=2)
    formatted_residential_data = json.dumps(residential_data, indent=2)
    
    # Prepare the prompt for the AI model
    prompt = f"""You are an AI assistant for a college. Use the following context, fee structure data, and residential facility data to answer the question. 
    If the data doesn't contain relevant information, say so.
    
    Context: {context}
    
    Fee Structure Data:
    {formatted_fee_structure}
    
    Residential Facility Data:
    {formatted_residential_data}
    
    Human: {query}
    AI:"""
    
    # Generate response using Gemini API
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def check_for_keywords(prompt, keywords):
    """Check if any of the keywords are in the prompt."""
    return any(keyword.lower() in prompt.lower() for keyword in keywords)

def get_keyword_response(keyword):
    """Return a predefined response for a given keyword."""
    keyword_responses = {
        "fees": "Here's information about our fee structure: ...",
        "hostel": "Information about our hostel facilities: ...",
        "admission": "For admission inquiries, please visit our admissions page at ...",
        # Add more keywords and responses as needed
    }
    return keyword_responses.get(keyword, "I don't have specific information for that keyword.")

# Streamlit UI
st.title("Institutional Chatbot")

# Load data when the app starts
load_fee_structure()
load_residential_data()

# Define keywords to check for
keywords = ["fees", "hostel", "admission"]  # Add more keywords as needed

# Main chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input prompt for user
if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate the response
    with st.chat_message("assistant"):
        if check_for_keywords(prompt, keywords):
            # If a keyword is found, use the predefined response
            for keyword in keywords:
                if keyword.lower() in prompt.lower():
                    response = get_keyword_response(keyword)
                    break
        else:
            # If no keyword is found, generate a response using the existing method
            context = get_relevant_context(prompt)
            response = generate_response_gemini(prompt, context)
        
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})