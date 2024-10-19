from datetime import datetime

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import NotesTaking


# Create your views here.
def index_page(request):
    srch = request.GET.get("search")
    notes_count = 0
    if srch:
        notes = NotesTaking.objects.filter(
            Q(heading=srch) | Q(description=srch))
        notes_count = notes.count()

        if notes_count == 0:
            notes = NotesTaking.objects.all()
            notes_count = notes.count()
            return HttpResponse("""
                <script>
                alert("No such datas found !");
                window.history.back()
                </script>
            """)

    else:
        notes = NotesTaking.objects.all()
        notes_count = notes.count()
    return render(request,"MyAppHTML/index.html",context={'notes':notes})

def add_notes(request):

    try:
        notes_time=None
        if request.method == 'POST':
            heading = request.POST['heading']
            description = request.POST['description']
            current_datetime = datetime.now()
            notes = NotesTaking(heading=heading, description=description,modified_date=current_datetime)
            notes.save()

            return HttpResponse("""
                            <script>
                            alert("Your notes was saved !");
                            window.location.href = '';
                            </script>
                            """)
    except Exception as e:
        return HttpResponse("""
                <script>
                alert("Please Enter All Datas !");
                window.history.back()
                </script>
                """)
    return render(request,"MyAppHTML/addNotes.html")

def deleteNotes(request,id):
    notes = NotesTaking.objects.get(id=id)
    if request.method == "POST":
        notes.delete()
        return HttpResponse("""
                        <script>
                        alert("Successfully Deleted !");
                        window.location.href = 'http://127.0.0.1:8000/'; 
                        </script>
                        """)

    # emp.delete()
    return render(request, "MyAppHTML/deleteNotes.html", context={"heading": notes.heading})


def updateNotes(request,id):
    notes = NotesTaking.objects.get(id=id)
    if request.method == "POST":
        data=request.POST
        heading_data = data.get('heading')
        description_data = data.get('description')

        if heading_data and description_data:
            notes.heading=heading_data
            notes.description=description_data
            current_datetime = datetime.now()
            notes.modified_date = current_datetime

            notes.save()
            return HttpResponse("""
                <script>
                alert("Successfully Modified !");
                window.location.href = 'http://127.0.0.1:8000/'; 
                </script>
                """)


    return render(request, "MyAppHTML/updateNotes.html", context={"notes": notes})


def viewNotes(request,id):
    notes = NotesTaking.objects.get(id=id)


    return render(request, "MyAppHTML/viewNotes.html", context={"notes": notes})