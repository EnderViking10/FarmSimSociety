# FarmSim Society

FarmSim Society is a Farming Simulator community. The 3 components are the website, discord bot, and FS25 mod

<details>
<summary>Database Schema</summary>

- users
    - id INTEGER PRIMARY KEY
    - username STRING
    - discord_id INTEGER
    - join_date DATETIME DEFAULT DATETIME NOW
    - admin BOOLEAN DEFAULT FALSE
    - farm_manager BOOLEAN DEFAULT FALSE
    - balance INTEGER DEFAULT 10000
- servers
    - id INTEGER PRIMARY KEY
    - ip STRING
    - name STRING
    - map STRING
- user_servers
    - user_id INTEGER FOREIGN KEY REFERENCES users(id)
    - server_id INTEGER FOREIGN KEY REFERENCES servers(id)
    - PRIMARY KEY (user_id, server_id)
- properties
    - id INTEGER PRIMARY KEY
    - property_id INTEGER
    - server_id INTEGER FOREIGN KEY servers(id)
    - user_id INTEGER FOREIGN KEY users(id)
    - image STRING
    - size INTEGER
    - price INTEGER
- auction
    - id INTEGER PRIMARY KEY
    - server_id INTEGER FOREIGN KEY REFERENCES servers(id)
    - property_id INTEGER FOREIGN KEY REFERENCES properties(id)
    - cost INTEGER

</details>

<br/>

<details>
<summary>Bot</summary>

The bot component of the community

<details>
<summary>Bot commands</summary>

- ## Economy
    - /bank - Shows users bank account
    - /transfer player user \<username\> amount \<amount\>
    - /transfer server

</details>

<br/>

<details>
<summary>Alembic commands</summary>

```shell
# Create new database revision
alembic revision --autogenerate -m "Description"

# Migrate to new revision
alembic upgrade head

# View history
alembic history
```

</details>

<br/>

<details>
<summary>Requirements</summary>

- aiohappyeyeballs==2.4.3
- aiohttp==3.11.8
- aiosignal==1.3.1
- alembic==1.14.0
- async-timeout==5.0.1
- attrs==24.2.0
- blinker==1.9.0
- certifi==2024.8.30
- charset-normalizer==3.4.0
- click==8.1.7
- discord.py==2.4.0
- Flask==3.1.0
- frozenlist==1.5.0
- greenlet==3.1.1
- idna==3.10
- itsdangerous==2.2.0
- Jinja2==3.1.4
- Mako==1.3.6
- MarkupSafe==3.0.2
- multidict==6.1.0
- propcache==0.2.0
- PyMySQL==1.1.1
- python-dotenv==1.0.1
- requests==2.32.3
- SQLAlchemy==2.0.36
- typing_extensions==4.12.2
- urllib3==2.2.3
- websockets==14.1
- Werkzeug==3.1.3
- yarl==1.18.0

</details>

<br/>

<details>
<summary>Todo</summary>

- Log every command run
    - To channel
    - More verbose
- Add more detail to help command

</details>
</details>

<br/>

<details>
<summary>Website</summary>

The website component of the community

<details>
<summary>Todo</summary>

- Add notification system
    - auction house
    - fix dark mode toggle bar on main

</details>

</details>

<br/>

<details>
<summary>FS25 Mod</summary>

The FS25 mod component of the community

<details>
<summary>Todo</summary>

</details>

</details>

<br/>

<details>
<summary>Database API</summary>

The Database package being used for the server and the bot

<details>
<summary>Todo</summary>

- Add remove_user method
- Make ServerRepository methods
- Make AuctionRepository methods
</details>

<details>
<summary>Docs</summary>

``` python
Class Database
    get_session()

session = from app import session

class UserRepository()
    create_user(session, username, discord_id, admin: False)
    get_user_by_discord_id(session, discord_id)
    get_user_by_id(session, user_id)
    add_money(session, discord_id, amount)
    remove_money(session, discord_id, amount)
    update_username(session, discord_id, username)
    remove_user(session, discord_id)

class AuctionRepository
    create_auction(session, server_id, property_id)
    get_auction_by_id(session, auction_id)
    get_all_auctions(session)
    set_cost(session, cost)

class ServerRepository
    create_server(session, ip, name, map)
    get_server_by_id(session, server_id)
    set_ip(session, server_id, ip)
    set_map(session, server_id, map)
    
class PropertyRepository
    create_property(session, server_id, user_id, property_number, image, size)
    get_property_by_number(session, server_id, property_number)
    set_user(session, server_id, property_number, user_id)
    set_image(session, server_id, property_number, image)
    set_size(session, server_id, property_number, size)
```
</details>

</details>
