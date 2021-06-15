from django.shortcuts import render,HttpResponse
from WikiCSSH.Tapping.tapping import get_final_data
from WikiCSSH.VisulizeWIKICSSH.visual import get_final_page

def home(request):
    return render(request,'home.html')

def tapping(request):
    if 'tap' and 'text' in request.POST:
        if request.POST.get("text") is None:
            print(request.POST.get("text"))
            return HttpResponse("The data is empty Plese enter some text")
        else :
            data = request.POST.get("text")
            return HttpResponse(get_final_data(data))
    else :
        print(request.POST.get("tap"))
        return render(request,'tapping.html')

def visualize(request):
    return HttpResponse(get_final_page())