import config


### date information ###
def bearingFileInfo():
    datefile = open(config.DatabaseInfoPath + 'dateinfo', "r")
    datelist_tmp = []
    timedict = {}
    for line in datefile:
        date, time = line.split('_')
        date = date.rstrip()
        time = time.rstrip()
        if date in datelist_tmp:
            timedict[date].append(time)
        else:
            datelist_tmp.append(date)
            timedict[date] = [time]
    
    datelist = []
    for date in datelist_tmp:
        datelist.append({'label':date, 'value':date})
    
    datefile.close()

    return datelist, timedict
