import discord
import asyncio 
from random import randint
import time 
import threading

TOKEN = ''
timeout_list = []
roles_global = None

client = discord.Client()

async def my_background_task():
	await client.wait_until_ready()
	global timeout_list
	while True:
		await asyncio.sleep(1)
		#print('Checking Ban, ', len(timeout_list), 'in timeout!')
		for a in timeout_list:
			if a[1] + 30 < time.time():
				for role in roles_global:
					if role.name == 'Fruit':
						role_to_add = role
				await client.add_roles(a[0], role_to_add)
				print(role_to_add.name,'role added.')
				timeout_list.remove(a)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    #print(client.user.id)
    print('------')

@client.event
async def on_message(message):
	global timeout_list
	global roles_global
	#Get users & roles 
	for server in client.servers:
		if int(server.id) == 286966714875379721:
			members	= server.members
			roles 	= server.roles
	roles_global = roles
	#!roulette
	if message.content.startswith('!roulette'):
		#HIT
		if (randint(0, 5)) == 0:
			await client.send_message(message.channel, '**BOOM!!**')
			for member in members:
				if str(member.name + '#' + member.discriminator) == str(message.author):
					mem_to_kill = member
					break
			for role in roles:
				if role.name == 'Fruit':
					role_to_remove = role
					break
			await client.remove_roles(mem_to_kill, role_to_remove)
			print(role_to_remove.name,'role removed.')
			timeout_list.append((mem_to_kill, time.time()))
		#MISS
		else:
			await client.send_message(message.channel, '*crickets*')
	

client.loop.create_task(my_background_task())
client.run(TOKEN)
# asyncio.sleep(n)