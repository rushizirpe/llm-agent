from django.shortcuts import render
import llm

def index(request):
    llm_response = ""
    if request.method == 'POST':
        model = llm.get_model("orca-mini-3b")
        llm_response = model.prompt(request.POST.get('prompt')).text()

    return render(request, 'index.html', { 'llm_response': llm_response})