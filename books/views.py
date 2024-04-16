from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Book
from members.models import Member
from django.utils import timezone
from bookissue.models import BookIssue
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import RestrictedError
# Create your views here.
@login_required(login_url='account:login')
def books_home(request):
    books = Book.objects.all()
    return render(request,'books/index.html', context={'books':books})

@login_required(login_url='account:login')
def add_book(request):
    if request.method == "GET":
        unbounded_form = BookCreationForm()
        return render(request,'books/addbook.html',context={
            'form': unbounded_form
        })
    elif request.method == "POST":
        bounded_form = BookCreationForm(request.POST)
        if bounded_form.is_valid():
            bounded_form.save()
            return render(request, 'books/addbook.html', context={'message':'Book added successfully','form':BookCreationForm()})
        else:
            return render(request, 'books/addbook.html', context={'form':bounded_form})

       
@login_required(login_url='account:login')
def edit_book(request,id):
    try:
        book = Book.objects.get(id=id)
        if request.method == "GET":
            book_form = BookCreationForm(instance=book)
            return render(request,'books/editbook.html',context={'form':book_form,'id':id})
        elif request.method == "POST":
            edited_form = BookCreationForm(request.POST,instance=book)
            if edited_form.is_valid():
                edited_form.save()
                return redirect('books:index')
            else:
                return render(request,'books/editbook.html',context={'form':edited_form,'id':id})
    except ObjectDoesNotExist:
        return render(request,'books/editbook.html',context={'message':"Book doesn't exist"})

@login_required(login_url='account:login')
def delete_book(request,id):
    try:
        book = Book.objects.get(id=id)
        if request.method == "GET":
            return render(request,'books/deletebook.html',context={'book':book})
        elif request.method == "POST":
            book.delete()
            return redirect('books:index')
            
    except ObjectDoesNotExist:
        return render(request,'books/deletebook.html',context={'message':"Book with given id doesn't exist"})
    except RestrictedError:
        return render(request,'books/deletebook.html',context={'book':book,'message':"Book cannot be deleted because it is issued to a member"})

@login_required(login_url='account:login')
def view_book(request,id):
    try:
        book = Book.objects.get(id=id)
    except ObjectDoesNotExist:
        return render(request, 'books/viewbook.html', context={'message':"Book not found"})
    try:
        bookissue = BookIssue.objects.get(book=book.id)
        fine = (timezone.now()-bookissue.date_created).total_seconds()//86400 - bookissue.for_days
        if fine<0:
            fine=0
        return render(request, 'books/viewbook.html', context={'book':book,'bookissue':bookissue,'fine':fine})
    except ObjectDoesNotExist:
        return render(request, 'books/viewbook.html', context={'book':book,'issuemessage':"This book has not been issued to any member"})
    
@login_required(login_url='account:login')
def booktomember(request,id):
    try:
        book = Book.objects.get(id=id)
    except ObjectDoesNotExist:
        return render(request, 'books/booktomember.html', context={'message':"Book not found"})
    if request.method == "GET":
        try:
            bookissue = BookIssue.objects.get(book=id)
            return render(request, 'books/booktomember.html', context={'book':book,'message':"The book has already been issued by "+bookissue.member.username+"."})
        except ObjectDoesNotExist:
            members = Member.objects.all()
            return render(request, 'books/booktomember.html', context={'members':members,'book':book})
    if request.method == "POST":
        if "fetchmember" in request.POST:
            member_id = int(request.POST.get("member_id",0) or 0)
            if member_id != 0:
                member = Member.objects.get(id=member_id)
                return render(request, 'books/booktomember.html', context={'member':member,'members':Member.objects.all(),'book':book})
            else:
                return render(request, 'books/booktomember.html', context={'book':book,'members':Member.objects.all(),'message':"Member not found"})
        elif "issuebook" in request.POST:
            member_id = int(request.POST.get("member_id",0) or 0)
            if member_id != 0:
                try:
                    member = Member.objects.get(id=member_id)
                except ObjectDoesNotExist:
                    return render(request, 'books/booktomember.html', context={'members':Member.objects.all(),'book':book,'message':"Member not found"})
                try:
                    bookissue = BookIssue.objects.get(member=member_id)
                    return render(request, 'books/booktomember.html', context={'member':member,'members':Member.objects.all(),'book':book,'message':"Member already has the book "+bookissue.book.title+" issued to them."})
                except ObjectDoesNotExist:
                    membertobook = BookIssue(member=member,book=book,for_days=request.POST.get("for_days",7))
                    membertobook.save()
                    return render(request, 'books/booktomember.html', context={'book':book,'message':"Book has been issued to the member "+member.username})
                    

    

    