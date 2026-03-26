"""
UI Module for MCTiers Application
Handles user interface and display functions
"""

import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Any
from datetime import datetime


class UIManager:
    """Manage user interface and display"""
    
    def __init__(self):
        """Initialize UI manager"""
        self.width = 60
    
    def show_welcome(self):
        """Display welcome message"""
        print("\n" + "=" * self.width)
        print("         MCTiers Data Science Application")
        print("=" * self.width)
        print("Welcome! This app allows you to explore Minecraft")
        print("player rankings from the MCTiers API.")
        print("=" * self.width)
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "-" * self.width)
        print("Main Menu:")
        print("-" * self.width)
        print("1. List all gamemodes")
        print("2. View overall rankings")
        print("3. View gamemode rankings")
        print("4. Search player profile")
        print("5. View test history")
        print("6. View recent tests")
        print("7. View interaction history")
        print("8. Visualise rankings")
        print("9. Help")
        print("0. Exit")
        print("-" * self.width)
    
    def show_help(self):
        """Display help information"""
        print("\n" + "=" * self.width)
        print("Help Guide")
        print("=" * self.width)
        print("\n1. Gamemodes:")
        print("   - These are different game types (Vanilla, Sword, etc.)")
        print("   - Each gamemode has its own rankings")
        print("\n2. Rankings:")
        print("   - Tier 1 = Best players, Tier 5 = Lower ranked players")
        print("   - High (0) and Low (1) positions within each tier")
        print("\n3. Player Search:")
        print("   - UUID format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        print("   - Username: Current Minecraft Java username")
        print("   - Discord ID: Numeric ID (can be found in Discord settings)")
        print("\n4. Tests:")
        print("   - Tests show when a player's ranking changed")
        print("   - Each test shows previous and new rankings")
        print("\n" + "=" * self.width)
        input("\nPress Enter to continue...")
    
    def get_input(self, prompt: str) -> str:
        """Get user input"""
        return input(prompt).strip()
    
    def get_count_input(self, max_val: int = 20) -> Optional[int]:
        """Get count input from user"""
        try:
            count_input = self.get_input("Number of results to show (1-20): ")
            if not count_input:
                return 10
            count = int(count_input)
            if count < 1:
                count = 10
            elif count > max_val:
                print(f"Maximum is {max_val}, using {max_val}")
                count = max_val
            return count
        except ValueError:
            print("Invalid number, using default 10")
            return 10
    
    def show_loading(self, message: str):
        """Show loading message"""
        print(f"\n{message}...")
    
    def show_message(self, message: str):
        """Show general message"""
        print(message)
    
    def show_error(self, error: str):
        """Show error message"""
        print(f"\n[ERROR] {error}")
    
    def display_gamemodes(self, data: Dict):
        """Display gamemodes"""
        print("\n" + "=" * self.width)
        print("Available Gamemodes")
        print("=" * self.width)
        
        for slug, info in data.items():
            print(f"\n[{slug}]")
            print(f"  Title: {info.get('title', 'N/A')}")
            if info.get('info_text'):
                # Show first 100 chars of info text
                text = info['info_text'][:100] + "..." if len(info['info_text']) > 100 else info['info_text']
                print(f"  Info: {text}")
            if info.get('kit_image'):
                print(f"  Kit Image: {info['kit_image']}")
            if info.get('discord_url'):
                print(f"  Discord: {info['discord_url']}")
        
        print("\n" + "=" * self.width)
        input("\nPress Enter to continue...")
    
    def display_gamemode_list(self, data: Dict):
        """Display just the list of gamemode names"""
        print("\nAvailable gamemodes:")
        for slug, info in data.items():
            print(f"  • {slug} - {info.get('title', 'No title')}")
    
    def display_overall_rankings(self, df: pd.DataFrame):
        """Display overall rankings"""
        if df.empty:
            print("\nNo rankings data available.")
            return
        
        print("\n" + "=" * self.width)
        print("Overall Rankings (Top Players by Points)")
        print("=" * self.width)
        
        for idx, row in df.head(20).iterrows():
            print(f"{idx+1:3}. {row['name']:<20} | Points: {row.get('points', 'N/A'):>6} | Region: {row.get('region', '??')}")
        
        print("\n" + "=" * self.width)
        input("\nPress Enter to continue...")
    
    def display_gamemode_rankings(self, data: Dict, gamemode: str):
        """Display gamemode rankings by tier"""
        print("\n" + "=" * self.width)
        print(f"{gamemode.upper()} Rankings by Tier")
        print("=" * self.width)
        
        for tier in ['1', '2', '3', '4', '5']:
            players = data.get(tier, [])
            if players:
                tier_name = "HIGH" if tier in ['1', '2'] else "LOW"
                print(f"\nTier {tier} ({tier_name}):")
                for player in players:
                    pos_text = "High" if player.get('pos') == 0 else "Low"
                    print(f"  • {player['name']:<20} | {pos_text} | Region: {player.get('region', '??')}")
            else:
                print(f"\nTier {tier}: No players")
        
        print("\n" + "=" * self.width)
        input("\nPress Enter to continue...")
    
    def display_player_profile(self, player: Dict):
        """Display player profile"""
        print("\n" + "=" * self.width)
        print(f"Player Profile: {player.get('name', 'Unknown')}")
        print("=" * self.width)
        print(f"UUID: {player.get('uuid', 'N/A')}")
        print(f"Region: {player.get('region', 'N/A')}")
        print(f"Points: {player.get('points', 'N/A')}")
        print(f"Overall Rank: #{player.get('overall', 'N/A')}")
        print(f"Discord ID: {player.get('discord_id', 'Not linked')}")
        
        # Display rankings
        rankings = player.get('rankings', {})
        if rankings:
            print("\nRankings:")
            for gamemode, rank in rankings.items():
                tier = rank.get('tier')
                pos = "High" if rank.get('pos') == 0 else "Low"
                retired = " (Retired)" if rank.get('retired') else ""
                print(f"  • {gamemode}: Tier {tier} {pos}{retired}")
                
                if rank.get('peak_tier'):
                    peak_pos = "High" if rank.get('peak_pos') == 0 else "Low"
                    print(f"    Peak: Tier {rank['peak_tier']} {peak_pos}")
        
        # Display badges
        badges = player.get('badges', [])
        if badges:
            print("\nBadges:")
            for badge in badges[:5]:  # Show first 5 badges
                print(f"  • {badge.get('title', 'Unknown')}: {badge.get('desc', '')[:80]}")
        
        print("\n" + "=" * self.width)
        input("\nPress Enter to continue...")
    
    def display_test_history(self, tests: List[Dict], uuid: str):
        """Display test history"""
        if not tests:
            print("\nNo test history found.")
            return
        
        print("\n" + "=" * self.width)
        print(f"Test History for {uuid}")
        print("=" * self.width)
        
        for test in tests[:20]:
            timestamp = test.get('at', 0)
            if timestamp:
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
            else:
                date = "Unknown"
            
            gamemode = test.get('gamemode', 'Unknown')
            result_tier = test.get('result_tier', '?')
            result_pos = "High" if test.get('result_pos') == 0 else "Low"
            
            prev_tier = test.get('prev_tier')
            prev_pos = test.get('prev_pos')
            
            print(f"\n[{date}] - {gamemode}")
            print(f"  Result: Tier {result_tier} {result_pos}")
            
            if prev_tier:
                prev_pos_text = "High" if prev_pos == 0 else "Low"
                print(f"  Previous: Tier {prev_tier} {prev_pos_text}")
            else:
                print(f"  Previous: New ranking")
            
            if test.get('tester'):
                tester = test['tester'].get('name', 'Unknown')
                print(f"  Tester: {tester}")
        
        print("\n" + "=" * self.width)
        input("\nPress Enter to continue...")
    
    def display_recent_tests(self, tests: List[Dict]):
        """Display recent tests"""
        if not tests:
            print("\nNo recent tests found.")
            return
        
        print("\n" + "=" * self.width)
        print("Recent Tests")
        print("=" * self.width)
        
        for test in tests[:20]:
            timestamp = test.get('at', 0)
            if timestamp:
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
            else:
                date = "Unknown"
            
            player = test.get('player', {})
            player_name = player.get('name', 'Unknown')
            gamemode = test.get('gamemode', 'Unknown')
            result_tier = test.get('result_tier', '?')
            result_pos = "High" if test.get('result_pos') == 0 else "Low"
            
            print(f"\n[{date}] {player_name} -> {gamemode}")
            print(f"  New Ranking: Tier {result_tier} {result_pos}")
        
        print("\n" + "=" * self.width)
        input("\nPress Enter to continue...")
    
    def display_history(self, history: List[str]):
        """Display interaction history"""
        if not history:
            print("\nNo interactions recorded this session.")
            return
        
        print("\n" + "=" * self.width)
        print("Interaction History (Current Session)")
        print("=" * self.width)
        
        for idx, entry in enumerate(history[-20:], 1):
            print(f"{idx:3}. {entry}")
        
        print("\n" + "=" * self.width)
        input("\nPress Enter to continue...")
    
    def display_rankings_chart(self, df: pd.DataFrame):
        """Display rankings bar chart"""
        if df.empty:
            print("\nNo data to visualise.")
            return
        
        # Get top 10 players for visualisation
        top_players = df.head(10)
        
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(top_players)), top_players['points'].values)
        plt.xlabel('Player')
        plt.ylabel('Points')
        plt.title('Top 10 Players by Points')
        plt.xticks(range(len(top_players)), top_players['name'].values, rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    
    def display_search_options(self):
        """Display search options"""
        print("\nSearch Player By:")
        print("1. UUID (e.g., 6553509f-66d3-4041-875f-164236e42e84)")
        print("2. Minecraft Username")
        print("3. Discord ID")