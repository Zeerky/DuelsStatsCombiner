key = "00000000-0000-0000-0000-000000000000" #REPLACE THIS WITH API KEY

import os

try:
    import requests
except ModuleNotFoundError:
    print("'Requests' module not found, installing...")
    print("This is for calling stats from the hypixel/mojang api")
    os.system("pip install requests")
    import requests

if key == "00000000-0000-0000-0000-000000000000":
	print("You can set this by default by editing this file")
	key = input("API KEY: ")

def getUUID(name):
	url = f'https://api.mojang.com/users/profiles/minecraft/{name}?'
	response = requests.get(url)
	uuid = response.json()['id']
	return uuid.lower()

def getIGN():
    nameRequest = requests.get("https://api.mojang.com/user/profiles/%s/names" % uuid).json()
    currentUsername = nameRequest[-1].get('name')
    return currentUsername.lower()

def checkOnline(name):
	url = f"https://api.hypixel.net/player?key={key}&uuid={getUUID(name)}"
	data = requests.get(url).json()
	lastLogin = data["player"].get("lastLogin", 0)
	lastLogout = data["player"].get("lastLogout", 0)
	if lastLogin > lastLogout:
		return "Status: Online"
	else:
		return "Status: Offline"
	

def main():
	duel = input("enter duel: ")
	duel = duel.lower()
	nameList = input("Please enter your usernames seperated by spaces: ").split()
	
	totalWins = 0
	totalAccounts = 0
	bestStreak = 0
	bestStreakPlayer = "none"
	bestOverallStreak = 0
	bestOverallStreakPlayer = "none"

	for i in nameList:
		url = f"https://api.hypixel.net/player?key={key}&uuid={getUUID(i)}"
		data = requests.get(url).json()
		sumoWins = data["player"]["stats"]["Duels"].get(f"{duel}_duel_wins", 0)
		sumoWins += data["player"]["stats"]["Duels"].get(f"{duel}_doubles_wins", 0)
		sumoWins += data["player"]["stats"]["Duels"].get(f"{duel}_four_wins", 0)
		sumoLosses = data["player"]["stats"]["Duels"].get(f"{duel}_duel_losses", 0)
		idvBestStreak = data["player"]["stats"]["Duels"].get(f"best_{duel}_winstreak", 0)
		currentStreak = data["player"]["stats"]["Duels"].get(f"current_{duel}_winstreak", 0)
		if currentStreak > bestStreak:
			bestStreak = currentStreak
			bestStreakPlayer = i
		if idvBestStreak > bestOverallStreak:
			bestOverallStreak = idvBestStreak
			bestOverallStreakPlayer = i

		totalWins = totalWins + sumoWins
		totalAccounts = totalAccounts + 1
		print(i + f" {duel.capitalize()} Wins: " + str("{:,}".format(sumoWins)))
		print(i + f" {duel.capitalize()} Losses: " + str("{:,}".format(sumoLosses)))
		print(f"Current streak: " + str("{:,}".format(currentStreak)))
		print(f"Best streak: " + str("{:,}".format(idvBestStreak)))
		print(checkOnline(i))
		print("Current total: " + str("{:,}".format(totalWins)))
		print("-" * 5)

	print("\n\nTotal Accounts Checked: " + str(totalAccounts))
	print("Overall Wins: " + str("{:,}".format(totalWins)))
	print("Highest Current Streak: " + str("{:,}".format(bestStreak)) + " by " + bestStreakPlayer)
	print("Highest Overall Streak: " + str("{:,}".format(bestOverallStreak)) + " by " + bestOverallStreakPlayer)
	test = input("\npress enter to continue")
	print("\n" * 5)
	main()

main()
