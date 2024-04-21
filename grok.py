import asyncio
import xai_sdk
import sys

file_path = "all_tweets.txt"


async def main():
    """Runs the example."""
    client = xai_sdk.Client()
    conversation = client.grok.create_conversation()

    with open(file_path, "r") as file:
        lines = file.readlines()
        text = "".join(lines[:100])

    text = (
        "Summarize these tweets into these categories: Disease Outbreaks and Public Health Emergencies, Medical Research and Innovations, Health and Wellness Awareness.  Include links to more information and emojis when you can, exclude promotional tweets and awareness months. Thanks "
        + text
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


asyncio.run(main())
