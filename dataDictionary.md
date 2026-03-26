# Data Dictionary

## Global Variables

| Variable Name | Data Type | Description | Validation Rules |
|---------------|-----------|-------------|------------------|
| baseUrl | string | Base URL for MCTiers API v2 endpoints | Must be valid HTTPS URL, ends with /api/v2 |
| myHistory | list | Stores user interactions during session | Each entry is string with timestamp format |

## API Response Data Structures

### Gamemode Object
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| slug | string | Unique identifier for the gamemode | "vanilla" |
| title | string | Display name of the gamemode | "Vanilla" |
| info_text | string/null | Markdown description (optional) | "The classic Minecraft experience..." |
| kit_image | string/null | URL to kit example image | "https://example.com/kit.png" |
| discord_url | string/null | Discord invite link | "https://discord.gg/minecraft" |

### Player Object (Overall Rankings)
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| uuid | string | Minecraft UUID (36 chars) | Must match UUID format |
| name | string | Minecraft username | 3-16 chars, alphanumeric |
| region | string | Two-letter region code | NA, EU, SA, AU, ME, AS, AF, ?? |
| points | integer | Total ranking points | >= 0, max 999999 |

### Player Object (Gamemode Rankings)
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| uuid | string | Minecraft UUID | Must match UUID format |
| name | string | Minecraft username | 3-16 chars, alphanumeric |
| region | string | Region code | NA, EU, SA, AU, ME, AS, AF, ?? |
| pos | integer | Position within tier (0=High, 1=Low) | 0 or 1 only |

### Ranking Object
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| tier | integer | Current tier (1-5) | 1 <= tier <= 5 |
| pos | integer | High/Low position | 0 or 1 |
| peak_tier | integer/null | Highest achieved tier | 1 <= peak_tier <= 5 |
| peak_pos | integer/null | Position for peak tier | 0 or 1 |
| attained | integer | Unix timestamp when ranking achieved | > 0 |
| retired | boolean | Whether player is retired | true or false |

### Test Object
| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| player | object | Player who was tested | Contains uuid, name |
| gamemode | string | Gamemode slug | Must exist in /mode/list |
| at | integer | Unix timestamp of test | > 0 |
| result_tier | integer | New tier after test | 1-5 |
| result_pos | integer | New position after test | 0 or 1 |
| prev_tier | integer/null | Previous tier | 1-5 or null |
| prev_pos | integer/null | Previous position | 0 or 1 or null |
| tester | object | Player who conducted test | Contains uuid, name |

## User Input Variables

| Variable | Type | Purpose | Validation |
|----------|------|---------|------------|
| usersPick | string | Menu selection from user | Must be "0"-"8" |
| howMany | integer | Number of results to fetch | 1-50, default 10 |
| modeChoice | string | Gamemode slug to view | Must exist in gamemodes list |
| choice | string | Search type selection | "1" or "2" |
| playerId | string | UUID for player search | UUID format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx) |
| playerName | string | Username for player search | 3-16 chars, alphanumeric |
| howManyTests | integer | Number of tests to show | 1-20, default 10 |
| howManyGraph | integer | Players to include in graph | 5-20, default 10 |

## Program State Variables

| Variable | Type | Purpose | Initial Value |
|----------|------|---------|---------------|
| myHistory | list | Stores user actions | [] |
| running | boolean | Controls main loop | True |
| response | object | HTTP response from API | None |
| data | dict | Parsed JSON response | None |