from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Member
from books.models import Book
from bookissue.models import BookIssue
from bookissue.models import BookIssue
from .forms import MemberCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import RestrictedError
# Create your views here.

@login_required(login_url='account:login')
def members_home(request):
    members = Member.objects.all()
    return render(request,'members/index.html',context={'members':members})


@login_required(login_url='account:login')
def add_member(request):
    if request.method == "GET":
        unbounded_form = MemberCreationForm()
        return render(request,'members/addmember.html',context = {
            'form':unbounded_form
        })
    elif request.method == "POST":
        bounded_form = MemberCreationForm(request.POST)
        if bounded_form.is_valid():
            bounded_form.save()
            return render(request,'members/addmember.html',context={
                'message':"Member added successfully",
                'form':MemberCreationForm()
            })
        else:
            return render(request,'members/addmember.html',context={'form':bounded_form})


@login_required(login_url='account:login')
def edit_member(request,id):
    try:
        member = Member.objects.get(id=id)
        if request.method == "GET":
            bounded_form = MemberCreationForm(instance=member)
            return render(request,'members/editmember.html',context={'form':bounded_form,'id':id})
        elif request.method == "POST":
            bounded_form = MemberCreationForm(request.POST,instance=member)
            if bounded_form.is_valid():
                bounded_form.save()
                return redirect('members:index')
            else:
                return render(request,'members/editmember.html',context={'form':bounded_form,'id':id})
    except ObjectDoesNotExist:
        return render(request,'members/editmember',context={'message':"Member with given ID doesn't exist"})


@login_required(login_url='account:login')
def delete_member(request,id):
    try: 
        member = Member.objects.get(id=id)
        if request.method == "GET":
            return render(request,'members/deletemember.html',context={'member':member,'id':id})
        elif request.method == "POST":
            if member.dues>0:
                return render(request,'members/deletemember.html', context={'member':member,'message':"Member cannot be deleted because they have not cleared their dues",'id':id})
            member.delete()
            return redirect('members:index')
    except ObjectDoesNotExist:
        return render(request,'members/deletemember.html',context={'message':"Member with given ID doesn't exist"})
    except RestrictedError:
        return render(request,'members/deletemember.html', context={'member':member,'message':"Member cannot be deleted because they have a book issued to them",'id':id})
    
@login_required(login_url='account:login')
def view_member(request,id):
    try: 
        member = Member.objects.get(id=id)
    except ObjectDoesNotExist:
        return render(request,'members/viewmember.html',context={'message':"Member with given ID doesn't exist"})
    try:
        bookissue = BookIssue.objects.get(member=id)
        fine = (timezone.now()-bookissue.date_created).total_seconds()//86400 - bookissue.for_days
        if fine<0:
            fine=0
        return render(request,'members/viewmember.html',context={'member':member,'bookissue':bookissue,'fine':fine})
    except ObjectDoesNotExist:
        return render(request,'members/viewmember.html',context={'member':member,'issuemessage':"Member has no issued book at present"})

  
@login_required(login_url='account:login')
def pay_fine(request,id):
    try:
        member = Member.objects.get(id=id)
        if request.method == "GET":
            return render(request, 'members/payfine.html', context={'member':member})
        elif request.method == "POST":
            fine = int(request.POST.get('dues',0))
            if fine<0:
                return render(request, 'members/payfine.html', context={'member':member,'message':"Fine cannot be less than 0"})
            if fine>0:
                member.dues = member.dues - fine
                member.save()
            return render(request, 'members/payfine.html', context={'member':member,'message':"Fine payed"})
    except ObjectDoesNotExist:
        return render(request, 'members/payfine.html', context={'message':"Member not found"})


@login_required(login_url='account:login')
def add_penalty(request,id):
    try:
        member = Member.objects.get(id=id)
        if request.method == "GET":
            return render(request, 'members/addpenalty.html', context={'member':member})
        elif request.method == "POST":
            penalty = int(request.POST.get('dues') or 0)
            if penalty<=0:
                return render(request, 'members/addpenalty.html', context={'member':member,'message':"Penalty cannot be less than or equal to 0"})
            if penalty>0:
                member.dues = member.dues + penalty
                member.save()
            return render(request, 'members/addpenalty.html', context={'member':member,'message':"Member penalized"})
    except ObjectDoesNotExist:
        return render(request, 'members/addpenalty.html', context={'message':"Member not found"})

@login_required(login_url='account:login')
def membertobook(request,id):
    try:
        member = Member.objects.get(id=id)
    except ObjectDoesNotExist:
        return render(request, 'members/membertobook.html', context={'message':"Member not found"})
    if request.method == "GET":
        try:
            bookissue = BookIssue.objects.get(member=id)
            return render(request, 'members/membertobook.html', context={'member':member,'message':"Member has the book "+bookissue.book.title+" issued to them."})
        except ObjectDoesNotExist:
            books = Book.objects.all()
            return render(request, 'members/membertobook.html', context={'member':member,'books':books})
    if request.method == "POST":
        if "fetchbook" in request.POST:
            book_id = int(request.POST.get("book_id",0) or 0)
            if book_id != 0:
                book = Book.objects.get(id=book_id)
                return render(request, 'members/membertobook.html', context={'member':member,'books':Book.objects.all(),'book':book})
            else:
                return render(request, 'members/membertobook.html', context={'member':member,'books':Book.objects.all(),'message':"Book not found"})
        elif "issuebook" in request.POST:
            book_id = int(request.POST.get("book_id",0) or 0)
            if book_id != 0:
                try:
                    book = Book.objects.get(id=book_id)
                except ObjectDoesNotExist:
                    return render(request, 'members/membertobook.html', context={'member':member,'books':Book.objects.all(),'message':"Book not found"})
                try:
                    bookissue = BookIssue.objects.get(book=book_id)
                    return render(request, 'members/membertobook.html', context={'member':member,'books':Book.objects.all(),'book':book,'message':"Book is already issued to "+bookissue.member.username+"."})
                except ObjectDoesNotExist:
                    membertobook = BookIssue(member=member,book=book,for_days=request.POST.get("for_days",7))
                    membertobook.save()
                    return render(request, 'members/membertobook.html', context={'member':member,'message':"Member has been issued the book "+book.title})
                    

    

    