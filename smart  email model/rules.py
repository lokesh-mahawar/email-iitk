def classify_email(subject, sender):
    subject = subject.lower()
    sender = sender.lower()

    course_keywords = ["assignment", "quiz", "exam", "lecture", "class", "moodle", "grades", "midsem", "tutorial"]
    general_keywords = ["event", "workshop", "webinar", "invite", "club", "cultural", "sports", "media", "announcement"]

    if any(word in subject for word in course_keywords):
        return "course"
    elif any(word in subject for word in general_keywords):
        return "general"
    elif "@iitk.ac.in" in sender:
        return "general"
    else:
        return "scrap"
