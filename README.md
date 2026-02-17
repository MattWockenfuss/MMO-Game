# MMO-Game
Distributed System MMO

Massive Multiplayer Online Game Prototype with automatic server assignment, load balancing, player collision detection, and an expandable entity interface.
Our system is robust. New tiles, entities, and worlds containing the aforementioned can be added without much effort or technical ability. The dataserver for example, reads world data from an intuitive .png image.

<table>
  <tr>
    <td>Before</td>
    <td>After</td>
  </tr>
  <tr>
    <td><img width="987" height="621" alt="3" src="https://github.com/user-attachments/assets/d2a5800f-7102-48b4-94a5-6da6fe2b86ea" /></td>
    <td><img width="1714" height="887" alt="2" src="https://github.com/user-attachments/assets/ce56be5b-45d6-4dba-a885-3c9ca3d5821a" /></td>
  </tr>
</table>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Here are a few snippets of our servers live, during this playtest we had 11 servers online, each with distinct responsibilities. A data server acted as the storage backend, holding all of the data for player login (just their username for our small test), all of the tiles present, the entities, and static entities present, as well as all of the worlds that are comprised of the tiles and entities. The communications server acted as the bridge when connecting to new servers, load balancing, as well as user login. The world server handles player and entity movement, and also stores its appropriate tileset internally.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;During our test, our 11 servers were running in a linux environment on professional servers we paid for, and had no experience with disruptions on lag. As briefly mentioned previously, this system is design for rapid expandability without technical knowledge. Therefore, the backend data server will scan within its directories and compile all of the provided assets for use later. <b>This allows for the addition of new worlds, entities, static entities, and tiles without touching a single line of code! </b>


<img width="523" height="295" alt="1" src="https://github.com/user-attachments/assets/a5d7f382-7359-4a50-88be-4482c8a4487f" />
<img width="625" height="274" alt="6" src="https://github.com/user-attachments/assets/305fc099-a9f8-404d-9f92-cea3d4d53d93" />

<img width="1099" height="767" alt="5" src="https://github.com/user-attachments/assets/3ab38857-93bd-4928-9b75-5ffd34be9402" />

<img width="2048" height="1021" alt="4" src="https://github.com/user-attachments/assets/8254f246-d3ac-4313-87d7-3d680febc940" />
<img width="2048" height="1090" alt="7" src="https://github.com/user-attachments/assets/c490e708-ba7c-46ad-98d2-25d185036144" />

