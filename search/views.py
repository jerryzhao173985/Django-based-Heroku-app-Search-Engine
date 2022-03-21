# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404, render

from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs
from .models import Paper

def index(request):
    return render(request, 'index.html')


# def possibleSearchWord(word)
#     wordList = []
#     words = word.split()
#     search_length = len(words)
#     return wordList


def match(search, paper, k=6):
    search_list = search.split()
    N = len(search_list)
    isMatch = False
    count = 0

    if N==1 :
        if (search in paper.title):
            isMatch = True
        return isMatch or (count>=k)

    if N>=2:
        for pw in search_list:
            if pw in paper.title:
                count += 2
            for key in paper.keywords.split(","):
                if pw in key:
                    count += 1
 
        return (isMatch or (count>=k), count)



def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        N = len(search.split())
        final_result= []
        all_papers_list = Paper.objects.all()

        if N==1:
            for paper in all_papers_list:
                if match(search, paper):
                    final_result.append((paper.title, paper.url, paper.abstract, paper.keywords))
        if N>=2:
            counts = []
            for paper in all_papers_list:
                if match(search, paper, 4)[0]:
                    final_result.append((paper.title, paper.url, paper.abstract, paper.keywords))
                    counts.append(match(search, paper, 4)[1])
            if(len(final_result)==0):
                for paper in all_papers_list:
                    if match(search, paper, 2)[0]:
                        final_result.append((paper.title, paper.url, paper.abstract, paper.keywords))
                        counts.append(match(search, paper, 2)[1])
            if(len(final_result)==0):
                for paper in all_papers_list:
                    if match(search, paper, 1)[0]:
                        final_result.append((paper.title, paper.url, paper.abstract, paper.keywords))
                        counts.append(match(search, paper, 1)[1])
            sorted_index = sorted(range(len(counts)), key=lambda k: counts[k])
            sorted_index = sorted_index[::-1]    # decending order of the index
            final_result = [final_result[qq] for qq in sorted_index]


        context = {
            'final_result': final_result
        }

        return render(request, 'search.html', context)

    else:
        return render(request, 'search.html')