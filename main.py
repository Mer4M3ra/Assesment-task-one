"""
MCTiers Data Science App
View Minecraft player rankings from MCTiers API
Made for Preliminary Software Engineering assignment
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# API endpoint - v2 because v1 gets removed June 2026
baseUrl = "https://mctiers.com/api/v2"

# Store user actions for the history feature (assignment requirement)
myHistory = []

def printMenu():
    """Display the main menu options"""
    print("\n" + "=" * 50)
    print("     MCTiers Rankings Explorer")
    print("=" * 50)
    print("1. See all gamemodes")
    print("2. See top players")
    print("3. See rankings for a gamemode")
    print("4. Find a player")
    print("5. See recent tests")
    print("6. What did I do?")
    print("7. Make a graph")
    print("8. Help me")
    print("0. Quit")
    print("-" * 50)

def fetchFromApi(url, extra=None):
    """
    Gets data from the API with error handling
    Without this, network errors would crash the program
    """
    try:
        response = requests.get(url, params=extra, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print("Couldn't find it. Check what you typed.")
            return None
        else:
            print(f"API error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("No internet connection. Check your wifi.")
        return None
    except requests.exceptions.Timeout:
        print("Took too long. Try again.")
        return None
    except Exception as e:
        print(f"Something went wrong: {e}")
        return None

def showGamemodes():
    """
    Shows available gamemodes - user needs this before using option 3
    Otherwise they wouldn't know what slugs to type
    """
    print("\nGetting gamemodes...")
    data = fetchFromApi(f"{baseUrl}/mode/list")
    
    if data:
        print("\n" + "=" * 50)
        print("Gamemodes You Can Check Out")
        print("=" * 50)
        for slug, info in data.items():
            # Only show title, descriptions were too long
            print(f"\n{slug}: {info.get('title', 'No title')}")
        myHistory.append("Looked at gamemodes")
    input("\nPress Enter to continue...")

def showTopPlayers():
    """
    Shows global rankings - most points first
    User picks count because API supports pagination up to 50
    """
    howMany = askHowMany()
    if not howMany:
        return
    
    print(f"\nGetting top {howMany} players...")
    data = fetchFromApi(f"{baseUrl}/mode/overall", {"count": howMany})
    
    if data:
        print("\n" + "=" * 50)
        print(f"Top {len(data)} Players")
        print("=" * 50)
        for i, player in enumerate(data, 1):
            print(f"{i:2}. {player['name']:<20} | Points: {player.get('points', 0):>6} | Region: {player.get('region', '??')}")
        myHistory.append(f"Looked at top {howMany} players")
    input("\nPress Enter to continue...")

def showModeRankings():
    """
    Shows tiered rankings for a specific gamemode
    API returns players grouped by tier 1-5 (1 is highest)
    Tiers 1-2 are labelled HIGH, 3-5 are LOW per MCTiers system
    """
    print("\nGetting gamemodes...")
    allModes = fetchFromApi(f"{baseUrl}/mode/list")
    
    if not allModes:
        return
    
    # Show available gamemodes so user doesn't have to guess
    print("\nGamemodes you can pick from:")
    for slug in allModes.keys():
        print(f"  • {slug}")
    
    modeChoice = input("\nType the gamemode name (like vanilla): ").lower().strip()
    if modeChoice not in allModes:
        print(f"'{modeChoice}' not found. Use option 1 to see all gamemodes.")
        return
    
    howMany = askHowMany()
    if not howMany:
        return
    
    print(f"\nGetting {modeChoice} rankings...")
    data = fetchFromApi(f"{baseUrl}/mode/{modeChoice}", {"count": howMany})
    
    if data:
        print("\n" + "=" * 50)
        print(f"{modeChoice.upper()} Rankings")
        print("=" * 50)
        
        for tier in ['1', '2', '3', '4', '5']:
            playersHere = data.get(tier, [])
            if playersHere:
                tierType = "HIGH" if tier in ['1', '2'] else "LOW"
                print(f"\nTier {tier} ({tierType}):")
                for player in playersHere:
                    # pos 0 = High position, 1 = Low position within tier
                    highLow = "High" if player.get('pos') == 0 else "Low"
                    print(f"  • {player['name']:<20} | {highLow} | Region: {player.get('region', '??')}")
            else:
                print(f"\nTier {tier}: No players here")
        
        myHistory.append(f"Looked at {modeChoice} rankings")
    input("\nPress Enter to continue...")

def findPlayer():
    """
    Search by UUID or username - both are common ways people identify players
    Shows all rankings across gamemodes for that player
    """
    print("\nHow do you want to search?")
    print("1. By UUID (looks like: 6553509f-66d3-4041-875f-164236e42e84)")
    print("2. By username")
    choice = input("Pick 1 or 2: ").strip()
    
    if choice == '1':
        playerId = input("Enter UUID: ").strip()
        if not playerId:
            return
        urlToUse = f"{baseUrl}/profile/{playerId}"
    elif choice == '2':
        playerName = input("Enter username: ").strip()
        if not playerName:
            return
        urlToUse = f"{baseUrl}/profile/by-name/{playerName}"
    else:
        print("Not a valid choice")
        return
    
    print("\nSearching...")
    playerData = fetchFromApi(urlToUse)
    
    if playerData and 'error' not in playerData:
        print("\n" + "=" * 50)
        print(f"Player: {playerData.get('name', 'Unknown')}")
        print("=" * 50)
        print(f"UUID: {playerData.get('uuid', 'N/A')}")
        print(f"Region: {playerData.get('region', 'N/A')}")
        print(f"Points: {playerData.get('points', 0)}")
        print(f"Overall Rank: #{playerData.get('overall', 'N/A')}")
        
        theirRankings = playerData.get('rankings', {})
        if theirRankings:
            print("\nTheir Rankings:")
            for modeName, rankInfo in theirRankings.items():
                tierNum = rankInfo.get('tier')
                highLowPos = "High" if rankInfo.get('pos') == 0 else "Low"
                retiredText = " (Retired)" if rankInfo.get('retired') else ""
                print(f"  • {modeName}: Tier {tierNum} {highLowPos}{retiredText}")
        
        myHistory.append(f"Searched for player: {playerData.get('name', 'Unknown')}")
    elif playerData and playerData.get('error') == "Resource not found":
        print("Couldn't find that player. Check the UUID or username.")
    else:
        print("Something went wrong finding the player")
    
    input("\nPress Enter to continue...")

def seeRecentTests():
    """
    Shows recent ranking changes (tests)
    API returns Unix timestamps, need to convert to readable dates
    """
    howManyTests = input("\nHow many tests to show? (1-20, default 10): ").strip()
    try:
        howManyTests = min(int(howManyTests) if howManyTests else 10, 20)
    except ValueError:
        howManyTests = 10
    
    print(f"\nGetting {howManyTests} recent tests...")
    testData = fetchFromApi(f"{baseUrl}/tests/recent", {"count": howManyTests})
    
    if testData:
        print("\n" + "=" * 50)
        print("Recent Tests")
        print("=" * 50)
        
        for oneTest in testData[:howManyTests]:
            # Convert Unix timestamp to human-readable date
            timeStamp = oneTest.get('at', 0)
            if timeStamp:
                theDate = datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M')
            else:
                theDate = "Unknown"
            
            thePlayer = oneTest.get('player', {})
            playerNameHere = thePlayer.get('name', 'Unknown')
            gameModeHere = oneTest.get('gamemode', 'Unknown')
            newTier = oneTest.get('result_tier', '?')
            newPos = "High" if oneTest.get('result_pos') == 0 else "Low"
            
            print(f"\n{theDate} - {playerNameHere}")
            print(f"  {gameModeHere}: Now Tier {newTier} {newPos}")
        
        myHistory.append(f"Looked at recent tests")
    input("\nPress Enter to continue...")

def seeWhatIDid():
    """
    Display user's session history
    Required by assignment spec - need to record interactions
    """
    if not myHistory:
        print("\nYou haven't done anything yet! Try some options first.")
    else:
        print("\n" + "=" * 50)
        print("What You've Done So Far")
        print("=" * 50)
        for num, thing in enumerate(myHistory[-20:], 1):
            print(f"{num}. {thing}")
    input("\nPress Enter to continue...")

def drawGraph():
    """
    Create bar chart of top players
    Required by marking criteria - need data visualisation
    """
    howManyGraph = input("\nHow many players to put in the graph? (5-20, default 10): ").strip()
    try:
        howManyGraph = min(max(int(howManyGraph) if howManyGraph else 10, 5), 20)
    except ValueError:
        howManyGraph = 10
    
    print(f"\nGetting top {howManyGraph} players...")
    graphData = fetchFromApi(f"{baseUrl}/mode/overall", {"count": howManyGraph})
    
    if graphData:
        playerNames = []
        playerPoints = []
        
        for onePlayer in graphData[:howManyGraph]:
            playerNames.append(onePlayer['name'])
            playerPoints.append(onePlayer.get('points', 0))
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(playerNames)), playerPoints)
        plt.xlabel('Player')
        plt.ylabel('Points')
        plt.title(f'Top {len(playerNames)} Players by Points')
        plt.xticks(range(len(playerNames)), playerNames, rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
        myHistory.append(f"Made a graph of top {howManyGraph} players")
    input("\nPress Enter to continue...")

def helpMe():
    """
    Explain what tiers, tests, etc mean
    New users won't understand MCTiers terminology
    """
    print("\n" + "=" * 50)
    print("Help Guide - What Everything Means")
    print("=" * 50)
    print("\nGamemodes:")
    print("  Different game types like Vanilla, Sword, etc.")
    print("\nTiers:")
    print("  Tier 1 = Best players")
    print("  Tier 5 = Lower ranked players")
    print("  High/Low = Position within each tier")
    print("\nSearching:")
    print("  UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
    print("  Username: Current Minecraft Java name")
    print("\nTests:")
    print("  Tests show when a player's rank changes")
    print("  They show the old rank and new rank")
    print("=" * 50)
    input("\nPress Enter to continue...")

def askHowMany():
    """
    Get count from user, enforce API limit of 50
    Default 10 is reasonable for display
    """
    howMany = input("\nHow many results? (1-50, default 10): ").strip()
    try:
        howMany = int(howMany) if howMany else 10
        if howMany < 1:
            howMany = 10
        elif howMany > 50:
            print("Max is 50, using 50")
            howMany = 50
        return howMany
    except ValueError:
        print("That's not a number, using 10")
        return 10

def start():
    """
    Main program loop
    Menu-driven interface as per assignment requirements
    """
    print("\nWelcome to my MCTiers Rankings Explorer!")
    print("Type a number to pick something.")
    
    while True:
        printMenu()
        usersPick = input("What do you want to do? (0-8): ").strip()
        
        if usersPick == '0':
            print("\nThanks for using my program!")
            print(f"You did {len(myHistory)} things this session.")
            break
        elif usersPick == '1':
            showGamemodes()
        elif usersPick == '2':
            showTopPlayers()
        elif usersPick == '3':
            showModeRankings()
        elif usersPick == '4':
            findPlayer()
        elif usersPick == '5':
            seeRecentTests()
        elif usersPick == '6':
            seeWhatIDid()
        elif usersPick == '7':
            drawGraph()
        elif usersPick == '8':
            helpMe()
        else:
            print("That's not an option. Pick a number between 0 and 8.")

if __name__ == "__main__":
    start()