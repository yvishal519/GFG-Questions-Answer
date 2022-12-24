def calendarMatching(calendar1, daily_bounds1, calendar2, daily_bounds2, meetingDuration):
    updated_calendar_1 = updateCalendar(calendar1, daily_bounds1)
    updated_calendar_2 = updateCalendar(calendar2, daily_bounds2)
    merged_calendar = mergeCalendars(updated_calendar_1, updated_calendar_2)
    flattened_calendar = flattenCalendar(merged_calendar)
    return getmatching_availabilities(flattened_calendar, meetingDuration)

def updateCalendar(calendar, daily_bounds):
    updated_calendar = calendar[:]
    updated_calendar.insert(0, ["0:00", daily_bounds[0]])
    updated_calendar.append([daily_bounds[1], "23:59"])
    return list(map(lambda m: [timetoMinutes(m[0]), timetoMinutes(m[1])], updated_calendar))

def mergeCalendars(calendar1, calendar2):
    merged = []
    i, j = 0, 0
    while i < len(calendar1) and j < len(calendar2):
        meeting_1, meeting_2 = calendar1[i], calendar2[j]
        if meeting_1[0] < meeting_2[0]:
            merged.append(meeting_1)
            i += 1
        else:
            merged.append(meeting_2)
            j += 1
    while i < len(calendar1):
        merged.append(calendar1[i])
        i += 1
    while j < len(calendar2):
        merged.append(calendar2[j])
        j += 1
    return merged

def flattenCalendar(calendar):
    flattened = [calendar[0][:]]
    for i in range(1, len(calendar)):
        current_meeting = calendar[i]
        previous_meeting = flattened[-1]
        current_start, current_end = current_meeting
        previous_start, previous_end = previous_meeting
        if previous_end >= current_start:
            newprevious_meeting = [previous_start, max(previous_end, current_end)]
            flattened[-1] = newprevious_meeting
        else:
            flattened.append(current_meeting[:])
    return flattened

def getmatching_availabilities(calendar, meetingDuration):
    matching_availabilities = []
    for i in range(1, len(calendar)):
        start = calendar[i - 1][1]
        end = calendar[i][0]
        availabilit_duration = end - start
        if availabilit_duration >= meetingDuration:
            matching_availabilities.append([start, end])
    return list(map(lambda m: [minutestoTime(m[0]), minutestoTime(m[1])], matching_availabilities))

def timetoMinutes(time):
    hours, minutes = list(map(int, time.split(":")))
    return hours * 60 + minutes

def minutestoTime(minutes):
    hours = minutes // 60
    mins = minutes % 60
    hoursString = str(hours)
    minutesString = "0" + str(mins) if mins < 10 else str(mins)
    return hoursString + ":" + minutesString
    
calendar1 = [['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
dailyBounds1 = ['9:00', '20:00']
calendar2 = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
dailyBounds2 = ['10:00', '18:30']
meetingDuration = 30    
print(calendarMatching(calendar1,dailyBounds1,calendar2,dailyBounds2,meetingDuration))