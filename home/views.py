from django.shortcuts import render, redirect
from django.http import HttpResponse

from home.models import FavBooks
from .forms import SearchQuery
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

import requests
import json

# Create your views here.


def home(request):

    context = {}
    try:
        if request.method == 'POST':
            query = request.POST['name']
            request.session['query'] = query
            context['queryres'] = callingbooks(query)
            request.session['queryres'] = context['queryres']
            return redirect(searchres)
    except Exception as e:
        return HttpResponse("No data found")

    return render(request, 'index.html', context)


def searchres(request):

    context = {}
    try:
        query = request.session['query']
        # print("Query in search res is", query)
        if request.method == 'POST':
            query = request.POST['name']
            request.session['query'] = query
            context['queryres'] = callingbooks(query)
            request.session['queryres'] = context['queryres']
            return redirect(searchres)

    except Exception as e:
        return HttpResponse("No data found")

    return render(request, 'searchres.html', context)


def bookdetails(request):
    context = {}
    try:
        query = request.session['query']
        # print("Query in search res is", query)
        if request.method == 'POST':
            query = request.POST['name']
            request.session['query'] = query
            context['queryres'] = callingbooks(query)
            request.session['queryres'] = context['queryres']
            return redirect(searchres)

    except Exception as e:
        return HttpResponse("No data found")

    return render(request, 'bookdetails.html', context)


def loginpage(request):
    if request.method == 'POST':
        username = request.POST['Name']
        password = request.POST['password']
        # print(username, password)
        user = authenticate(request, username=username, password=password)
        # Checks if the user exists in django db

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def logoutpage(request):
    # print("log out")
    logout(request)

    return redirect('home')


def register(request):
    if request.method == 'POST':
        user = request.POST['Name']
        email = request.POST['email']
        password1 = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if password1 == confirmpassword:
            if not User.objects.filter(username=user).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(
                        username=user, email=email, password=password1)
                    user.save()
        return redirect('login')
    return render(request, 'register.html')


@csrf_exempt
def updateshelf(request):
    print("Update shelf entered")
    data = json.loads(request.body)
    print(data)
    bookthumb = data['bookthumb']
    bookisbn = data['bookisbn']
    booktitle = data['booktitle']
    bookauthor = data['bookauthor']
    bookpub = data['bookpub']
    action = data['action']
    print(
        f"booktitle {booktitle} /n Bookauthor:{bookauthor}/n bookpub:{bookpub} /n isbn{bookisbn} /n action: {action}")

    current_user = request.user.username
    print(f"Cur user is {current_user}")
    favs = FavBooks.objects.create(user=current_user, btitle=booktitle,
                                   isbn=bookisbn, author=bookauthor, publisher=bookpub, thumb=bookthumb)
    favs.save()
    # messages.success(request, "Added to shelf successfully")

    return JsonResponse("Book added", safe=False)


def removebook(request, id):
    data = FavBooks.objects.get(id=id)
    data.delete()
    messages.success(request, "Removed from shelf successfully")
    return redirect('bookshelf')


def bookshelf(request):
    data = FavBooks.objects.all()
    context = {"books": data}
    return render(request, 'bookshelf.html', context)


def callingbooks(name):
    book_name = name
    URL = (
        f"https://www.googleapis.com/books/v1/volumes?q={book_name}&key=AIzaSyD2jOwIKO-F1GrhDJSs-jmXXMIigJDPOj0")
    r = requests.get(url=URL)
    data = r.json()
    # print(data)
    resultnumber = (len(data['items']))
    # print(f"Found {resultnumber} matches")
    currentquery = []
    for i in range(resultnumber):

        currentquery.append(
            [data['items'][i]['volumeInfo']['title']])  # 0 Title

        if 'authors' in data['items'][i]['volumeInfo'].keys():
            currentquery[i].append(
                data['items'][i]['volumeInfo']['authors'][0])  # 1 Authors
        else:
            currentquery[i].append("Information unavailable")

        if 'description' in data['items'][i]['volumeInfo'].keys():
            currentquery[i].append(
                data['items'][i]['volumeInfo']['description'])  # 2 Description
        else:
            currentquery[i].append("Information unavailable")

        if 'imageLinks' in data['items'][i]['volumeInfo'].keys():
            currentquery[i].append(
                data['items'][i]['volumeInfo']['imageLinks']['thumbnail'])  # 3 Thumbnail
        else:
            currentquery[i].append("Information unavailable")

        if 'publisher' in data['items'][i]['volumeInfo'].keys():
            currentquery[i].append(
                data['items'][i]['volumeInfo']['publisher'])  # 4 Publisher
        else:
            currentquery[i].append("Information unavailable")

        if 'publishedDate' in data['items'][i]['volumeInfo'].keys():
            currentquery[i].append(
                data['items'][i]['volumeInfo']['publishedDate'])  # 5 Publishing date
        else:
            currentquery[i].append("Information unavailable")

        if 'averageRating' in data['items'][i]['volumeInfo'].keys():
            currentquery[i].append(
                data['items'][i]['volumeInfo']['averageRating'])  # 6 Average Rating
        else:
            currentquery[i].append("Information unavailable")

        if 'maturityRating' in data['items'][i]['volumeInfo'].keys():
            currentquery[i].append(
                data['items'][i]['volumeInfo']['maturityRating'])  # 7 Maturity Rating
        else:
            currentquery[i].append("Information unavailable")

        if 'industryIdentifiers' in data['items'][i]['volumeInfo'].keys():
            if 'identifier' in data['items'][i]['volumeInfo']['industryIdentifiers'][0].keys():
                currentquery[i].append(
                    data['items'][i]['volumeInfo']['industryIdentifiers'][0]['identifier'])  # 8 ISBN-13
            else:
                currentquery[i].append("Information unavailable")  # 8 ISBN-13
        else:
            currentquery[i].append("Information unavailable")

        if 'pageCount' in data['items'][i]['volumeInfo'].keys():
            currentquery[i].append(
                data['items'][i]['volumeInfo']['pageCount'])  # 9 PageCount
        else:
            currentquery[i].append("Information unavailable")

        if 'language' in data['items'][i]['volumeInfo'].keys():
            currentquery[i].append(
                data['items'][i]['volumeInfo']['language'])  # 10 Language
        else:
            currentquery[i].append("Information unavailable")

        if 'previewLink' in data['items'][i]['volumeInfo'].keys():
            currentquery[i].append(
                data['items'][i]['volumeInfo']['previewLink'])  # 11 Purchase Link
        else:
            currentquery[i].append("Information unavailable")

    return currentquery
    # print(currentquery)
