import asyncio

import xai_sdk
import sys



file_path = "all_tweets.txt"
with open(file_path, "r") as file:
    data = file.read()

async def main():
    """Runs the example."""
    client = xai_sdk.Client()

    conversation = client.grok.create_conversation()

    print("Enter an empty message to quit.\n")

    first = True
    while True:
        user_input = input("Human: ")
        print("")

        if not user_input:
            return

        token_stream, _ = conversation.add_response(user_input)
        print("Grok: ", end="")
        async for token in token_stream:
            print(token, end="")
            sys.stdout.flush()
        print("\n")

        if first:
            print("===")
            print("Generating title..")
            title = await conversation.generate_title()
            print(f"Title: {title}")
            print("===\n")
            first = False


asyncio.run(main())