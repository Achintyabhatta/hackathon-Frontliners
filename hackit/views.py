from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from . import speechtotext
from . import essentials
from . import recommendations
# Create your views here.

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['audiofile']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        results = speechtotext.perform(uploaded_file)
        dataset = essentials.perform(results['text'])
        answer = round(results['mean'],4)
        answer = answer * 100
        answer = round(answer,2)
        recommend = recommendations.perform(dataset)
        return render(request,'output.html',{'res': results['text'],'dataset':dataset, 'foot': answer,'datasetm': recommend})
    return render(request,'uploaddoc.html')