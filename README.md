# Sequence diagrams
The number between brackets represents the message code. Some messages have a value between parentheses at the end, that represents an internal code/value for that message.

- [Login Server](#login-server)
    - [Authentication](#authentication)
        - [Login](#login)
- [Game Server](#game-server)
    - [Authentication](#authentication-1)
        - [Login](#login-1)
        - [Logout](#logout)
    - [Switch to stage on same server](#switch-to-stage-on-same-server)
        - [Disconnect](#disconnect)
        - [Connect](#connect)
    - [Switch to stage on different server](#switch-to-stage-on-different-server)
        - [Disconnect](#disconnect-1)
        - [Connect](#disconnect-1)
    - [Chat](#chat)
        - [Say](#say)
        - [Whisper](#whisper)
        - [Say to channel](#say-to-channel)
    - [Inventory](#inventory)
        - [Move](#move)
        - [Split](#split)
        - [Destroy](#destroy)
        - [Use (consumables)](#use-consumables)
    - [Interactions](#interactions)
        - [Talk to NPC](#talk-to-npc)
        - [Get HP](#get-hp)
        - [Attack](#attack)
        - [Move](#move)
# Login server
## Authentication
### Login
```mermaid
sequenceDiagram
    participant Client
    participant Login server
    participant Other client
    Client-)Login server: [2] Authenticate
    break invalid user password
    Login server-)Client: [0] Authentication error (152)
    Login server-)Client: FIN
    end
    break account is logged in
    Login server-)Client: [0] Authentication error (161)
    Login server-)Client: FIN
    alt on login server
    Login server-)Other client: [0] Authentication error (161)
    else on game server
    Login server-)Other client: [13] System log (161)
    end
    Login server-)Other client: FIN
    end
    opt has announcement
    Login server-)Client: [12] Announcement
    end
    Login server-)Client: [0] Character list
```
# Game server
## Authentication
### Login
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Client-)Game server: [2] Authenticate
    Client-)Game server: [3] Empty message
    break invalid data
    Game server-)Client: [0] Error (167)
    Game server-)Client: FIN
    end
    opt is in league
    Game server-)Other client: [292] Member detail
    end
    opt is in area of interest
    Game server-)Other client: [1] Player
    end
    opt is friend
    Game server-)Other client: [40] Friend detail
    end
    Game server-)Client: [2] Character
    Game server-)Client: [91] Function bar
    Game server-)Client: [26] Inventory
    Game server-)Client: [93] Server timestamp
    loop entities
    Game server-)Client: [1] Player
    Game server-)Client: [8] NPC
    Game server-)Client: [14] Object
    end
    loop entities dynamic state
    Game server-)Client: [29] Update player
    end
    Game server-)Client: [92] Acquired emotes
    Game server-)Client: [305] Leagues territories
    Game server-)Client: [39] Friends
    loop connected friends
    Game server-)Client: [40] Friend detail
    end
    Game server-)Client: [341] Achievements
    Game server-)Client: [329] House information
    Game server-)Client: [366] Online reward
```


### Logout
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Game server-)Client: FIN
    opt is in area of interest
    Game server-)Other client: [7] Remove entity (1)
    end
    opt is in team
    Game server-)Other client: [37] Leaves team (4)
    end
    opt is in league
    Game server-)Other client: [293] Member disconnected
    end
    opt is friend
    Game server-)Other client: [46] Friend disconnected
    end
```
---
## Switch to stage on same server
### Disconnect
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Game server-)Client: [12] Redirect to server (only stage is set)
    opt is in area of interest
    Game server-)Other client: [7] Remove entity
    end
```
### Connect
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Client-)Game server: [9] Empty message
    Game server-)Client: [20] Unknown message
    Game server-)Client: [2] Character
    Game server-)Client: [92] Acquired emotes
    Game server-)Client: [91] Function bar
    Game server-)Client: [26] Inventory
    loop entities
    Game server-)Client: [1] Player
    Game server-)Client: [8] NPC
    Game server-)Client: [14] Object
    end
    loop entities dynamic state
    Game server-)Client: [29] Update player
    end
    Game server-)Client: [341] Achievements
    Game server-)Client: [329] House information
    opt is in area of interest
    Game server-)Other client: [1] Player
    end

```
---
## Switch to stage on different server
### Disconnect
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Game server-)Client: [12] Redirect to server
    Client-)Game server: [232] Empty message
    Game server-)Client: FIN
    opt is in area of interest
    Game server-)Other client: [7] Remove entity
    end
