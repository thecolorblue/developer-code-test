import sqlite3
import json

SQL_FILE = "cma-artworks.db"
JSON_FILE = "src/assets/artwork.json"

def encode_difficult_title(title):
  return title.replace('c. ', '&&&c.').replace('ca. ', '&&&ca.').replace('St. ', '&&&St.').replace('Mt. ', '&&&Mt.')

def decode_difficult_title(title):
  return title.replace('&&&c.', 'c. ').replace('&&&ca.', 'ca. ').replace('&&&St.', 'St. ').replace('&&&Mt.', 'Mt. ')

def sql_to_artwork(file):
  response = []
  conn = sqlite3.connect(file)
  conn.row_factory = sqlite3.Row
  db = conn.cursor()
  rows = db.execute('''
    SELECT DISTINCT 
      artwork.accession_number,
      artwork.tombstone,
      artwork.title,
      department.name as department_name, 
      creator.role as creator_role,
      creator.description as creator_description
    FROM artwork
    INNER JOIN (creator INNER JOIN artwork__creator ON creator.id = artwork__creator.creator_id) ON artwork.id = artwork__creator.artwork_id
    INNER JOIN (department INNER JOIN artwork__department ON department.id = artwork__department.department_id) ON artwork.id = artwork__department.artwork_id
  ''').fetchall()

  conn.commit()
  conn.close()

  for row in rows:
    dict_row = dict(row)
    tombstone_parts = encode_difficult_title(row['tombstone']).split('. ')
    creator_parts = row['creator_description'].rsplit('(', 1)

    title_parts = tombstone_parts[0].rsplit(', ', 1)

    if len(creator_parts) > 1:
      creator_meta = creator_parts[1].split(', ')

    if title_parts[1]:
      dict_row['created'] = decode_difficult_title(title_parts[1])

    if tombstone_parts[1]:
      dict_row['creator_full'] = tombstone_parts[1]

    if tombstone_parts[2]:
      dict_row['description'] = decode_difficult_title(tombstone_parts[2])

    dict_row['creator_name'] = creator_parts[0].strip()

    if creator_meta:
      dict_row['creator_region'] = creator_meta[0]
      if len(creator_meta) > 1:
        dict_row['creator_lifetime'] = creator_meta[1].replace(')','')
    
    dict_row['attribution'] = decode_difficult_title('. '.join(tombstone_parts[3:]))

    response.append(dict_row)

  return response

def artwork_to_json(artwork):
  return json.dumps(artwork, sort_keys=True, indent=4)


if __name__ == "__main__":
  artwork = sql_to_artwork(SQL_FILE)
  file = open(JSON_FILE, "w")

  file.write(artwork_to_json(artwork))

  file.close()
