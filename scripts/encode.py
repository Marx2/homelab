from pykeepass import PyKeePass
# load db
kp = PyKeePass('db.kdbx', password='somePassw0rd')
# find any group by its name
group = kp.find_groups(name='social', first=True)

# get the entries in a group
group.entries

# find any entry by its title
entry = kp.find_entries(title='facebook', first=True)