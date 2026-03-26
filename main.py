
import requests
import matplotlib.pyplot as plt
from datetime import datetime

baseUrl = "https://mctiers.com/api/v2"
myHistory = []

def getData(url, extra=None):
    """Get data from API with error handling"""
    try:
        r = requests.get(url, params=extra, timeout=10)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 404:
            print("Not found. Check what you typed.")
        else:
            print(f"API error: {r.status_code}")
    except:
        print("Connection error. Check internet.")
    return None

def menu():
    print("\n" + "=" * 50)
    print("     MCTiers Rankings Explorer")
    print("=" * 50)
    print("1. Gamemodes     5. Recent tests")
    print("2. Top players   6. My history")
    print("3. Mode rankings 7. Make graph")
    print("4. Find player   8. Help")
    print("0. Exit")
    print("-" * 50)

def showGamemodes():
    data = getData(f"{baseUrl}/mode/list")
    if data:
        print("\n=== Gamemodes ===")
        for slug, info in data.items():
            print(f"{slug}: {info.get('title', 'No title')}")
        myHistory.append("Viewed gamemodes")
    input("\nPress Enter...")

def showTopPlayers():
    count = getCount()
    if not count: return
    data = getData(f"{baseUrl}/mode/overall", {"count": count})
    if data:
        print(f"\n=== Top {len(data)} Players ===")
        for i, p in enumerate(data, 1):
            print(f"{i:2}. {p['name']:<20} | Points: {p.get('points', 0):>6} | Region: {p.get('region', '??')}")
        myHistory.append(f"Viewed top {count} players")
    input("\nPress Enter...")

def showModeRankings():
    modes = getData(f"{baseUrl}/mode/list")
    if not modes: return
    print("\nGamemodes:", ", ".join(modes.keys()))
    mode = input("Enter gamemode: ").lower().strip()
    if mode not in modes:
        print("Not found")
        return
    count = getCount()
    if not count: return
    data = getData(f"{baseUrl}/mode/{mode}", {"count": count})
    if data:
        print(f"\n=== {mode.upper()} Rankings ===")
        for tier in ['1','2','3','4','5']:
            players = data.get(tier, [])
            if players:
                tierType = "HIGH" if tier in ['1','2'] else "LOW"
                print(f"\nTier {tier} ({tierType}):")
                for p in players:
                    pos = "High" if p.get('pos') == 0 else "Low"
                    print(f"  • {p['name']:<20} | {pos} | {p.get('region', '??')}")
            else:
                print(f"\nTier {tier}: No players")
        myHistory.append(f"Viewed {mode} rankings")
    input("\nPress Enter...")

def findPlayer():
    print("\n1. UUID  2. Username")
    choice = input("Choose: ").strip()
    if choice == '1':
        uid = input("UUID: ").strip()
        if not uid: return
        url = f"{baseUrl}/profile/{uid}"
    elif choice == '2':
        name = input("Username(Try Flowtives, Ferremc, K1rbe): ").strip()
        if not name: return
        url = f"{baseUrl}/profile/by-name/{name}"
    else:
        return
    data = getData(url)
    if data and 'error' not in data:
        print(f"\n=== {data.get('name', 'Unknown')} ===")
        print(f"UUID: {data.get('uuid', 'N/A')}")
        print(f"Region: {data.get('region', 'N/A')}")
        print(f"Points: {data.get('points', 0)}")
        print(f"Overall Rank: #{data.get('overall', 'N/A')}")
        if data.get('rankings'):
            print("\nRankings:")
            for mode, r in data['rankings'].items():
                tier = r.get('tier')
                pos = "High" if r.get('pos') == 0 else "Low"
                retired = " (Retired)" if r.get('retired') else ""
                print(f"  • {mode}: Tier {tier} {pos}{retired}")
        myHistory.append(f"Searched: {data.get('name')}")
    else:
        print("Player not found")
    input("\nPress Enter...")

def seeRecentTests():
    count = input("How many tests? (1-20, default 10): ").strip()
    try:
        count = min(int(count) if count else 10, 20)
    except:
        count = 10
    data = getData(f"{baseUrl}/tests/recent", {"count": count})
    if data:
        print("\n=== Recent Tests ===")
        for t in data[:count]:
            date = datetime.fromtimestamp(t.get('at', 0)).strftime('%Y-%m-%d %H:%M') if t.get('at') else "Unknown"
            p = t.get('player', {})
            name = p.get('name', 'Unknown')
            mode = t.get('gamemode', 'Unknown')
            tier = t.get('result_tier', '?')
            pos = "High" if t.get('result_pos') == 0 else "Low"
            print(f"\n{date} - {name}")
            print(f"  {mode}: Now Tier {tier} {pos}")
        myHistory.append("Viewed recent tests")
    input("\nPress Enter...")

def seeHistory():
    if not myHistory:
        print("\nNo history yet.")
    else:
        print("\n=== Your History ===")
        for i, h in enumerate(myHistory[-20:], 1):
            print(f"{i}. {h}")
    input("\nPress Enter...")

def drawGraph():
    count = input("How many players? (5-20, default 10): ").strip()
    try:
        count = min(max(int(count) if count else 10, 5), 20)
    except:
        count = 10
    data = getData(f"{baseUrl}/mode/overall", {"count": count})
    if data:
        names = [p['name'] for p in data[:count]]
        points = [p.get('points', 0) for p in data[:count]]
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(names)), points)
        plt.xlabel('Player')
        plt.ylabel('Points')
        plt.title(f'Top {len(names)} Players')
        plt.xticks(range(len(names)), names, rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        myHistory.append(f"Made graph of top {count} players")
    input("\nPress Enter...")

def helpMe():
    print("\n" + "=" * 50)
    print("Help Guide")
    print("=" * 50)
    print("\nTiers: 1=Best, 5=Lowest")
    print("High/Low = Position within tier")
    print("UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
    print("Tests show when a player's rank changed")
    print("=" * 50)
    input("\nPress Enter...")

def getCount():
    try:
        c = input("\nHow many? (1-50, default 10): ").strip()
        c = int(c) if c else 10
        if c < 1: c = 10
        if c > 50: 
            print("Max 50")
            c = 50
        return c
    except:
        return 10

def start():
    print("\nWelcome to MCTiers Rankings Explorer!")
    while True:
        menu()
        choice = input("Choice (0-8): ").strip()
        if choice == '0':
            print(f"\nThanks! You did {len(myHistory)} things.")
            break
        elif choice == '1': showGamemodes()
        elif choice == '2': showTopPlayers()
        elif choice == '3': showModeRankings()
        elif choice == '4': findPlayer()
        elif choice == '5': seeRecentTests()
        elif choice == '6': seeHistory()
        elif choice == '7': drawGraph()
        elif choice == '8': helpMe()
        else: print("Invalid choice")

if __name__ == "__main__":
    start()