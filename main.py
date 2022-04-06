# main.py TEST GIT PUSH
from dislash import (
    InteractionClient,
    SlashInteraction,
    Option,
    OptionChoice,
    OptionType,
    ActionRow,
    Button,
    SelectMenu,
    SelectOption,
    ButtonStyle,
    ResponseType,
    application_commands
)
from datetime import datetime, time, timedelta
import asyncio
import os
from dotenv import load_dotenv
import discord
from pymongo import MongoClient
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix="?")
bot.remove_command('help')
inter_client = InteractionClient(
    bot, test_guilds=[902715845086691429, 712529260329435146])

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

mongodbcluster = os.getenv('MONGODB_C')

CHANNEL = "918593122626322462"

cluster = MongoClient(mongodbcluster)

db = cluster["question_list"]

collection = db["questions"]

numRows = collection.estimated_document_count()

if collection.estimated_document_count() < 1:
    collection.insert_one({
        "id":
        1,
        "question":
        "No questions at the moment. Please notify a moderator to add more."
    })
    MESSAGE = collection.find_one({"id": 1})["question"]
else:
    MESSAGE = collection.find_one({"id": 1})["question"]




#Sends daily qotd
def seconds_until():  
    qnow = datetime.now()
    setTime = time(15,30)
    future = datetime.combine(qnow, setTime)
    if (future - qnow).days < 0:
        future = datetime.combine(qnow + timedelta(days=1), setTime)
    return (future - qnow).total_seconds()

@tasks.loop(hours=24)
async def send_interval_message():
    await bot.wait_until_ready()
    messageSent = collection.find_one({"id": 1})["question"]
    role = "<@&918675335506165800>"
    embed = discord.Embed(title="Question of the Day",
        description=role + " `" + messageSent + "`",
        color=000000)
    embed.set_thumbnail(
        url=
        "https://cdn.discordapp.com/attachments/929505032322318337/954121742618595398/qotdimg.png"
    )
    await asyncio.sleep(seconds_until())  
    x = 0
    channel = bot.get_channel(918593122626322462)   
    pins = await channel.pins()
    for message in pins:
        await message.unpin()
        x+=1
        if x == 1:
            break
    pinQotd = await channel.send(embed=embed)
    await pinQotd.pin()

    collection.delete_one({"id": 1})
    reorder(1,collection.estimated_document_count())

@send_interval_message.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")
    print(seconds_until())

send_interval_message.start() 

#Manually send a question
@bot.command()
@commands.has_permissions(manage_messages=True)
async def qotd(ctx):
    messageSent2 = collection.find_one({"id": 1})["question"]
    role = "<@&918675335506165800>"
    embed = discord.Embed(title="Question of the Day",
                          description=role + " `" + messageSent2 + "`",
                          color=000000)
    embed.set_thumbnail(
        url=
        "https://cdn.discordapp.com/attachments/929505032322318337/954121742618595398/qotdimg.png"
    )
    botmsg = await ctx.send(embed=embed)
    await botmsg.pin()
    await ctx.message.delete()
    collection.delete_one({"id": 1})
    reorder(1, collection.estimated_document_count())


@bot.command()
@commands.has_permissions(manage_messages=True)
async def help(ctx):
    embed = discord.Embed(title="List of commands", color=discord.Color.blue())
    embed.add_field(
        name="instructions",
        value=
        "Use the prefix '?' and then type in one of the following commands and its required arguments. For adding questions, be sure to surround your question with quotation marks for the bot to accept the entire question.",
        inline=False)
    embed.add_field(
        name="getstatus",
        value=
        "Sends a message if the bot is online as well as the number of questions in its database.",
        inline=False)
    embed.add_field(
        name="get [id]",
        value=
        "Given an id number, it will return the question assigned that id number.",
        inline=False)
    embed.add_field(
        name="add [question]",
        value="Adds the question to the database.\n\n`?add \"What is..\"`",
        inline=False)
    embed.add_field(
        name="remove [id]",
        value=
        "Given an id number, it will remove the question assigned that id number.",
        inline=False)
    embed.add_field(
        name="replace [id] [newquestion]",
        value=
        "Given an id number and new question, it will replace the question assigned that number with the new question.",
        inline=False)
    embed.add_field(
        name="qotd",
        value=
        "Manually post a question from the queue if the auto timer fails for the day or to post a new question.",
        inline=False)
    embed.add_field(name="list",
                    value="List 10 upcoming questions",
                    inline=False)

    await ctx.send(embed=embed)


