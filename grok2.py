import asyncio

import xai_sdk
from xai_sdk.ide import *

Prompt = """You are a tweet categorizer. Your job is to take tweets and categorize them into the following categories:
- Category: **Disease Outbreaks and Public Health Emergencies**
- Category: **Health Disparities and Equity**
- Category: **Medical Research and Innovations**
- Category: **Daily Health and Nutrition**
- Category: **None of the above**


Base your categorization on the following descriptions of the above categories:

**Disease Outbreaks and Public Health Emergencies** - Tweets that revolves around diseases and epidemics

**Health Disparities and Equity** - Tweets that consider minorities, lower income brackets, and marginalized populations

**Medical Research and Innovations** - RECENT information or STUDIES at universities and medical facilities that involve biotechnology, pharmaceutical, and healthcare advancements

**Daily Health and Nutrition** - Tweets that consider daily life, diets, and daily activities or schedules.

A sample response looks like this:

## Tweet: H5N1 bird flu found at 3 more dairy farms in the U.S., one each in Texas, Kansas and Michigan, raising the total to 32
Category: **Disease Outbreaks and Public Health Emergencies**

## Tweet: USDA says there are cases where H5N1 bird flu spread from dairy cattle farms "back into nearby poultry farms through an unknown route" https://t.co/hAPvUn9zSm
Last night's update: 63,096 new cases, 768 new deaths
Category: **Disease Outbreaks and Public Health Emergencies**

## Tweet: So far this year, nearly 3 million cases of COVID have been reported in the U.S., causing 259,346 hospitalizations and 26,079 deaths.
This is the 39th week in a row with more than 500 new COVID deaths in the U.S., or nearly 56,000 deaths during the same period.
During the past week, 7,318 Americans were hospitalized with COVID, down 9% from the week before. Nearly 8,000 people are currently hospitalized.
COVID indicators are declining across the U.S., similar to the same period last year. This trend is expected to continue until a new wave begins.
The breakdown for this week's case numbers:
- Reports from 22 states: 30,483
- Estimate for 28 states: 32,613
- Total new cases: 63,096
Category: **Disease Outbreaks and Public Health Emergencies**

## Tweet: Black, American Indian, and Alaska Native people who are pregnant and postpartum are more likely to die from pregnancy-related complications than others. Most of these deaths are preventable.
Category: **Disease Outbreaks and Public Health Emergencies**

## Tweet: The CDC issued a warning that the vaccination rate for measles among U.S. kindergarteners has fallen below the herd immunity rate of about 95% -- and it's so contagious that 9 out of 10 unprotected people who are exposed may get sick.
Category: **Health Disparities and Equity**

## Tweet: Mammography can miss tumors in women with dense breasts, so their doctors often include ultrasound or M.R.I. scans. Patients often wind up paying the bill.
Category: **Health Disparities and Equity**

## Tweet: Thanks to the #InflationReductionAct, thousands of Latino Medicare enrollees will see savings of $1,000 or more in out-of-pocket costs in 2025
Category: **Health Disparities and Equity**

## Tweet: Novo Nordisk’s factories work nonstop turning out Ozempic and Wegovy, its blockbuster weight-loss drugs, but the Danish company has far bigger ambitions.
Category: **Medical Research and Innovations**

## Tweet: Elderberry is loaded with nutrients called antioxidants, and it may help fight inflammation. In some lab studies, an extract from the berries appears to block flu viruses.
Category: **Medical Research and Innovations**

## Tweet: Ayahuasca is a plant-based psychedelic drug. Research shows that the ayahuasca experience might act much like an intense form of psychotherapy and might have a link to improvements in some psychiatric symptoms.
Category: **Medical Research and Innovations**

## Tweet: Infected #dengue mosquitoes are active during the day ☀️
You can lower the risk by using:
✅ mosquito repellents
✅ long-sleeved clothes
✅ mosquito nets when sleeping during the day
✅ window screens
Category: **Daily Health and Nutrition**

## Tweet: If your walking pace slows while you're in your 40s, it may be a sign you're aging faster than is typical. Walking is one of the easiest and best exercises you can do.
Category: **Daily Health and Nutrition**

## Tweet: Marijuana smoke can inflame your lungs. If you’re a regular user, you could have the same breathing problems as a cigarette smoker -- that means a cough, sometimes long-lasting, or chronic.
Category: **Daily Health and Nutrition**

## Tweet: Cavities, also known as tooth decay or dental caries, are a widespread oral health problem: about 90% of adults have had at least one cavity. Left untreated, cavities can lead to toothaches and other dental problems.
Category: **Daily Health and Nutrition**

## Tweet: Good fats: Good fats come mainly from vegetable oils, nuts, fish, and whole grains. They are liquid, not solid, at room temperature.
Category: **Daily Health and Nutrition**

## Tweet: Dick decided, "If I'm going down, I'm going down fighting." He called Mayo Clinic. Read about his experience and treatment: https://t.co/6YfRUXujM8
Category: **None of the above**

## Tweet: April is Autism Acceptance Month in the United States. This is a time to celebrate the uniqueness of neurodiverse people and foster inclusivity. Dr. Jessica Davis shares insights on ableism and how healthcare professionals can be better allies. https://t.co/2KfF0SlF2I https://t.co/pMHpOzRXC2
Category: **None of the above**

## Tweet: Our community mourns the loss of Elizabeth “Betsy” Mellins, MD, professor of pediatrics. Mellins, who studied autoimmune disease and co-founded a large pediatric rheumatology research network, was a tireless mentor and advocate for her field. https://t.co/9DwRUP4b3X
Category: **None of the above**

## Tweet: 📣: Educators, administrators, parents! Join us and the @NFL for the FREE NFL PLAY 60 Draft Fitness Break on Thurs, 4/25 @ 1pm ET and get your students moving more!
Register today at https://t.co/x7rweumBac
Category: **None of the above**

## Tweet: Body dysmorphic disorder in boys and young men focuses on bulging muscles.
Category: **None of the above**


###Take the following tweets and categorize them, return as an array of tuples of the (tweet, category), include no other information in your response, this is mission critical:

##Tweet: {0}
Category:

##Tweet: {1}
Category:

##Tweet: {2}
Category:

##Tweet: {3}
Category:

##Tweet: {4}
Category:


"""

