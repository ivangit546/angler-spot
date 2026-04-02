from django.shortcuts import redirect, render
from django.views import View
from angler.models.post import Post, Like


class SearchView(View):  #TODO will switch to postgres to implement fully functional search engine 
    def post(self, request):
        searched = request.POST.get('searched')
        if searched == '':
            posts = Post.objects.none()
        else:
            posts = Post.objects.filter(text__contains=searched)
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        context = {
            'posts':posts,
            'searched':searched,
            'liked_post_ids':liked_post_ids}
        return render(request, 'angler/search_page.html', context)
    
