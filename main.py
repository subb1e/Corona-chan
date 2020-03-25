import discord
import datetime
import COVID19Py

covid19 = COVID19Py.COVID19()
client = discord.Client()

locations = covid19.getLocations()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('/corona'):
        lquery = message.content[7:].strip()
        locationQuery = lquery.lower() 
       

        if "united states" in locationQuery or "usa" in locationQuery:
            locationQuery = "US"
        elif "south korea" in locationQuery or "korea" in locationQuery:
            locationQuery = "korea, south"

        try:
            for i in locations:
                if i['province'] != "":
                    continue
                if i['country'].lower() == locationQuery.lower():
                    country = str(i['country'])
                    confirmed = str(i['latest']['confirmed'])

                    cases = country + " has **" + confirmed + "** confirmed cases."
                    await message.channel.send(cases)
                
                    lastupdate = str(i['last_updated'])
                    newdate = datetime.datetime.strptime(lastupdate, '%Y-%m-%dT%H:%M:%S.%fZ')
                    timedesc = "This information was updated on {:%A, %B %d, %Y}."
                    timedesc = timedesc.format(newdate.date())

                    deaths = str(i['latest']['deaths'])
                    recovered = str(i['latest']['recovered'])

                    embed = discord.Embed(title="Coronavirus cases in " + country, description=timedesc, color=0x764BA7)
                    embed.add_field(name="Deaths", value=deaths, inline=True)
                    imgurl = "https://i.imgur.com/UrbDTj1.png"
                    embed.set_thumbnail(url=imgurl)
                    await message.channel.send(embed=embed)
                
        except Exception as ex:
            print(ex)

    if message.content.startswith('/corona help'):
        embed = discord.Embed(title="Bot help", color=0x764BA7)
        embed.add_field(name="Get case information", value="/corona <country>")
        await message.channel.send(embed=embed)

if __name__ == '__main__':
    import config
    client.run(config.token)