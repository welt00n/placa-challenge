import datetime
from tkinter import W
from django.http import HttpResponse
from django.shortcuts import redirect, render
from interview.models import Interviewee
import gpt

import logging
logger = logging.getLogger("django")

LOCAL_ASSISTANT_ID = gpt.get_new_assistant().id
def index(request):
    return render(
        request,
        "interview/index.html",
        {"interviewees": Interviewee.objects.order_by("created_at")}
    )

def start_interview(request):
    return redirect('chat', gpt.get_new_thread().id)

def submit_message(request):
    gpt.create_new_message(request.POST.get("thread_id"), request.POST.get("message"))
    return redirect('chat', request.POST.get("thread_id"))

def chat(request, thread_id):
    messages = gpt.run_thread(thread_id, LOCAL_ASSISTANT_ID)
    result = gpt.get_result(gpt.get_raw_messages(thread_id))
    finished = "disabled" if result else ""

    if result:
        create_new_interviewee(result)

    return render(
        request,
        "interview/chat.html",
        {
            "messages":messages,
            "thread_id": thread_id,
            "finished": finished
        }
    )

def create_new_interviewee(data):
    new_interviewee = Interviewee(
        name=data.get("name"),
        years_of_experience=data.get("years_of_experience"),
        favorite_programming_language=data.get("favorite_programming_language"),
        interview_date=data.get("interview_date"),
        willing_to_work_onsite=data.get("willing_to_work_onsite"),
        willing_to_use_ruby=data.get("willing_to_use_ruby"),
        created_at=datetime.datetime.now()
    )
    new_interviewee.save()