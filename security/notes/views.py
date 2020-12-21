from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from datetime import datetime
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import sqlite3

from .models import Note

# Create your views here.

@login_required
def index(request):
  latest_notes = Note.objects.order_by('-pub_date')[:25]
  content = { 'latest_notes': latest_notes }
  return render(request, 'notes/index.html', content)

@login_required
def note(request, note_id):
  note = Note.objects.get(id=note_id)
  return HttpResponse(
    "<div>%s</div><div></br>%s @ %s</div>"
    % (note.note_text, note.user.username, note.pub_date)
  )

@login_required
def add(request):
  user = request.user
  note = request.POST.get('content')
  cursor = sqlite3.connect('db.sqlite3').cursor()

  cursor.executescript("""
    INSERT into notes_note (note_text, pub_date, user_id)
    values('%s', '%s', %s);
  """ % (note, datetime.now(), user.id))

  return redirect('/notes')


@login_required
def user(request, user_id):
  user = User.objects.get(id = user_id)
  content = {'user' : user}
  return render(request, 'user/info.html', content)

@login_required
def search(request):
  search_term = request.POST.get('search_term')
  cursor = sqlite3.connect('db.sqlite3').cursor()

  res = cursor.execute("SELECT notes_note.id, note_text, username, pub_date FROM notes_note LEFT JOIN auth_user ON notes_note.user_id = auth_user.id WHERE note_text LIKE '%%%s%%' " % search_term).fetchall()

  response = []
  for row in res:
    response.append({"id":row[0], "note_text":row[1],  "username":row[2], "pub_date":row[3]})

  content = {'content' : response}
  return render(request, 'notes/search.html', content)


def logout_view(request):
  logout(request)
  return redirect("/notes")

def signup_view(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    psw = request.POST.get('password')
    psw2 = request.POST.get('password_ver')

    if (psw == psw2):
      user = User.objects.create_user(username=username, email=email, password=psw,
        first_name=first_name, last_name=last_name)
      user.save()
      
      user = authenticate(request, username=username, password=psw)
      login(request, user)
      return redirect("/notes")



  return render(request, 'registration/signup.html')