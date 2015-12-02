import praw
from .models import Redditor, RedditorStatus, Status, Subreddit, Comment, Submission, InterestingWord, WordCategory, \
    BadComment
import json
from urllib import FancyURLopener
import calendar, datetime
import re


def get_comments(redditor):
    update_user_status(redditor, 20)
    r = praw.Reddit('Statistics bot by /u/filthyneckbeard')
    user = r.get_redditor(redditor.username)
    comments = user.get_comments(limit=None)
    for comment in comments:
        num_results = Subreddit.objects.filter(name=comment.subreddit.display_name).count()
        if num_results == 0:
            create_subreddit(comment.subreddit)
        num_post_results = Comment.objects.filter(comment_id=comment.id).count()
        if num_post_results == 0:
            user_comment = Comment()
            save = 1
            try:
                user_comment.submission = get_submission(str(comment.link_id.split('_')[1]))
            except:
                save = 0
            user_comment.body = comment.body
            user_comment.comment_date = datetime.datetime.utcfromtimestamp(comment.created_utc)
            user_comment.comment_id = comment.id
            user_comment.controversiality = comment.controversiality
            user_comment.gilded = comment.gilded
            if save == 1:
                try:
                    user_comment.permalink = get_submission(str(comment.link_id.split('_')[1])).permalink + comment.id
                except:
                    save = 0
            else:
                user_comment.permalink = "lol"
            user_comment.redditor = Redditor.objects.get(username=comment.author.name)
            user_comment.score = comment.score
            if save == 1:
                user_comment.save()

            for word in InterestingWord.objects.all():
                if find_whole_word(word)(comment.body):
                    bad_comment = BadComment()
                    bad_comment.comment = user_comment
                    bad_comment.save()
                    bad_comment.words.add(word)


def find_whole_word(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def get_submission(submission_id):
    r = praw.Reddit('Statistics bot by /u/filthyneckbeard')
    submission = r.get_submission(submission_id=submission_id)
    num_results = Subreddit.objects.filter(name=submission.subreddit.display_name).count()
    if num_results == 0:
        create_subreddit(submission.subreddit)
    try:
        author_name = submission.author.name
    except AttributeError:
        author_name = None
    if author_name is not None:
        num_redditor_results = Redditor.objects.filter(username=author_name).count()
        if num_redditor_results == 0:
            create_user(submission.author)
    num_post_results = Submission.objects.filter(submission_id=submission.id).count()
    if num_post_results == 0:
        user_submission = Submission()
        user_submission.over_18 = submission.over_18
        if author_name is not None:
            user_submission.redditor = Redditor.objects.get(username=submission.author.name)
        user_submission.score = submission.score
        user_submission.permalink = submission.permalink
        user_submission.submission_id = submission.id
        user_submission.subreddit = Subreddit.objects.get(name=submission.subreddit.display_name)
        user_submission.title = submission.title
        user_submission.url = submission.url
        user_submission.submission_date = datetime.datetime.utcfromtimestamp(submission.created_utc)
        user_submission.save()
        return user_submission
    else:
        user_submission = Submission.objects.get(submission_id=submission.id)
        return user_submission


def get_submissions(redditor):
    update_user_status(redditor, 10)
    r = praw.Reddit('Statistics bot by /u/filthyneckbeard')
    user = r.get_redditor(redditor.username)
    submissions = user.get_submitted(limit=None)
    for submission in submissions:
        num_results = Subreddit.objects.filter(name=submission.subreddit.display_name).count()
        if num_results == 0:
            create_subreddit(submission.subreddit)
        num_post_results = Submission.objects.filter(submission_id=submission.id).count()
        if num_post_results == 0:
            user_submission = Submission()
            user_submission.over_18 = submission.over_18
            user_submission.redditor = redditor
            user_submission.score = submission.score
            user_submission.permalink = submission.permalink
            user_submission.submission_id = submission.id
            user_submission.subreddit = Subreddit.objects.get(name=submission.subreddit.display_name)
            user_submission.title = submission.title
            user_submission.url = submission.url
            user_submission.submission_date = datetime.datetime.utcfromtimestamp(submission.created_utc)
            user_submission.save()


def create_subreddit(subreddit):
    sub = Subreddit()
    sub.name = subreddit.display_name
    myopener = MyOpener()
    page = (myopener.open('http://www.reddit.com/r/' + sub.name + '/about.json'))
    stuff = page.read()
    the_dict = json.loads(stuff)
    sub.over_18 = the_dict['data']['over18']
    sub.flagged = False
    sub.save()
    for user in subreddit.get_moderators():
        if Redditor.objects.filter(username=user.name).count() < 1:
            create_user(user)
        mod = Redditor.objects.get(username=user.name)
        sub.moderators.add(mod)
        sub.save()


def create_user(user):
    bloke = Redditor()
    bloke.profile_url = "http://reddit.com/u/" + user.name
    bloke.username = user.name
    bloke.last_updated = datetime.datetime.utcnow()
    bloke.save()

    bloke_status = RedditorStatus()
    bloke_status.redditor = bloke
    status = Status.objects.get(id=1)
    bloke_status.status = status
    bloke_status.save()


def update_user_status(redditor, status_id):
    bloke_status = RedditorStatus.objects.get(redditor=redditor)
    new_status = Status.objects.get(id=status_id)
    bloke_status.status = new_status
    bloke_status.save()
    if status_id == 30:
        redditor.last_updated = datetime.datetime.utcnow()
        redditor.save()


class MyOpener(FancyURLopener):
    version = 'Helper opener for bot by /u/filthyneckbeard'