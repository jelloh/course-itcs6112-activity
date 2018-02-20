import copy

'''
Aileen Benedict
02/17/2018

Now write a program to read the file generated. Your program should get the value of n (the number of records to be
displayed) from the user, and generate the following output and write them into separate files.
    a.	The top n users who have tweeted the most for the entire timeline. ---------------------- done
    b.	The top n users who have tweeted the most for every hour. ------------------------------- done
    c.	The top n users who have the maximum followers. ----------------------------------------- done
    d.	The top n tweets which have the maximum retweet count. ---------------------------------- done
'''
# -------------------------------------------------------------------------------------------------------
# Specify file from the user
FILE_NAME = input("Enter the file name: ")
INPUT_FILE = './' + FILE_NAME + '.txt'
OUTPUT_FILE = './' + FILE_NAME + '_output.txt'

# Get value of n from the user
N = int(input("Enter value of n: "))

# Information from tweets
users = []
times = []
tweets = []
followers = []
retweets = []

# -------------------------------------------------------------------------------------------------------
# Open the file and retrieve info
with open(INPUT_FILE, 'rb') as f:
    # Loop through the file and save info in lists
    for line in f:
        # Get users from file
        users.append(line.split()[0])
        '''
        user = line_of_text.split()[0]
        if user not in users:
            users.append(user)
        '''
        # Get times from the file
        times.append(
            line[
            (line.find(bytes('[', 'utf-8')) + 1):
            (line.find(bytes(']', 'utf-8')) - 1)]
        )

        # Get tweets
        # From first " to last "
        tweets.append(
            line[
                (line.find(bytes('"','utf-8')) + 1):
                (line.rfind(bytes('"','utf-8')))
            ]
        )

        # Get followers
        # From 2nd to last " " to last " "
        hehe = line.split(bytes(' ','utf-8'))
        followers.append(int((hehe[len(hehe) - 2]).decode('utf-8'))) # I should've done this decoding from the
                                                                     # very beginning... :')
                                                                     # Would've made things so much easier for me ;-;

        # Get retweets
        # last space to end
        retweets.append(
            int((line[(line.rfind(bytes(' ','utf-8'))):]).decode('utf-8'))
        )

# -------------------------------------------------------------------------------------------------------
with open(OUTPUT_FILE, 'w') as f:
    # Find "The top n users who have tweeted the most for the entire timeline."
    print("\n\nTop ", N, " users who have tweeted the most for the entire timeline.")
    f.write("Top users who have tweeted the most for the entire timeline.\nuser - tweet #\n")

    data = {}
    for user in users:
        if data.get(user, -1) == -1:
            data[user] = 1
        else:
            data[user] += 1

    # print N users
    for i in range(0,N):
        max_val = max(data.values())
        for user in data.keys():
            if data[user] == max_val:
                print((user).decode("utf-8")  + 'has ' + str(max_val) + ' tweets.')
                f.write(str((user).decode('utf-8') + ' - ' + str(max_val) + '\n'))
                del data[user]
                break

    data.clear()

    # -------------------------------------------------------------------------------------------------------
    # The top n users who have tweeted the most for every hour
    print("\n\nTop " + str(N) + " users who have tweeted the most for every hour")
    f.write('\nUsers who have tweeted the most for every hour.\nuser - tweets in one hour\n')

    data = {}
    # Loop through users
    # print N users
    for user in users:
        if data.get(user, -1) != -1:
            continue

        # Now loop through times
        index = 0       # current index
        max_c = 1         # current max tweets per hour
        count = 1       # for holding tweets per current hour
        hour = 0        # current hour
        last_hour = 0   # previous hour - used for comparisons

        # Loop to find the highest number of tweets per hour
        for time in times:
            # Only check times for that user if it is the one we are currently checking
            if users[index] == user:
                # Parse current hour
                a = time.find(bytes(':', 'utf-8'))
                b = time.find(bytes(':', 'utf-8'), a+1)
                hour = time[a:b]

                #print(str(hour == last_hour))
                #print("count: " + str(count) + " max: " + str(max))

                # If same as previous hour, increment tweets
                if hour == last_hour:
                    count += 1
                else:
                    # If new hour, check for new max
                    if count > max_c:
                        max_c = count
                    count = 1 # Reset count to 1
                    last_hour = hour

            if count > max_c:
                max_c = count
            index += 1

        data[user] = max_c

    # print N user
    for i in range(0,N):
        m = max(data.values())
        for user in data.keys():
            if data[user] == m:
                print(user.decode("utf-8") , 'has ', m, ' tweets in one hour.')
                f.write(str(user.decode('utf-8') + ' - ' + str(m) + '\n'))
                del data[user]
                break

    data.clear()



    # -------------------------------------------------------------------------------------------------------
    # The top n users who have the maximum followers.
    print("\n\nTop " + str(N) + " users who have the maximum followers")
    f.write('\nTop users who have the maximum followers.\nuser - followers\n')

    data = {}
    u = copy.deepcopy(users)
    fl = copy.deepcopy(followers)
    n = 0
    while n < N:
        index = fl.index(max(fl))
        if u[index] in data:
            u.remove(u[index])
            fl.remove(fl[index])
            continue

        data[u[index]] = fl[index]
        u.remove(u[index])
        fl.remove(fl[index])

        n+= 1

    for d in data:
        print(d.decode('utf-8'), ' has ', data[d], ' followers!')
        f.write(str(d.decode('utf-8') + ' - ' + str(data[d]) + '\n'))

    data.clear()


    # -------------------------------------------------------------------------------------------------------
    # The top n tweets which have the maximum retweet count.
    print("\n\nTop " + str(N) + " tweets which have the maximum retweet count")
    f.write('\nTop tweets with maximum retweet count.\ntweet - retweet count\n')

    data = {}
    t = copy.deepcopy(tweets)
    rt = copy.deepcopy(retweets)
    n = 0
    while n < N:
        index = rt.index(max(rt))
        if t[index] in data:
            t.remove(t[index])
            rt.remove(rt[index])
            continue

        data[t[index]] = rt[index]
        t.remove(t[index])
        rt.remove(rt[index])

        n+= 1

    for d in data:
        print('"', d.decode('utf-8'), '" has ', data[d], ' retweets!')
        f.write(str(d.decode('utf-8') + ' - ' + str(data[d]) + '\n'))

    data.clear()
