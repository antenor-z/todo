from datetime import datetime
def human_deadline(deadline):
    if deadline == "":
        return "no deadline"
    
    deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()

    ret = []

    delta = abs(deadline - now)
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds // 60) % 60

    if days > 1: 
        ret.append(f"{days} days")
    elif days == 1:
        ret.append("a day")
    
    if days <= 2:
        if hours > 1: 
            ret.append(f"{hours} hours")
        elif hours == 1:
            ret.append("an hour")

    if days <= 2 and hours <= 5:
        if minutes > 1: 
            ret.append(f"{minutes} minutes")
        elif minutes == 1:
            ret.append("a minute")

    if len(ret) > 1:
        ret.insert(len(ret) - 1, "and")
    if len(ret) > 3:
        ret.insert(1, ", ")

    
    if deadline >= now:
        ret.append("left")
    else:
        ret.insert(0, "deadline expired")
        ret.append("ago")

    return " ".join(ret).replace(" , ", ",")
