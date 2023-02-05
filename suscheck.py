from pathlib import Path
from urllib.parse import urlparse
import sqlite3

user = str(Path.cwd()).split('\\')[2]
profiles = []
try:
    path = Path(f'C:\\Users\\{user}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
    profiles += [str(f) + '\\places.sqlite' for f in path.iterdir() if f.is_dir()]
except:
    pass
try:
    path = Path(f'C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data')
    profiles += [str(f) + '\\History.sqlite' for f in path.iterdir() if f.is_dir()]
except:
    pass
print(profiles)

visit_count = {}
for profile in profiles:
    # Connect to the "places.sqlite" database
    conn = sqlite3.connect(f'{profile}')
    cursor = conn.cursor()

    # Execute a SQL query to select the URL, title, and visit time from the "moz_places" table

    query = '''
    SELECT * FROM moz_places ORDER BY visit_count ASC
    '''

    try:
        result = cursor.execute(query).fetchall()
        for row in result:
            domain_name = urlparse(row[1]).netloc
            if int(row[4]) > 0:
                if domain_name in visit_count:
                    visit_count[domain_name] += row[4]
                else:
                    visit_count[domain_name] = row[4]
    except sqlite3.OperationalError as e:
        pass
# sort the dictionary by visit count in descending order
sorted_visit_count = {k: v for k, v in sorted(visit_count.items(), key=lambda item: item[1])}

# print the sorted dictionary
for k, v in sorted_visit_count.items():
    if 'e6' in k or 'furaffinity' in k or 'yiff' in k:
        print(f"You're a fuckin furry")
    elif 'python' in k or 'java' in k or 'stackoverflow' in k or 'github' in k:
        print(f"Ahh, a programmer")
    else:
        print(f"You visited {k} {v} times")
# Close the connection to the database
conn.close()
