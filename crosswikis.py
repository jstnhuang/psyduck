import sqlite3
import unicodedata

def getEntityDistribution(dbPath, arg):
  """Gets the entity distribution from Crosswikis for a given arg.
  Args:
    dbPath: The string path to the SQLite3 db file.
    arg: The argument to look up.
  """
  if arg == None or arg == '':
    return []
  arg = getLnrm(arg)
  db = sqlite3.connect(dbPath)
  cursor = db.execute(
    ('SELECT entity, cprob, info from crosswikis '
    'WHERE anchor=? '
    'ORDER BY cprob DESC LIMIT 10000'),
    (arg,)
  ) 
  entities = []
  while True:
    try:
      row = cursor.fetchone()
      if row == None:
        break
      entities.append(dict(
        title=row[0],
        cprob=float(row[1]),
        count=getCount(row[2])
      ))
    except sqlite3.OperationalError:
      continue
  db.close()
  return entities

def getLnrm(arg):
  """Normalizes the given arg by stripping it of diacritics, lowercasing, and
  removing all non-alphanumeric characters."""
  arg = ''.join([
    c for c in unicodedata.normalize('NFD', arg)
    if unicodedata.category(c) != 'Mn'
  ])  
  arg = arg.lower()
  arg = ''.join([
    c for c in arg
    if c in set('abcdefghijklmnopqrstuvwxyz0123456789')
  ])
  return arg

def getCount(info):
  """Given a crosswikis info string, output the count embedded in it."""
  infoParts = info.split(' ')
  labels = ['W:', 'Wx:', 'w:', 'w:']
  count = 0
  for part in infoParts:
    for label in labels:
      if part.startswith(label):
        counts = part[len(label):]
        numerator = int(counts.split('/')[0])
        count += numerator
  return count
