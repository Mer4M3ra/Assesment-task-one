"""
MCTiers Data Science App
A simple program to view Minecraft player rankings
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# API URL
API_URL = "https://mctiers.com/api/v2"

# Store user actions for history
history = []

def showMenu():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("     MCTiers Rankings Explorer")
    print("=" * 50)
    print("1. List all gamemodes")
    print("2. View overall rankings")
    print("3. View gamemode rankings")
    print("4. Search for a player")
    print("5. View recent tests")
    print("6. View my history")
    print("7. Create a graph")
    print("8. Help")
    print("0. Exit")
    print("-" * 50)

def getData(url, params=None):
    """Get data from API with error handling"""
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print("Not found. Check your input.")
            return None
        else:
            print(f"API error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("Cannot connect to internet. Check your connection.")
        return None
    except requests.exceptions.Timeout:
        print("Request timed out. Try again.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def showGamemodes():
    """Show all available gamemodes"""
    print("\nFetching gamemodes...")
    data = getData(f"{API_URL}/mode/list")
    
    if data:
        print("\n" + "=" * 50)
        print("Available Gamemodes")
        print("=" * 50)
        for slug, info in data.items():
            # Only show the gamemode name, no description
            print(f"\n{slug}: {info.get('title', 'No title')}")
        history.append("Viewed gamemodes")
    input("\nPress Enter to continue...")

def showOverall():
    """Show top players by points"""
    count = getCount()
    if not count:
        return
    
    print(f"\nFetching top {count} players...")
    data = getData(f"{API_URL}/mode/overall", {"count": count})
    
    if data:
        print("\n" + "=" * 50)
        print(f"Top {len(data)} Players")
        print("=" * 50)
        # Show ALL players, not just first 20
        for i, player in enumerate(data, 1):
            print(f"{i:2}. {player['name']:<20} | Points: {player.get('points', 0):>6} | Region: {player.get('region', '??')}")
        history.append(f"Viewed overall rankings (top {count})")
    input("\nPress Enter to continue...")

def showGamemodeRankings():
    """Show rankings for a specific gamemode"""
    # First show available gamemodes
    print("\nFetching gamemodes...")
    gamemodes = getData(f"{API_URL}/mode/list")
    
    if not gamemodes:
        return
    
    print("\nAvailable gamemodes:")
    for slug in gamemodes.keys():
        print(f"  • {slug}")
    
    # Get user input
    gamemode = input("\nEnter gamemode name (e.g., vanilla): ").lower().strip()
    if gamemode not in gamemodes:
        print(f"'{gamemode}' not found. Use option 1 to see all gamemodes.")
        return
    
    count = getCount()
    if not count:
        return
    
    print(f"\nFetching {gamemode} rankings...")
    data = getData(f"{API_URL}/mode/{gamemode}", {"count": count})
    
    if data:
        print("\n" + "=" * 50)
        print(f"{gamemode.upper()} Rankings")
        print("=" * 50)
        
        for tier in ['1', '2', '3', '4', '5']:
            players = data.get(tier, [])
            if players:
                tier_type = "HIGH" if tier in ['1', '2'] else "LOW"
                print(f"\nTier {tier} ({tier_type}):")
                for player in players:
                    pos = "High" if player.get('pos') == 0 else "Low"
                    print(f"  • {player['name']:<20} | {pos} | Region: {player.get('region', '??')}")
            else:
                print(f"\nTier {tier}: No players")
        
        history.append(f"Viewed {gamemode} rankings")
    input("\nPress Enter to continue...")

def searchPlayer():
    """Search for a player by UUID or username"""
    print("\nSearch by:")
    print("1. UUID (e.g., 6553509f-66d3-4041-875f-164236e42e84)")
    print("2. Username")
    choice = input("Choose (1 or 2): ").strip()
    
    if choice == '1':
        uuid = input("Enter UUID: ").strip()
        if not uuid:
            return
        url = f"{API_URL}/profile/{uuid}"
    elif choice == '2':
        name = input("Enter username: ").strip()
        if not name:
            return
        url = f"{API_URL}/profile/by-name/{name}"
    else:
        print("Invalid choice")
        return
    
    print("\nSearching...")
    data = getData(url)
    
    if data and 'error' not in data:
        print("\n" + "=" * 50)
        print(f"Player: {data.get('name', 'Unknown')}")
        print("=" * 50)
        print(f"UUID: {data.get('uuid', 'N/A')}")
        print(f"Region: {data.get('region', 'N/A')}")
        print(f"Points: {data.get('points', 0)}")
        print(f"Overall Rank: #{data.get('overall', 'N/A')}")
        
        # Show rankings
        rankings = data.get('rankings', {})
        if rankings:
            print("\nRankings:")
            for mode, rank in rankings.items():
                tier = rank.get('tier')
                pos = "High" if rank.get('pos') == 0 else "Low"
                retired = " (Retired)" if rank.get('retired') else ""
                print(f"  • {mode}: Tier {tier} {pos}{retired}")
        
        history.append(f"Searched for player: {data.get('name', 'Unknown')}")
    elif data and data.get('error') == "Resource not found":
        print("Player not found. Check the UUID or username.")
    else:
        print("Could not find player")
    
    input("\nPress Enter to continue...")

def showRecentTests():
    """Show recent tests"""
    count = input("\nHow many tests to show? (1-20, default 10): ").strip()
    try:
        count = min(int(count) if count else 10, 20)
    except ValueError:
        count = 10
    
    print(f"\nFetching {count} recent tests...")
    data = getData(f"{API_URL}/tests/recent", {"count": count})
    
    if data:
        print("\n" + "=" * 50)
        print("Recent Tests")
        print("=" * 50)
        
        for test in data[:count]:
            # Convert timestamp to date
            timestamp = test.get('at', 0)
            if timestamp:
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
            else:
                date = "Unknown"
            
            player = test.get('player', {})
            player_name = player.get('name', 'Unknown')
            gamemode = test.get('gamemode', 'Unknown')
            tier = test.get('result_tier', '?')
            pos = "High" if test.get('result_pos') == 0 else "Low"
            
            print(f"\n{date} - {player_name}")
            print(f"  {gamemode}: Now Tier {tier} {pos}")
        
        history.append(f"Viewed recent tests")
    input("\nPress Enter to continue...")

def showHistory():
    """Show user's interaction history"""
    if not history:
        print("\nNo history yet. Do something first!")
    else:
        print("\n" + "=" * 50)
        print("Your History (This Session)")
        print("=" * 50)
        for i, entry in enumerate(history[-20:], 1):
            print(f"{i}. {entry}")
    input("\nPress Enter to continue...")

