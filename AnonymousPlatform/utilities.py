
def determine_tag(conversation):
    for i in conversation:
        if i.tag == "1":
            i.tag = "工作"
        elif i.tag == "2":
            i.tag = "加薪"
        elif i.tag == "3":
            i.tag = "餐饮"
        elif i.tag == "4":
            i.tag = "告白"
        elif i.tag == "5":
            i.tag = "老板"
        elif i.tag == "6":
            i.tag = "摸鱼"
