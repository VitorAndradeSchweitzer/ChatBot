from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

from decouple import config
# Initialize Groq LLM
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7,
     api_key=config('GROQ_API_KEY'),
)

class Init(TemplateView):
    template_name = "pages/init.html"
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["extra_info"] = "This is additional data."
            return context


class APIendpointteste2(APIView):
    def get(self, request):
        return Response({"message": "Use POST to send input"})
    def post(self, request):
        user_input = request.POST.get("user_input", "Write a song about a crazy man")
        # Define the expected JSON structure
        parser = JsonOutputParser(pydantic_object={
            "type": "object",
            "properties": {
                "song-title": {"type": "string"},
                "lyrics": {"type": "string"},
               
            }
        })

        # Create a simple prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Create a Song about the theme givem by the user and return into JSON with this structure:
                {{
                    "song-title": "song title ",
                    "lyrics": short-song-created,
                    """),
            ("user", "{input}")
        ])


        chain = prompt | llm | parser

        def parse_product(description: str) -> dict:
            result = chain.invoke({"input": description})
            return result

                
        # Example usage
        description = f"""
        {user_input}"""

     

        data = parse_product(description)  
        return JsonResponse(data)






