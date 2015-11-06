=====
RedditorProfiler
=====

RedditorProfiler is a Django app to build a profile of a given redditor.

The app will loop through all of a redditor's submissions and comments, and give a webpage output
showing the user's best and worst comments, and any comments with words flagged as "bad".

Quick start
-----------

Make sure you have the required packages & django apps. RedditorProfiler requires PRAW, urllib and Celery

1. Add "RedditorProfiler" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'RedditorProfiler',
    )

2. Include the RedditorProfiler URLconf in your project urls.py like this::

    url(r'^redditor/', include('RedditorProfiler.urls', namespace="RedditorProfiler")),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to add to the list of "interesting" words & add their categories.
   
5. Start the celery worker (e.g. celery -a djangoapps worker -l info)

6. Visit http://127.0.0.1:8000/polls/ to participate in the poll.
