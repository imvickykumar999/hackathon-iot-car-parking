
def comments(video_id = 'Cpc_rHf1U6g'):
    from googleapiclient.discovery import build

    api_key = 'AIzaSyCcJX4qdbo9caqxZSKDmuBjNVWfvq8_Wcs'
    dict = {}

    # def video_comments(video_id):
    # empty list for storing reply
    replies = []

    # creating youtube resource object
    youtube = build('youtube', 'v3',
                    developerKey=api_key)

    # retrieve youtube video results
    video_response=youtube.commentThreads().list(
    part='snippet,replies',
    videoId=video_id
    ).execute()

    # print(video_response)

    # iterate video response
    # while video_response:

    # extracting required info
    # from each result object
    for item in video_response['items']:

        # Extracting comments
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']

        # counting number of reply of comment
        replycount = item['snippet']['totalReplyCount']

        # if reply is there
        if replycount>0:

            # iterate through all reply
            for reply in item['replies']['comments']:

                # Extract reply
                reply = reply['snippet']['textDisplay']

                # Store reply is list
                replies.append(reply)

        # print comment with list of reply
        # print(comment, replies, end = '\n\n')
        dict.update({comment: replies})

        # empty reply list
        replies = []

    # Again repeat
    # if 'nextPageToken' in video_response:
    #     video_response = youtube.commentThreads().list(
    #             part = 'snippet,replies',
    #             videoId = video_id
    #         ).execute()
    # else:
    #     break

    # Enter video id
    # video_id = "Cpc_rHf1U6g" # my new video...

    # Call function
    # video_comments(video_id)

    # dictionary to json file...
    # import json
    #
    # with open('comments.json', 'w') as fp:
    #     json.dump(dict, fp)

    return dict


def tvl(vid = 'hlznpxNGFGQ'):
    from googleapiclient.discovery import build

    # video_id = input('Enter video URL or ID : ')
    video_id = vid

    youtube = build('youtube','v3',developerKey='AIzaSyCcJX4qdbo9caqxZSKDmuBjNVWfvq8_Wcs')
    video_request=youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    )

    video_response = video_request.execute()
    title = video_response['items'][0]['snippet']['title']
    likes = video_response['items'][0]['statistics']['likeCount']
    views = video_response['items'][0]['statistics']['viewCount']

    return title, likes, views
