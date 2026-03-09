from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Outpass

# Create your views here.

@login_required
def apply_outpass(request):

    if request.method == 'POST':

        from_date = request.POST.get('from_date')
       # out_time = request.POST.get('out_time')
        to_date = request.POST.get('to_date')
        #in_time = request.POST.get('in_time')
        reason = request.POST.get('reason')
        parent_phone = request.POST.get('parent_phone')

        Outpass.objects.create(
            student=request.user,
            from_date=from_date,
            
            to_date=to_date,
           
            reason=reason,
            parent_phone=parent_phone,
        )

        return redirect('student_homepage')

    return render(request, 'apply_outpass.html')


def outpass_list(request):

    outpasses = Outpass.objects.all().order_by('-created_at')

    return render(
        request,
        'outpass_list.html',
        {'outpasses':outpasses}
    )


def approve_outpass(request,id):

    outpass = get_object_or_404(Outpass,id=id)

    outpass.status = "approved"

    outpass.save()

    return redirect('outpass_list')


def reject_outpass(request,id):

    outpass = get_object_or_404(Outpass,id=id)

    outpass.status = "rejected"

    outpass.save()

    return redirect('outpass_list')

@login_required
def my_outpasses(request):

    outpasses = Outpass.objects.filter(
        student=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_outpass.html',
        {'outpasses': outpasses}
    )

def download_outpass(request, id):

    outpass = Outpass.objects.get(id=id)

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="outpass.txt"'

    response.write(f"Outpass\n\nReason: {outpass.reason}\nFrom: {outpass.from_date}\nTo: {outpass.to_date}")

    return response

