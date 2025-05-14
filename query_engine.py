from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from gemini_direct import run_gemini

def get_prompt_template():
    return PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful assistant. Answer ONLY using the context below.
If the context is insufficient, just say: "I don’t know based on the video."

Context:
{context}

Question: {question}
"""
    )

def build_qa_chain(retriever, llm_or_type, api_key=None):
    prompt = get_prompt_template()
    parser = StrOutputParser()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def chain(question):
        docs = retriever.invoke(question)
        context = format_docs(docs)
        full_prompt = prompt.invoke({"context": context, "question": question})

        if llm_or_type == "direct":
            return run_gemini(full_prompt.to_string(), api_key)

        return parser.invoke(llm_or_type.invoke(full_prompt))

    return chain

