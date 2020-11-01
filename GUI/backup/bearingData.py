from path import dateinfoPath


### date information ###
def bearingFileInfo():
    datefile = open(dateinfoPath + 'dateinfo', "r")
    datelist_tmp = []
    timedict = {}
    for line in datefile:
        date, time = line.split('_')
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