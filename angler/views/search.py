from django.shortcuts import render
from django.views import View
from angler.models.post import Post, Like
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchHeadline
from django.db.models import Q

class SearchView(View): 
    def post(self, request):
        searched = request.POST.get('searched')
        friendslist = request.user.friends
        if searched:
            vector = SearchVector('text', 'user__username', 'user__profile__profile_name')
            query = SearchQuery(searched)
            posts = Post.objects.annotate(search=vector).filter(search=query).annotate(headline_text=SearchHeadline('text', query, start_sel="<mark>", stop_sel="</mark>", highlight_all=True),
                                                                                           headline_username=SearchHeadline('user__username', query, start_sel="<mark>", stop_sel="</mark>", highlight_all=True),
                                                                                               headline_profile_name=SearchHeadline('user__profile__profile_name', query, start_sel="<mark>", stop_sel="</mark>", highlight_all=True)).exclude(is_private=True & ~Q(user__in=friendslist))
        else:   
            posts = None    
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        context = {
            'posts':posts,
            'searched':searched,
            'liked_post_ids':liked_post_ids}
        return render(request, 'angler/search_page.html', context)
    
