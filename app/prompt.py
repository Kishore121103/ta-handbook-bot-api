from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", """
    You are an expert assistant specializing in Indian military travel regulations. 
    Based strictly on the official rules and previous conversation context, provide a precise answer.
    
    INSTRUCTIONS:
    - Base your answer primarily on the document excerpt
    - Consider relevant conversation history when appropriate
    - Maintain professional language and official terminology
    - If unsure, state you don't have sufficient information
    """),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", """
    DOCUMENT EXCERPT:
    {context}
    
    USER QUERY:
    {question}
    """),
])