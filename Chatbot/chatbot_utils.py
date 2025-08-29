from decouple import config

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import  ChatMessage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
import json
# Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7,
     api_key=config('GROQ_API_KEY'),
)


generic_parser = JsonOutputParser(pydantic_object={
    "type": "object",
    "properties": {
        "practice_tip": {"type": "string"},
        "recommended_instrument": {"type": "string"}
    },
    "required": ["practice_tip", "recommended_instrument"]
})

generic_prompt = ChatPromptTemplate.from_messages([
    ("system", """Você é Maestro, um assistente especializado em dicas de estudo musical e recomendações de instrumentos. 
Dado o tema fornecido pelo usuário, retorne um JSON com apenas esta estrutura, não adicione nenhum texto a mais, e mantenha a resposta curta:

{{
    "practice_tip": "uma dica útil de estudo ou prática relacionada ao tema",
    "recommended_instrument": "instrumento mais indicado para esse tema ou estilo musical"
}}
"""),
    ("user", "{input}")
])




def chatbot_generate_response(user_input):
        chain = generic_prompt | llm | generic_parser

        def parse_product(description: str) -> dict:
            result = chain.invoke({"input": description})
            return result

        description = f"""
        {user_input}"""
        data = parse_product(description)  
        return data


def generate_response_with_summary(conversation, user_input, llm=llm):
    if conversation.memory:
        mem = ConversationSummaryMemory(llm=llm)
        mem.load_memory_variables({"history": json.loads(conversation.memory)})
    else:
        mem = ConversationSummaryMemory(llm=llm)



    chain = generic_prompt | llm
    # Cria a chain com memória, vou
    chain = ConversationChain(llm=llm, memory=mem, verbose=True)

    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: mem.chat_memory, 
        input_messages_key="input",
        history_messages_key="history",
    )
        
    response = chain_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": str(conversation.id)}}
    )

    #ai_response = response.content if hasattr(response, "content") else str(response)
    ai_response = response['response']
    # Salva mensagens no banco
    ChatMessage.objects.create(conversation=conversation, role="human", content=user_input)
    ChatMessage.objects.create(conversation=conversation, role="ai", content=ai_response)

    # Atualiza a memória resumida no banco
    mem_json = json.dumps(mem.load_memory_variables({})['history'])
    conversation.memory = mem_json
    conversation.save()

    return ai_response