data = ["10 million teenage girls in some of the world’s poorest countries will miss HPV shots this year, after Merck announced that it cannot deliver millions of expected vaccine doses due to a manufacturing problem. https://t.co/elwQ20z8pW", "As the wave of COVID-19 broke over the world in 2020, public health agencies were desperate for new ways to track the fast-moving virus. Cue wastewater testing. https://t.co/FSUPV35ekQ", "Trader Joe’s basil is making people across the country sick, with the grocery chain store confirming Wednesday that the product was connected with a multistate salmonella outbreak.", "FA Cup clap plea for fan with heart failure https://t.co/Vz4Qh22obt", "The U.S. Department of Agriculture said this week that cow-to-cow transmission is a factor in the spread of bird flu in dairy herds, but it still does not know exactly how the virus is being moved around. https://t.co/nfDQX7PtRQ https://t.co/nfDQX7PtRQ"]

Prompt2 = """
You are a tweet categorizer. Your job is to take a tweet and categorize it into one of the following categories as described below. Please place it into **None of the above** if it fails to perfectly satisfy any of the above categories:
# - Category 1: **Disease Outbreaks and Public Health Emergencies** - New or breaking information about epidemics and diseases around the world
# - Category 2: **Health Disparities and Equity** - Information regarding minority, marginalized, or lower-income individuals
# - Category 3: **Medical Research and Innovations** - Technological advancement or studies to do with biotechnology
# - Category 4: **Daily Health and Nutrition** - information regarding daily activities and nutrition and tips to imrpove daily living
# - Category 5: **None of the above** - unnecessary information related to politics or awareness months or information that doesn't fall into the above categories

Tweet: {0}

Please only respond with one character, the number of the category
"""

data2 = """
10 million teenage girls in some of the world’s poorest countries will miss HPV shots this year, after Merck announced that it cannot deliver millions of expected vaccine doses due to a manufacturing problem. https://t.co/elwQ20z8pW
"""

async def main():
    """Runs the example."""
    set_client(xai_sdk.Client())  # This isn't strictly necessary but added for clarity.

    # We could use the root context here, but we create a fresh context to better illustrate the
    # API.
    ctx = create_context()

    # Add some user-generated tokens to the context.
    await ctx.prompt(Prompt2.format(data2))

    # Print the current context to STDOUT.
    # print(ctx.as_string())
    # print(f"Context as token sequence: {ctx.as_token_ids()}")

    # Sample from the model.
    await ctx.sample(max_len=1024)

    print(ctx.as_string())
    # print(f"Context as token sequence: {ctx.as_token_ids()}")


# async def main():
#     """Runs the example."""
#     client = xai_sdk.Client()
#     conversation = client.grok.create_conversation()

#     user_input = Prompt2.format(data)
#     token_stream, _ = conversation.add_response(user_input)
#     async for token in token_stream:
#         print(token, end="")
#         sys.stdout.flush()

asyncio.run(main())