import csv
import copy

rawdata = []
with open("data/decimal_log.csv","r") as file:
    reader = csv.reader(file)

    for row in reader:
        rawdata.append(row)
print("loaded")

users = {}
streaks = [{'user': '', 'timestamp': -1, 'length': 0, 'start': '', 'end': '', 'thread': ''},{'user': '', 'timestamp': -1, 'length': 0, 'start': '', 'end': '', 'thread': ''}] #odd, even
max_streaks = {}

for x in range(4,len(rawdata)-1):
    if x % 100000 == 0:
        print(x)
    count, user, timestamp, commentid, threadid = rawdata[x]
    prev_count, prev_user, prev_timestamp, prev_commentid, prev_threadid = rawdata[x-1]
    reply_time = int(float(timestamp) - float(prev_timestamp))
    if int(count) % 2 == 1:
        streak = streaks[0]
    else:
        streak = streaks[1]

    if user == streak['user'] and reply_time == streak['timestamp']:
        streak['length'] += 1
    else:
        streak['end'] = commentid
        if str(streak['timestamp']) not in max_streaks:
            max_streaks[str(streak['timestamp'])] = copy.deepcopy(streak)
        else:
            if max_streaks[str(streak['timestamp'])]['length'] < streak['length']:
                max_streaks[str(streak['timestamp'])] = copy.deepcopy(streak)
        streak['user'] = user
        streak['timestamp'] = reply_time
        streak['length'] = 1
        streak['start'] = commentid
        streak['end'] = ''
        streak['thread'] = threadid

sorted_max_streaks = sorted([streak for streak in max_streaks.values() if streak['timestamp'] >= 0], key=lambda x: x['timestamp'], reverse=False)



with open("results/biggest_reply_time_streaks_by_timestamp.txt","w") as f:
    f.write("Reply Time|Streak|User|Start|End\n")
    print("Reply Time|Streak|User|Start|End")
    f.write(":-:|:-:|:-:|:-:|:-:\n")
    print(":-:|:-:|:-:|:-:|:-:")
    for item in sorted_max_streaks[:31]:
        timestamp = item['timestamp']
        user = item['user']
        start = item['start']
        end = item['end']
        thread = item['thread']
        length = item['length']
        
        start_link = f"https://www.reddit.com/r/counting/comments/{thread}/_/{start}/"
        end_link = f"https://www.reddit.com/r/counting/comments/{thread}/_/{end}/"
        
        row = f"{timestamp}s | {length} | {user} | [{start}]({start_link}) | [{end}]({end_link}) "
        f.write(f"{row}\n")
        print(row)