from openai import OpenAI
import asyncio
import random
import json




prompt = """You are a tweet analyzer, extract all the information from these tweets that pertains to each of these categories:
    **Disease Outbreaks and Public Health Emergencies** - New or breaking information about only epidemics and diseases around the world, avoid covid related updates unless they involve new variants
    **Health Disparities and Equity** - Information regarding minority, marginalized, or lower-income individuals, avoid initiatives and awareness months/weeks
    **Medical Research and Innovations** - advancements or studies to do with biotechnology
    **Daily Health and Nutrition** - information regarding daily activities and nutrition and tips to imrpove daily living
    **None of the above** - unnecessary information related to politics or awareness months or information that doesn't fall into the above categories
     
 Find the 5 best tweets for each of the categories and then summarize them into a 280 character passage that uses correct grammar and is easy to follow as if there was no longer access to the tweets. Be as specific as possible while maintaining the paragraph format. Use complete sentences and avoid semicolons and return them in the following format:
{"category1": "summary1", "category2":  "summary2", "category3": "summary3", "category4":  "summary4"}

Then add another item to the dictionary that contains a full summary of the tweets of length 240 characters called "summary".
"""


file_path = "all_tweets.txt"

async def create_summaries():
  client = OpenAI()
  text = ""
  with open(file_path, 'r') as file:
    lines = file.readlines() 
    random.shuffle(lines)
    text = lines[0:200]
  
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": prompt},
      {"role": "user", "content": "".join(text)}
    ],
  )
  dict = json.loads(completion.choices[0].message.content)
  arr = []
  arr.append(dict["Disease Outbreaks and Public Health Emergencies"])
  arr.append(dict["Health Disparities and Equity"])
  arr.append(dict["Medical Research and Innovations"])
  arr.append(dict["Daily Health and Nutrition"])
  print(arr)

  completion2 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Take an array of sentences and create a 200 character summary form them"},
      {"role": "user", "content": "".join(arr)}
    ],
    max_tokens=4096
  )
  print(completion2.choices[0].message.content)
  arr.append(completion2.choices[0].message.content)
  return arr

asyncio.run(create_summaries())