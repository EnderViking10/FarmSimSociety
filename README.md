# FarmSim Society

FarmSim Society is a Farming Simulator community. The 3 components are the website, discord bot, and FS25 mod

<details>
<summary>Bot</summary>

The bot component of the community

<details>
<summary>Bot commands</summary>

- ## Economy
    - /bank - Shows users bank accont
    - /transfer player user \<username\> amount \<amount\>
    - /transfer server

</details>

<br/>

<details>
<summary>Database Schema</summary>

- users
    - id Integer Primary Key
    - username String
    - discord_id Integer
    - join_date DATETIME DEFAULT DATETIME NOW
    - is_admin Boolean DEFAULT false
    - farm_manager Boolean DEFAULT false
- bank
    - id INTEGER PRIMARY KEY
    - discord_id INTEGER FOREIGN KEY users(discord_id)
    - balance INTEGER default 10000
- servers
    - id INTEGER PRIMARY KEY
    - ip String
    - name String
    - map String
- user_servers
    - user_id Integer
    - server_id Integer
    - PRIMARY KEY (user_id, server_id)
    - FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    - FOREIGN KEY (server_id) REFERENCES servers(id) ON DELETE CASCADE
- properties
  - id Integer primary key
  - property_id integer
  - discord_id INTEGER FOREIGN KEY users(discord_id)
  - server_id INTEGER FOREIGN KEY servers(id)

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
