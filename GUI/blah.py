import commands
break_loop = 0
while 1:
    lines = commands.getoutput("wmctrl -l").split("\n")
    for line in lines:
        line = line.replace("  ", " ")
        win = tuple(line.split(" ", 3))
        if 'gst-launch-0.10' in win[3]:
            break_loop = 1;
    if break_loop == 1:
        break
    else:
        print "gst-launch not yet opened"
print "launched!"
