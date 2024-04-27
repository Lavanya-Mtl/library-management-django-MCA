from django.shortcuts import render, redirect
from books.models import Book
from members.models import Member
from .models import BookIssue
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='account:login')
def issue_book(request):
    books = Book.objects.all()
    members = Member.objects.all()
    context={'books':books,'members':members}
    if request.method=="GET": 
        return render(request,'bookissue/mainissue.html',context=context)
    elif request.method=="POST":
        book_id = int(request.POST.get("book_id",0))
        member_id = int(request.POST.get("member_id",0))
        if "fetch" in request.POST:
            if book_id!=0:
                book = Book.objects.get(id=book_id)
                context['book']=book
            if member_id!=0:
                member = Member.objects.get(id=member_id)
                context['member']=member
            return render(request,'bookissue/mainissue.html',context=context)
        elif "issuebook" in request.POST:
            if member_id==0:
                context['member_error']="Please select a member"
                return render(request,'bookissue/mainissue.html',context=context)
            if book_id==0:
                context['book_error']="Please select a book"
                return render(request,'bookissue/mainissue.html',context=context)
            #get the member and the book
            member = Member.objects.get(id=member_id)
            book = Book.objects.get(id=book_id)
            context['member']=member
            context['book']=book
            #check if member already has a book issued
            
            try:
                bookissue = member.bookissue
                print(member.username)
                context['member_error']=member.username+" already has issued the book "+bookissue.book.title + " with  book ID " + bookissue.book.book_id
                return render(request,'bookissue/mainissue.html',context=context)
            except Member.bookissue.RelatedObjectDoesNotExist:
                print("hey,getting member's issue list is kinda rude")
            try:
                bookissue = book.bookissue
                context['member_error']=book.title+" has already been issued by "+bookissue.member.username
                return render(request,'bookissue/mainissue.html',context=context)
            except Book.bookissue.RelatedObjectDoesNotExist:
                pass
            if int(request.POST.get("for_days",7))<=0:
                context['issue_error']="Number of days should be greater than 0"
                return render(request,'bookissue/mainissue.html',context=context)
            #check if book is already issued
            #return error in case any of them is true
            #if we reach the end, just issue the book to the person.
            bookissue = BookIssue(member=member,book=book,for_days=request.POST.get("for_days",7))
            bookissue.save()
            context['message']="Book "+book.title+" issued to "+member.username+ " successfully!"
            return render(request,'bookissue/mainissue.html',context=context)


@login_required(login_url='account:login')            
def return_book(request):
    if request.method == "GET":
        members = Member.objects.all()
        books = Book.objects.all()
        context = {'books':books,'members':members}
        return render(request,'bookissue/return.html',context=context)
    elif request.method == "POST":
        if 'search_book' in request.POST:
            members = Member.objects.all()
            books = Book.objects.all()
            context = {'books':books,'members':members}
            try:
                issue = BookIssue.objects.get(book=request.POST['book_id'])
                fine = (timezone.now()-issue.date_created).total_seconds()//86400 - issue.for_days
                if fine<0:
                    fine=0
                context['issue'] = issue
                context['fine'] = fine
            except ObjectDoesNotExist:
                context['message']='This book has not been issued by anyone yet.'
            return render(request,'bookissue/return.html',context=context)
        elif 'search_member' in request.POST:
            members = Member.objects.all()
            books = Book.objects.all()
            context = {'books':books,'members':members}
            try:
                issue = BookIssue.objects.get(member=request.POST['member_id'])
                fine = (timezone.now()-issue.date_created).total_seconds()//86400 - issue.for_days
                if fine<0:
                    fine=0
                context['issue'] = issue
                context['fine'] = fine
            except ObjectDoesNotExist:
                context['message']='This member has not been issued any book.'
            return render(request,'bookissue/return.html',context=context)
        elif 'fine_unpaid' in request.POST:
            try:
                issue = BookIssue.objects.get(id=request.POST['fine_unpaid'])
                fine = (timezone.now()-issue.date_created).total_seconds()//86400 - issue.for_days
                if fine>0:
                    print("Non zero fine.check member")
                    issue.member.dues = issue.member.dues + fine
                    issue.member.save()
                issue.delete()
                return render(request,'bookissue/return.html',context={'message':'Book returned successfully','books':Book.objects.all(),'members':Member.objects.all()})
            except ObjectDoesNotExist:
                return render(request,'bookissue/return.html',context={'message':'Data on issuing the book to the member not found','books':Book.objects.all(),'members':Member.objects.all()})
        elif 'paid' in request.POST:
            try:
                issue = BookIssue.objects.get(id=request.POST['paid'])
                return render(request,'bookissue/return.html',context={'message':'Book returned successfully','books':Book.objects.all(),'members':Member.objects.all()})
            except ObjectDoesNotExist:
                return render(request,'bookissue/return.html',context={'message':'Data on issuing the book to the member not found'})
        

@login_required(login_url='account:login')
def index(request):
    bookissues = BookIssue.objects.all()
    return render(request,'bookissue/index.html', context= {
        'bookissues':bookissues
    })

@login_required(login_url='account:login')
def view(request,bookissueid):
    try:
        bookissue = BookIssue.objects.get(id=bookissueid)
        fine = (timezone.now()-bookissue.date_created).total_seconds()//86400 - bookissue.for_days
        if fine<0:
            fine=0
    except ObjectDoesNotExist:
        return render(request,'bookissue/view.html',context={'message':'Data entry not found: Book has been returned by member'}) 
    
    if request.method == "GET":
        return render(request,'bookissue/view.html',context={
            'bookissue': bookissue,
            'fine':fine
        })
    elif request.method == "POST":
        if 'fine_unpaid' in request.POST:
            print("return without paying fine")
            fine = (timezone.now()-bookissue.date_created).total_seconds()//86400 - bookissue.for_days
            if fine>0:
                print("Non zero fine.check member")
                bookissue.member.dues = bookissue.member.dues + fine
                bookissue.member.save()
        bookissue.delete()   
        return redirect('bookissue:index')
    