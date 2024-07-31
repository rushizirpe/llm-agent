from django.shortcuts import render
from django.http import JsonResponse
from transformers import pipeline
import llm

def index(request):
    llm_response = ""
    if request.method == 'POST':
        model = llm.get_model("orca-mini-3b")
        llm_response = model.prompt(request.POST.get('prompt')).text()

    return render(request, 'index.html', { 'llm_response': llm_response})

def launch_api(request):
    if request.method == 'POST':
        request.session['api_launched'] = True
        return render(request, 'api.html', {'message': 'API Launched!'})
    return render(request, 'api.html')

def stop_api(request):
    if request.method == 'POST':
        request.session['api_launched'] = False
        return render(request, 'api.html', {'message': 'API Stopped!'})
    return render(request, 'api.html')

def chat_completion(request):
    if not request.session.get('api_launched', False):
        return JsonResponse({'error': 'API not launched'}, status=403)

    chat_model = pipeline("text-generation", model="gpt2")
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        if prompt:
            response = chat_model(prompt, max_length=50, num_return_sequences=1)
            generated_text = response[0]['generated_text']
            
            return JsonResponse({'text': generated_text.rsplit('.', 1)[0].replace(prompt, '').strip() + "."})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_embeddings(request):
    if not request.session.get('api_launched', False):
        return JsonResponse({'error': 'API not launched'}, status=403)

    embedding_model = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if text:
            embeddings = embedding_model(text)
            return JsonResponse({'embeddings': embeddings[0][0]}) 
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def api_view(request):
    return render(request, 'api.html')
