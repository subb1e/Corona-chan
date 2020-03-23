import discord
import csv
import datetime

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    locationQuery = message.content[7:].strip()

    if message.author == client.user:
        return

    if message.content.startswith('/corona'):
        with open('03-22-2020.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            
            try:
                for row in reader:
                    if row['Province/State'] != "" and row['Province/State'] != row['Country/Region']:
                        continue
                    if row['Country/Region'].lower() == locationQuery:
                        cases = row['Country/Region'] + " has **" + row['Confirmed'] + "** confirmed cases."
                        await message.channel.send(cases)
                        
                        lastupdate = row["Last Update"]
                        newdate = datetime.datetime.strptime(lastupdate, '%Y-%m-%dT%H:%M:%S')
                        timedesc = "This information was updated on {:%A, %B %d, %Y}."
                        timedesc = timedesc.format(newdate.date())

                        deaths = row["Deaths"]
                        recovered = row["Recovered"]

                        embed = discord.Embed(title="Coronavirus cases in " + row["Country/Region"], description=timedesc, color=0x764BA7)
                        embed.add_field(name="Deaths", value=deaths, inline=True)
                        embed.add_field(name="Recovered", value=recovered, inline=True)
                        imgurl = "https://i.imgur.com/UrbDTj1.png"
                        embed.set_thumbnail(url=imgurl)
                        await message.channel.send(embed=embed)
                    
            except Exception as ex:
                print(ex)

if __name__ == '__main__':
    import config
    client.run(config.token)