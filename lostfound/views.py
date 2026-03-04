from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import LostItem


# ===============================
# HOME / VIEW ITEMS
# ===============================
@login_required
def home(request):

    items = LostItem.objects.all().order_by('-id')

    return render(
        request,
        'lostfound/lost_items.html',
        {'items': items}
    )


# ===============================
# ADD LOST / FOUND ITEM
# ===============================
@login_required
def add_item(request):

    if request.method == "POST":

        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        image = request.FILES.get('image')

        LostItem.objects.create(
            user=request.user,
            title=title,
            description=description,
            status=status,
            image=image
        )

        return redirect('lostfound_home')

    return render(request, 'lostfound/add_item.html')


# ===============================
# CLAIM ITEM
# ===============================
@login_required
def claim_item(request, id):

    item = LostItem.objects.get(id=id)

    # Prevent owner claiming own post
    if item.user == request.user:
        return redirect('lostfound_home')

    item.status = "claimed"
    item.claimed_by = request.user
    item.save()

    return redirect('lostfound_home')

@login_required
def request_claim(request, id):

    item = LostItem.objects.get(id=id)

    if item.user != request.user:
        item.claim_requested_by = request.user
        item.save()

    return redirect('lostfound_home')

@login_required
def approve_claim(request, id):

    item = LostItem.objects.get(id=id)

    if item.user == request.user:
        item.status = "claimed"
        item.claimed_by = item.claim_requested_by
        item.claim_requested_by = None
        item.save()

    return redirect('lostfound_home')