#Checks if the bot is working. Sends an embedded message if it's online and nothing if it is not.
@bot.command()
@commands.has_permissions(manage_messages=True)
async def getstatus(ctx):
    embed = discord.Embed(title="Bot Status", color=discord.Color.blue())
    embed.add_field(name="Status", value="Online", inline=False)
    embed.add_field(name="Number of questions",
                    value=collection.estimated_document_count())

    await ctx.send(embed=embed)


#LIST WITH PAGES
@bot.command()
@commands.has_permissions(manage_messages=True)
async def list(ctx: SlashInteraction):
    qc = collection.estimated_document_count()
    def tl(id, count):
        if count < id:
            return "*empty*"
        else:
            answer = collection.find_one({"id": id})["question"]
            return answer
    
    def pull(x):
        return f"**{x}.** {tl(x, qc)}"

    page1 = [pull(2),pull(3),pull(4),pull(5),pull(6),pull(7),pull(8),pull(9),pull(10)]
    
    page2 = [pull(11),pull(12),pull(13),pull(14),pull(15),pull(16),pull(17),pull(18),pull(19)]
    
    page3 = [pull(20),pull(21),pull(22),pull(23),pull(24),pull(25),pull(26),pull(27),pull(28),pull(29)]
    
    page4 = [pull(30), pull(31), pull(32),pull(33),pull(34),pull(35),pull(36),pull(37),pull(38),pull(39)]
    
    page5 = [pull(40), pull(41), pull(42), pull(43), pull(44), pull(45), pull(46), pull(47), pull(48), pull(49)]

    page6 = [pull(50), pull(51), pull(52), pull(53), pull(54), pull(55), pull(56), pull(57), pull(58), pull(59)]

    page7 = [pull(70), pull(71), pull(72), pull(73), pull(74), pull(75), pull(76), pull(77), pull(78), pull(79)]

    page8 = [pull(80), pull(81), pull(82), pull(83), pull(84), pull(85), pull(86), pull(87), pull(88), pull(89)]

    page9 = [pull(90), pull(91), pull(92), pull(93), pull(94), pull(95), pull(96), pull(97), pull(98), pull(99)]

    page10 = [pull(100)]

        
    pages = [
        '\n\n'.join(page1),
        '\n\n'.join(page2),
        '\n\n'.join(page3),
        '\n\n'.join(page4),
        '\n\n'.join(page5),
        '\n\n'.join(page6),
        '\n\n'.join(page7),
        '\n\n'.join(page8),
        '\n\n'.join(page9),
        '\n\n'.join(page10)
    ]
    page = 0
    
    emb1 = discord.Embed(
        color=discord.Color.green())
    emb1.add_field(name="Next", value="**1.** " + tl(1, qc))
    emb1.add_field(name="Upcoming", value= pages[page])
    emb1.set_footer(text=f"total # of questions: {qc}")
    
    # Create some buttons
    row_of_buttons = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="<",
            custom_id="prev"
        ),
        Button(
            style=ButtonStyle.green,
            label=">",
            custom_id="next"
        )
    )
    # Send a message
    msg = await ctx.reply(
        embed=emb1,
        components=[row_of_buttons]
    )

    def check(inter):
        return inter.author.id == ctx.author.id
    # One of the ways to process commands
    # See also an example below
    for _ in range(100): # Max 100 clicks per command
        try:
            inter = await msg.wait_for_button_click(check, timeout=None)
        except asyncio.TimeoutError:
            await msg.edit(components=[])
            return
        # inter is instance of ButtonInteraction
        # Get the clicked button id
        ID = inter.clicked_button.custom_id
        # Maybe change the page
        if ID == "prev":
            if page > 0:
                page -= 1
        elif ID == "next":
            if page + 1 < len(pages):
                page += 1
        # Update the message
        emb1.remove_field(1)
        emb1.insert_field_at(2,name="Upcoming", value=pages[page])
        await inter.reply(embed=emb1, type=ResponseType.UpdateMessage)
    
    await msg.edit(components=[])




