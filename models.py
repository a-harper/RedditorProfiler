from django.db import models

# Create your models here.


class Redditor(models.Model):
    username = models.CharField(max_length=70)
    profile_url = models.CharField(max_length=150)
    last_updated = models.DateTimeField()

    def __unicode__(self):
        return self.username


class Status(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.description


class RedditorStatus(models.Model):
    redditor = models.ForeignKey(Redditor)
    status = models.ForeignKey(Status)

    def __unicode__(self):
        return self.status.description


class Subreddit(models.Model):
    name = models.CharField(max_length=100)
    over_18 = models.BooleanField()
    flagged = models.BooleanField(default=False)
    moderators = models.ManyToManyField(Redditor)

    def __unicode__(self):
        return self.name


class Submission(models.Model):
    submission_id = models.CharField(max_length=20)
    permalink = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    over_18 = models.BooleanField()
    redditor = models.ForeignKey(Redditor, null=True)
    subreddit = models.ForeignKey(Subreddit)
    score = models.IntegerField(default=0)
    submission_date = models.DateTimeField()

    def __unicode__(self):
        return self.title


class InterestingWord(models.Model):
    word = models.CharField(max_length=50)

    def __unicode__(self):
        return self.word


class WordCategory(models.Model):
    category_name = models.CharField(max_length=50)
    words = models.ManyToManyField(InterestingWord)

    def __unicode__(self):
        return self.category_name


class Comment(models.Model):
    comment_id = models.CharField(max_length=20)
    permalink = models.CharField(max_length=200)
    redditor = models.ForeignKey(Redditor)
    submission = models.ForeignKey(Submission)
    body = models.CharField(max_length=10000)
    controversiality = models.IntegerField(default=0)
    gilded = models.BooleanField()
    score = models.IntegerField(default=0)
    comment_date = models.DateTimeField()

    def __unicode__(self):
        return self.permalink


class BadComment(models.Model):
    comment = models.ForeignKey(Comment)
    words = models.ManyToManyField(InterestingWord)

    def __unicode__(self):
        return self.comment.body
