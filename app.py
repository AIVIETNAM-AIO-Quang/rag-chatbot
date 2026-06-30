import streamlit as st
import chromadb
from openai import OpenAI
import pypdf

st.set_page_config(
    page_title="RAG Chatbot",
)

st.title("RAG Chatbot")
st.write("A simple Chatbot for studying.")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

def chunk_text(text, size = 1000, overlap = 200):
  chunks, start = [], 0
  while start < len(text):
    chunks.append(text[start:start + size])
    start += size - overlap
  return chunks

def embed(texts):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )
    return [item.embedding for item in response.data]

def process_pdf(file):
  text = "".join(p.extract_text() or "" for p in pypdf.PdfReader(file).pages)
  chunks = chunk_text(text)
  col = chromadb.Client().get_or_create_collection("rag")
  col.add(ids=[str(i) for i in range(len(chunks))], documents = chunks, embeddings = embed(chunks))

  return col, len(chunks)

def retrieve(query, collection, k = 2):
  q = embed(query)
  res = collection.query(query_embeddings=q, n_results=k)
  return res["documents"][0]

PROMPT = """You are a QA assistant. Use the context below to answer the question. If the context has no relevant information, say you don't know - do not make things up. Answer concisely.

Context: {context}

Question: {question}

Answer:"""

def rag(question, collection, k=2):
  context = "\n\n".join(retrieve(question, collection, k))
  prompt = PROMPT.format(context = context, question = question)
  resp = client.chat.completions.create(
    model=CHAT_MODEL,
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)
return resp.choices[0].message.content

for k, v in {"collection": None, "chat_history": []}.items():
  st.session_state.setdefault(k, v)

with st.sidebar:
  f = st.file_uploader("Choose a PDF file", type = "pdf")
  if f and st.button("Process PDF"):
    st.session_state.collection, n = process_pdf(f)
    st.success(f"{n} chunks indexed")

for m in st.session_state.chat_history:
  st.chat_message(m["role"]).write(m["content"])

q = st.chat_input("Ask a question...")
if q and st.session_state.collection:
  ans = rag(q, st.session_state.collection)
  st.session_state.chat_history +=[
      {"role": "user", "content": q},
      {"role": "assistant", "content": ans}
  ]
  st.rerun()
