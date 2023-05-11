import sqlite3
import sys
import xml.etree.ElementTree as ET

# Incoming Pokemon MUST be in this format
#
# <pokemon pokedex="" classification="" generation="">
#     <name>...</name>
#     <hp>...</name>
#     <type>...</type>
#     <type>...</type>
#     <attack>...</attack>
#     <defense>...</defense>
#     <speed>...</speed>
#     <sp_attack>...</sp_attack>
#     <sp_defense>...</sp_defense>
#     <height><m>...</m></height>
#     <weight><kg>...</kg></weight>
#     <abilities>
#         <ability />
#     </abilities>
# </pokemon>



# Read pokemon XML file name from command-line
# (Currently this code does nothing; your job is to fix that!)
if len(sys.argv) < 2:
    print("You must pass at least one XML file name containing Pokemon to insert")
    sys.exit()

conn = sqlite3.connect('pokemon.sqlite')
c = conn.cursor()

for i, xml_file in enumerate(sys.argv):
    # Skip if this is the Python filename (argv[0])
    if i == 0:
        continue

    tree = ET.parse(xml_file)
    root = tree.getroot()

    name = root.find('name').text
    c.execute("SELECT * FROM pokemon WHERE name=?", (name,))
    if c.fetchone() is not None:
        print(f"{name} is already in the database, skipping...")
        continue

    pokedex = root.attrib['pokedex']
    classification = root.attrib['classification']
    generation = root.attrib['generation']
    hp = root.find('hp').text
    types = [t.text for t in root.findall('type')]
    attack = root.find('attack').text
    defense = root.find('defense').text
    speed = root.find('speed').text
    sp_attack = root.find('sp_attack').text
    sp_defense = root.find('sp_defense').text
    height = root.find('height/m').text
    weight = root.find('weight/kg').text
    abilities = [a.text for a in root.findall('abilities/ability')]

    c.execute("INSERT INTO pokemon VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (name, pokedex, classification, generation, hp, ','.join(types), attack, defense, speed,
               sp_attack, sp_defense, f"{height}m/{weight}kg"))
    for ability in abilities:
        c.execute("INSERT INTO abilities VALUES (?, ?)", (name, ability))

    print(f"{name} inserted into the database")

conn.commit()
conn.close()

