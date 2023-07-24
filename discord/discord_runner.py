import discord
from discord import app_commands
from discord.ext import commands
from weather import main
from datetime import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("bot_token")
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@client.event
async def on_ready():
    print('The bot is online, logged in as {0.user}'.format(client))
    synced = await client.tree.sync()
    print(f"{len(synced)} commands synced.")
    print()
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="a working prototype, let's go."))


@client.tree.command(name="weather", description="Gets the weather of a specified city.")
@app_commands.describe(city="State the city.")
async def weather_getter(interaction: discord.Interaction, city: str, ):
    current_time = time.ctime(time.time())
    print(f"At {current_time}, user {interaction.user.name} queried about the city of {city}.")
    matching_cities = main.list_searcher(city)
    if len(matching_cities) > 1:
        option_message = ["There is more than one city for your query.",
                          "Which of the following cities correspond to your query?"]
        character = 65
        for index, city_dictionary in enumerate(matching_cities):
            city_moniker = city_dictionary["city"]
            state_moniker = city_dictionary["admin_name"]
            if "," in state_moniker:
                name = state_moniker.split(", ")
                name = name[::-1]
                state_moniker = " ".join(name)
            country_moniker = city_dictionary["country"]
            full_sentence = f"**{chr(character)}.** {city_moniker}, {state_moniker}, {country_moniker}"
            option_message.append(full_sentence)
            character += 1
        option_message = "\n".join(option_message)
        await interaction.response.defer()
        await interaction.followup.send(option_message)

        def check(m: discord.Message):
            return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

        content = await client.wait_for('message', check=check, timeout=30)
        letter = content.content
        if letter.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and len(letter) == 1:
            real_index = int(ord(letter.upper()) - 65)
            try:
                matching_cities = matching_cities[real_index]
                weather_data = main.weather_acquirer(matching_cities)
                dictionary_output = matching_cities
                if isinstance(dictionary_output, list):
                    dictionary_output = matching_cities[0]
                city_name = dictionary_output.get('city')
                country_name = dictionary_output.get('country')
                state_name = dictionary_output.get('admin_name')
                current_weather = weather_data.get("current_weather")
                temperature = current_weather.get("temperature")
                wind_speed = current_weather.get("windspeed")
                wind_direction = current_weather.get("winddirection")
                current_conditions = current_weather.get("weathercode")
                current_conditions = main.weather_code_decipher(current_conditions)
                time_updated = current_weather.get("time")
                time_updated = str(datetime.fromisoformat(time_updated)).split()[1]
                if "," in state_name:
                    name = state_name.split(", ")
                    name = name[::-1]
                    state_name = " ".join(name)
                city_sentence = [city_name, state_name, country_name]
                city_sentence = [i for i in city_sentence if len(i) != 0]
                city_sentence = ", ".join(city_sentence)
                embedded_content = discord.Embed(title=f"Latest Weather for {city_sentence}",
                                                 description=f"Correct as of {time_updated} AEST", color=0x00ff00)
                embedded_content.add_field(name="Condition", value=current_conditions, inline=True)
                embedded_content.add_field(name="Temperature", value=f"{temperature}°C", inline=True)
                embedded_content.add_field(name="Wind", value=f"{wind_speed}km/h at bearing {wind_direction}°",
                                           inline=True)
                await interaction.followup.send(embed=embedded_content)
                print(f"The result {city_sentence} was printed.")
                print()
            except IndexError:
                await interaction.followup.send("Input not recognized, please redo the command.")
                print("No result was printed.")
        else:
            await interaction.followup.send("Input not recognized, please redo the command.")
            print("No result was printed.")


    elif len(matching_cities) == 0:
        await interaction.response.defer()
        await interaction.followup.send("The city was not recognized, please try again.")
        print("No result was printed.")
        print()

    else:
        weather_data = main.weather_acquirer(matching_cities)
        dictionary_output = matching_cities
        if isinstance(dictionary_output, list):
            dictionary_output = matching_cities[0]
        city_name = dictionary_output.get('city')
        country_name = dictionary_output.get('country')
        state_name = dictionary_output.get('admin_name')
        current_weather = weather_data.get("current_weather")
        temperature = current_weather.get("temperature")
        wind_speed = current_weather.get("windspeed")
        wind_direction = current_weather.get("winddirection")
        current_conditions = current_weather.get("weathercode")
        current_conditions = main.weather_code_decipher(current_conditions)
        if "," in state_name:
            name = state_name.split(", ")
            name = name[::-1]
            state_name = " ".join(name)
        time_updated = current_weather.get("time")
        time_updated = str(datetime.fromisoformat(time_updated)).split()[1]
        city_sentence = [city_name, state_name, country_name]
        city_sentence = [i for i in city_sentence if len(i) != 0]
        city_sentence = ", ".join(city_sentence)
        embedded_content = discord.Embed(title=f"Latest Weather for {city_sentence}",
                                         description=f"Correct as of {time_updated} AEST", color=0x00ff00)
        embedded_content.add_field(name="Condition", value=current_conditions, inline=True)
        embedded_content.add_field(name="Temperature", value=f"{temperature}°C", inline=True)
        embedded_content.add_field(name="Wind", value=f"{wind_speed}km/h at bearing {wind_direction}°", inline=True)
        await interaction.response.send_message(embed=embedded_content)
        print(f"The result {city_sentence} was printed.")
        print()


client.run(token)
