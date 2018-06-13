from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

from .forms import PostModelForm, CommentForm
from .models import PostModel


#@login_required
def post_model_create_view(request):
    form = PostModelForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        messages.success(request, "Đã tạo một bài đăng internet mới!")
        context = {
            "form": PostModelForm()
        }
    
    template = "internet/post.html"
    return render(request, template, context)

#@login_required
def post_model_update_view(request, id=None):
    obj = get_object_or_404(PostModel, id=id)
    form = PostModelForm(request.POST or None, instance=obj)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Đã cập nhật bài đăng!")
        return HttpResponseRedirect("/internet/{num}".format(num=obj.id))
    
    template = "internet/update.html"
    return render(request, template, context)


def post_model_detail_view(request, id=None):
    obj = get_object_or_404(PostModel, id=id)
    context = {
        "object": obj,
    }
    template = "internet/detail.html"
    return render(request, template, context)



def post_model_delete_view(request, id=None):
    obj = get_object_or_404(PostModel, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Đã xóa bài đăng")
        return HttpResponseRedirect("/internet/")
    context = {
        "object": obj,
    }
    template = "internet/delete.html"
    return render(request, template, context)


def post_model_list_view(request):
    query = request.GET.get("q", None)
    qs = PostModel.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(slug__icontains=query)
                )
    context = {
        "object_list": qs,
    }
    template = "internet/internet.html"
    return render(request, template, context)



@login_required(login_url='/login/')
def login_required_view(request):
    print(request.user)
    qs = PostModel.objects.all()
    context = {
        "object_list": qs,
    }

    if request.user.is_authenticated():
        template = "internet/internet.html"
    else:
        template = "internet/list-view-public.html"
        #raise Http404
        return HttpResponseRedirect("/login")
    
    return render(request, template, context)




def post_model_robust_view(request, id=None):
    obj = None
    context =  {}
    success_message = 'Một bài đăng mới đã được tạo'
    
    if id is None:
        "obj có thể được tạo ra"
        template = "internet/post.html"
    else:
        "obj prob exists"
        obj = get_object_or_404(PostModel, id=id)
        success_message = 'Một bài đăng mới đã được tạo'
        context["object"] = obj
        template = "internet/detail.html"
        if "edit" in request.get_full_path():
            template = "internet/update.html"
        if "delete" in request.get_full_path():
            template = "internet/delete.html"
            if request.method == "POST":
                obj.delete()
                messages.success(request, "Đã xóa bài đăng")
                return HttpResponseRedirect("/internet/")

    #if "edit" in request.get_full_path() or "create" in request.get_full_path():
    form = PostModelForm(request.POST or None, instance=obj)
    context["form"] = form
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, success_message)
        if obj is not None:
            return HttpResponseRedirect("/internet/{num}".format(obj.id))
        context["form"] - PostModelForm()
    return render(request, template, context)

def comments(request, id):
    post = get_object_or_404(PostModel, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST, author=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = form.author
            comment.save()
            return redirect('internet:detail', id=post.id)
    else:
        form = CommentForm()
        return render(request, 'internet/comments.html', {"form":form})