def makeGraph():
    """Create a graph of top players"""
    count = input("\nHow many players to graph? (5-20, default 10): ").strip()
    try:
        count = min(max(int(count) if count else 10, 5), 20)
    except ValueError:
        count = 10
    
    print(f"\nFetching top {count} players...")
    data = getData(f"{API_URL}/mode/overall", {"count": count})
    
    if data:
        # Create lists for the graph
        names = []
        points = []
        
        for player in data[:count]:
            names.append(player['name'])
            points.append(player.get('points', 0))
        
        # Make the graph
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(names)), points)
        plt.xlabel('Player')
        plt.ylabel('Points')
        plt.title(f'Top {len(names)} Players by Points')
        plt.xticks(range(len(names)), names, rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
        history.append(f"Created graph of top {count} players")
    input("\nPress Enter to continue...")

def showHelp():
    """Show help information"""
    print("\n" + "=" * 50)
    print("Help Guide")
    print("=" * 50)
    print("\nWhat are gamemodes?")
    print("  Different game types like Vanilla, Sword, etc.")
    print("\nWhat are tiers?")
    print("  Tier 1 = Best players, Tier 5 = Lower ranked")
    print("  High/Low = Position within each tier")
    print("\nHow to search?")
    print("  UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
    print("  Username: Current Minecraft Java name")
    print("\nWhat are tests?")
    print("  Tests show when a player's rank changes")
    print("=" * 50)
    input("\nPress Enter to continue...")

def getCount():
    """Get number of results to show"""
    count = input("\nHow many results? (1-50, default 10): ").strip()
    try:
        count = int(count) if count else 10
        if count < 1:
            count = 10
        elif count > 50:
            print("Max is 50, using 50")
            count = 50
        return count
    except ValueError:
        print("Invalid, using 10")
        return 10

def main():
    """Main program loop"""
    print("\nWelcome to MCTiers Rankings Explorer!")
    
    while True:
        showMenu()
        choice = input("Enter choice (0-8): ").strip()
        
        if choice == '0':
            print("\nThanks for using MCTiers Explorer!")
            print(f"You did {len(history)} things this session.")
            break
        elif choice == '1':
            showGamemodes()
        elif choice == '2':
            showOverall()
        elif choice == '3':
            showGamemodeRankings()
        elif choice == '4':
            searchPlayer()
        elif choice == '5':
            showRecentTests()
        elif choice == '6':
            showHistory()
        elif choice == '7':
            makeGraph()
        elif choice == '8':
            showHelp()
        else:
            print("Invalid choice. Enter 0-8.")

# Run the program
if __name__ == "__main__":
    main()