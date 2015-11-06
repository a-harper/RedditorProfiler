from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
import time
from operator import itemgetter
from datetime import datetime, timedelta
from django.db.models import Count
import praw

# Create your views here.

from .models import Redditor, Submission, Subreddit, Comment, Status, RedditorStatus, BadComment
from tasks import write_user, update_user


def index(request):
    not_pending = RedditorStatus.objects.filter(status__gt=10)
    recently_updated = RedditorStatus.objects.filter(status__gt=1).order_by('-redditor__last_updated')[:10]
    if request.method == 'POST':
        username = str(request.POST['username'])
        return HttpResponseRedirect(reverse('RedditorProfiler:redditor', args=(username,)))
    return render(request, 'RedditorProfiler/index.html', {'recently_updated': recently_updated})


def redditor(request, username):
    r = praw.Reddit('Statistics bot by /u/filthyneckbeard')
    context = {'error_message': "Wat"}
    template = 'RedditorProfiler/redditor.html'
   # try:
    user = r.get_redditor(username)
    num_results = Redditor.objects.filter(username=username).count()
    if num_results == 0:
        write_user.delay(user)
        time.sleep(1)
        the_bloke = Redditor.objects.get(username=username)
        update_user.delay(the_bloke)
        time.sleep(1)
        return render(request, 'RedditorProfiler/redditor.html', {'error_message': username +
                                                                        " is being updated."})
    else:
        the_bloke = Redditor.objects.get(username=username)
        status = RedditorStatus.objects.get(redditor=the_bloke)
        if status.status_id == 1 or the_bloke.last_updated < (timezone.now() - timedelta(days=1)):
            update_user.delay(the_bloke)
            time.sleep(1)
            return render(request, 'RedditorProfiler/redditor.html', {'error_message': username +
                                                                        " is being updated.",
                                                                      'redditor': username})
        # if status.status_id < 30:
            # return render(request, 'RedditorProfiler/redditor.html', {'error_message': username +
            #                                                            " status: " + status.status.description,
            #                                                          'redditor': username})
        else:
            info_message = None
            if status.status_id < 30:
                info_message = the_bloke.username + " is currently being updated (" + status.status.description + \
                    "). This data is subject to change"

            template = 'RedditorProfiler/redditorinfo.html'
            top_submissions = Submission.objects.filter(redditor=the_bloke).order_by('-score')[:5]
            top_comments = Comment.objects.filter(redditor=the_bloke).order_by('-score')[:5]
            submissions = Submission.objects.filter(redditor=the_bloke)
            comments = Comment.objects.filter(redditor=the_bloke)
            worst_comments = Comment.objects.filter(redditor=the_bloke).order_by('score')[:5]
            nsfw_posts = Submission.objects.filter(redditor=the_bloke, over_18=True)
            nsfw_comments = Comment.objects.filter(redditor=the_bloke, submission__over_18=True)
            badword_comments = BadComment.objects.filter(comment__redditor=the_bloke)
            sublist = []
            subreddits = Subreddit.objects.all()
            for sub in subreddits:
                posts = submissions.filter(subreddit=sub)
                coms = comments.filter(submission__subreddit=sub)
                count = 0
                if len(coms) > 0:
                    count += len(coms)
                if len(posts) > 0:
                    count += len(posts)
                subname = sub.name
                if count > 0:
                    sublist.append((subname, count, sub.flagged))
            sublist.sort(key=itemgetter(2))
            sublist.sort(key=itemgetter(1))
            sublist.reverse()

            context = {'top_submissions': top_submissions, 'top_comments': top_comments,
                       'sublist': sublist,
                       'redditor': the_bloke, 'worst_comments': worst_comments, 'nsfw_posts': nsfw_posts,
                       'nsfw_comments': nsfw_comments, 'badword_comments': badword_comments,
                       'info_message': info_message}

   # except:
    #    return render(request, 'RedditorProfiler/redditor.html', {'error_message': "No user found"})

    return render(request, template, context)


def subreddits(request, username, subreddit):
    bloke = Redditor.objects.get(username=username)
    submissions = Submission.objects.filter(redditor=bloke).filter(subreddit__name=subreddit).order_by('-score')
    comments = Comment.objects.filter(redditor=bloke).filter(submission__subreddit__name=subreddit).order_by('-score')
    sublink = "/r/" + subreddit
    context = {'redditor': bloke, 'submissions': submissions, 'comments': comments, 'sub': subreddit, 'sublink': sublink}

    return render(request, 'RedditorProfiler/subreddits.html', context)