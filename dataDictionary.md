
---

## dataDictionary.md


# Data Dictionary

## Global Variables

| Variable | Type | What it does |
|----------|------|--------------|
| baseUrl | string | The MCTiers API website address |
| myHistory | list | Stores what the user does during the session |

## Variables in fetchFromApi()

| Variable | Type | What it does |
|----------|------|--------------|
| url | string | The full API address we're calling |
| extra | dict | Extra parameters like count |
| response | object | The API's reply |

## Variables in showTopPlayers()

| Variable | Type | What it does |
|----------|------|--------------|
| howMany | integer | How many players to show (user chooses) |
| data | list | List of player objects from API |
| i | integer | Counter for player position (1,2,3...) |
| player | dict | One player's info (name, points, region) |

## Variables in showModeRankings()

| Variable | Type | What it does |
|----------|------|--------------|
| allModes | dict | All gamemodes from API |
| modeChoice | string | Which gamemode the user picked |
| howMany | integer | Players per tier (user chooses) |
| data | dict | Rankings grouped by tier (1-5) |
| tier | string | Current tier number |
| playersHere | list | Players in this tier |
| player | dict | One player's info |
| tierType | string | "HIGH" for tiers 1-2, "LOW" for 3-5 |
| highLow | string | "High" or "Low" based on pos value |

## Variables in findPlayer()

| Variable | Type | What it does |
|----------|------|--------------|
| choice | string | "1" for UUID search, "2" for username |
| playerId | string | The UUID the user entered |
| playerName | string | The username the user entered |
| urlToUse | string | Full API address for search |
| playerData | dict | Player profile from API |
| theirRankings | dict | Player's rankings in all gamemodes |
| modeName | string | Name of the gamemode |
| rankInfo | dict | Details about their rank |
| tierNum | integer | Their tier number (1-5) |
| highLowPos | string | "High" or "Low" |
| retiredText | string | " (Retired)" or empty |

## Variables in seeRecentTests()

| Variable | Type | What it does |
|----------|------|--------------|
| howManyTests | integer | Number of tests to show |
| testData | list | List of test objects from API |
| oneTest | dict | One test result |
| timeStamp | integer | Unix timestamp from API |
| theDate | string | Readable date and time |
| thePlayer | dict | Player who was tested |
| playerNameHere | string | Player's Minecraft name |
| gameModeHere | string | Which gamemode |
| newTier | integer | Their new tier |
| newPos | string | "High" or "Low" |

## Variables in drawGraph()

| Variable | Type | What it does |
|----------|------|--------------|
| howManyGraph | integer | How many players in the graph |
| graphData | list | Top players from API |
| playerNames | list | Names of players (X-axis) |
| playerPoints | list | Points of players (Y-axis) |
| onePlayer | dict | One player's info |

## Helper Functions

| Function | What it does |
|----------|--------------|
| askHowMany() | Gets count from user, limits to 1-50 |
| printMenu() | Shows the menu options |
| helpMe() | Shows help information |
| seeWhatIDid() | Shows session history |