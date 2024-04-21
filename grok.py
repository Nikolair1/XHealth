import asyncio
import xai_sdk
import sys

file_path = "all_tweets.txt"

Prompt  = """
You are a tweet categorizer. Your job is to take tweets and categorize them into the following categories:
- Category: *Disease outbreaks and public health emergencies*
- Category: **
- Category: **
- Category: **
- Category: *None of the above*

Here are some examples:

## Tweet: YAPYAPYAP
Category: *Disease outbreaks and public health emergencies*


###Take the following 10 tweets and categorize them like above:

##Tweet: {tweet0}
Category:

"""


async def main3():
    """Runs the example."""
    client = xai_sdk.Client()
    conversation = client.grok.create_conversation()

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 100):
            set_of_lines = lines[i:i+100]
            # Do something with the set of lines
            print(f"Processing set {i//100 + 1}:")
            text = "digest this information" + "".join(set_of_lines)
            token_stream, _ = conversation.add_response(text.strip())

    


    text = (
        "Summarize these tweets into these categories: Disease Outbreaks and Public Health Emergencies, Medical Research and Innovations, Health and Wellness Awareness.  Include links to more information and emojis when you can, exclude promotional tweets and awareness months. Thanks "
        
    )
    # print("Human:", text.strip())
    token_stream, _ = conversation.add_response(text.strip())
    print("Grok: ", end="")
    async for token in token_stream:
        print(token, end="")
        sys.stdout.flush()
    print("\n")

    print("===")
    print("Generating title..")
    title = await conversation.generate_title()
    print(f"Title: {title}")
    print("===\n")


asyncio.run(main3())