```

### Connect
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Client-)Game server: [2] Authenticate
    Client-)Game server: [3] Empty message
    opt is in area of interest
    Game server-)Other client: [1] Player
    end
    opt is friend
    Game server-)Other client: [40] Friend detail
    end
    Game server-)Client: [2] Character
    Game server-)Client: [92] Acquired emotes
    Game server-)Client: [91] Function bar
    Game server-)Client: [26] Inventory
    loop entities
    Game server-)Client: [1] Player
    Game server-)Client: [8] NPC
    Game server-)Client: [14] Object
    end
    loop entities dynamic state
    Game server-)Client: [29] Update player
    end
    Game server-)Client: [39] Friends
    loop connected friends
    Game server-)Client: [40] Friend detail
    end
    Game server-)Client: [341] Achievements
    Game server-)Client: [329] House information
    Game server-)Client: [366] Online reward
```
---

## Chat
### Say
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Client-)Game server: [14] Say
    Game server-)Client: [23] Said
    opt is in area of interest
    Game server-)Other client: [23] Said
    end
```

### Whisper
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Client-)Game server: [295] Whisper
    alt valid target
    Game server-)Client: [295] Whispers
    Game server-)Other client: [295] Whispers
    else invalid target
    Game server-)Client: [295] Whispers (error)
    end
```

The first value of `Whisper` seems to be static and unused.
The `Whispers` first field is the receptor of the event, the source player for Client and the destination player for Other client.

### Say to channel
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Client-)Game server: [294] Send channel message
    opt is member of channel
    Game server-)Client: [294] Channel message
    Game server-)Other client: [294] Channel message
    end
    
```
---

## Inventory
### Move
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Client-)Game server: [18] Move slot
    Game server-)Client: [27] Update slots (src and dst)
    opt src or dst is equipment
    Game server-)Client: [66] Update stats
    opt is in area of interest
    Game server-)Other client: [29] Update player (1)
    end
    end
```

The `Update slots` message contains the state of the source and destination slots.


If the destination slot is empty, then becomes the slot for the item, and source becomes an empty slot.


If the destination slots contains the same item (code) and is quantifiable, then the slots are merged and the source becomes an empty slot.


If the destination slots contains a different item, then the slots are swapped.


### Split
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    Client-)Game server: [47] Split slot
    Game server-)Client: [27] Update slots (src and dst) (dst new item)
```

The `Update slots` message contains the state of the source and destination slots. The destination slot is a new item (new id) containing the specified amount of items. The source is updated with the remaining amount.


### Destroy
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Client-)Game server: [19] Destroy item
    Game server-)Client: [19] Unknown message
    Game server-)Client: [27] Update slot (src)
    opt destroy src is equipment
    Game server-)Client: [66] Update stats
    opt is in area of interest
    Game server-)Other client: [29] Update player (1)
    end
    end
```

### Use (consumables)
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Client-)Game server: [46] Use item in slot
    Game server-)Client: [27] Update slot (src)
    Game server-)Client: [66] Update stats
    opt is in area of interest
    Game server-)Other client: [29] Update player (4)
    end
```

---

## Interactions

### Talk to NPC


```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Client-)Game server: [7] Unknown (2)
    Client-)Game server: [5] Interact with NPC (0)
    Game server-)Client: [3] Fix to coords
    opt is in area of interest
    Game server-)Other client: [3] Fix to coords
    end
    Game server-)Client: [18] Show dialog
    opt has options
    Client-)Game server: [11] Select option (n)
    Game server-)Client: [18] Show dialog
    end
    Client-)Game server: [11] Close dialog (1)
```


### Get HP
```mermaid
sequenceDiagram
    participant Client
    participant Game server
    Client-)Game server: [22] Request (12)
    Game server-)Client: [19] Update NPC (1)
```

This is triggered when the player right clics a monster or enters a fight.
This is a single event, the client makes multiple requests.

### Attack

```mermaid
sequenceDiagram
    participant Client
    participant Game server
    Client-)Game server: [7] Unknown (X)
    Client-)Game server: [5] Interact with NPC (0)
    Game server-)Client: [10] Basic attack
    Game server-)Client: [19] Update NPC (1)
```

The value of message [7] seems to be between 0 and 7.

### Move

```mermaid
sequenceDiagram
    participant Client
    participant Game server
    participant Other client
    Client-)Game server: [4] Move
    Game server-)Client: [5] Moved
    opt is in area of interest
    Game server-)Other client: [5] Moved
    end
    
```