#Returns the question given an id.
@bot.command()
@commands.has_permissions(manage_messages=True)
async def get(ctx, id):
    if int(id) > collection.estimated_document_count():
        await ctx.channel.send(
            "Question not found. Check to see if your number is greater than the number of questions that exist and try again."
        )
    else:
        id = int(id)
        question = collection.find_one({"id": id})["question"]

        # create embed
        embed = discord.Embed(title="Question info",
                              color=discord.Color.blue())
        embed.add_field(name="id", value=id, inline=False)
        embed.add_field(name="Question", value=question)
        await ctx.send(embed=embed)


#Adds a question to the database
@bot.command()
@commands.has_permissions(manage_messages=True)
async def add(ctx, question):
    question = {
        "id": collection.estimated_document_count() + 1,
        "question": question
    }
    collection.insert_one(question)

    embed = discord.Embed(
        title=
        "Your question has been added. Use '?get [id]' to view your question.",
        color=discord.Color.blue())
    embed.add_field(name="id", value=question.get("id"), inline=False)
    embed.add_field(name="Question", value=question.get("question"))

    await ctx.send(embed=embed)


#Removes the question given an id.
@bot.command()
@commands.has_permissions(manage_messages=True)
async def remove(ctx, id):
    if int(id) > collection.estimated_document_count():
        await ctx.channel.send(
            "Question does not exist. Check to see if your number is greater than the number of questions that exist and try again."
        )
    else:
        id = int(id)
        question = collection.find_one({"id": id})["question"]
        print(question)
        collection.delete_one({"id": id})

        # create embed
        embed = discord.Embed(title="Your question has been removed.",
                              color=discord.Color.blue())
        embed.add_field(name="id", value=id, inline=False)
        embed.add_field(name="Question", value=question)

        await ctx.channel.send(embed=embed)

    reorder(id, collection.estimated_document_count())


#Edits a question given its id and the new question it will replace it with
@bot.command()
@commands.has_permissions(manage_messages=True)
async def replace(ctx, id, newQuestion):
    if int(id) > collection.estimated_document_count():
        await ctx.channel.send(
            "Question not found. Check to see if your number is greater than the number of questions that exist and try again."
        )
    else:
        id = int(id)
        question = collection.find_one({"id": id})["question"]
        collection.find_one_and_replace({
            "id": id,
            "question": question
        }, {
            "id": id,
            "question": newQuestion
        })

        embed = discord.Embed(title="Your question has been replaced",
                              color=discord.Color.blue())
        embed.add_field(name="id", value=id, inline=False)
        embed.add_field(name="Previous Question", value=question, inline=False)
        embed.add_field(name="New Question", value=newQuestion)

        await ctx.channel.send(embed=embed)


#Function that gets called to reorder the ids to ensure that ids for each question incremenet by 1
def reorder(id, numRows):
    if id <= numRows:
        id += 1
        collection.update_one({"id": id}, {"$set": {"id": id - 1}})
        return reorder(id, numRows)
    else:
        return


#Error handling for missing arguments, non-existent commands, or missing manage_messages permissions
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(
            "Error: You need to be manage_messages to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: Missing an arugment.")

    elif isinstance(error, commands.CommandNotFound):
        #await ctx.send("Error: Command not found.")
        return


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    if collection.estimated_document_count() < 1:
        collection.insert_one({
            "id":
            1,
            "question":
            "No questions at the moment. Please notify a moderator to add more."
        })
    


#bot.run(TOKEN)
