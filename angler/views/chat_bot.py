from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from google import genai
from google.genai import types
from google.genai import errors
from django.utils.html import linebreaks
from angler.models.chatbot import HiloChat

def ask_genai(message):
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=message,
            config=types.GenerateContentConfig(
                max_output_tokens=150,
                tools=[],
                response_mime_type="text/plain",
                system_instruction="Your name is Hilo and you are a expert fishing assistant for AnglerSpot. You are strictly a text only assistant. You only answer fishing related questions. These questions can include fish identification, good fishing locations, fishing equipment, ideal weather condiditions for fishing and any techniques that would help to catch fish. Keep answers short and concise, try to stay within the constraints of 150 output tokens. You are a strict text-only assistant. Do not request, describe, or attempt to generate images, audio, video, files, or executable code blocks. Dont use wasteful things like asterisks to delineate things like items in a list of items.",
            )
        )
        return response.text
    except errors.ClientError as e:
        if e.code == 429:
            return "Hilo AI rate limit reached. Please try again later."


class ChatBotView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        chats = HiloChat.objects.filter(user=request.user)
        context = {'chats':chats}
        return render (request, 'angler/chatbot.html', context)
    def post(self, request):
        message = request.POST.get('message')
        response = ask_genai(message)
        HiloChat.objects.create(user=request.user, message=message, response=response)
        return JsonResponse({'message': message, 'response': linebreaks(response)})