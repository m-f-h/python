""" persistent-data.py - May 2022 by M.F.Hasler

In a nutshell, this is about how to store data that you have computed in Python 
for use in subsequent sessions. (Obviously, by saving it to some storage medium
in various possible formats, using various possible packages.)

I recently wrote a blog post about using persistent data in Python.
I compared
- SQL databases : MySQL, PostgresQL, MariaDB, SQLite
- dbm style databases: inconvenience: supports only <bytes> as keys and data
  see https://docs.python.org/3/library/dbm.html#module-dbm
- shelves: most convenient. 
  https://docs.python.org/3/library/shelve.html

The latter appears to be the most appropriate for what I need: a knowledge database for an AI assistant I'm developing.

See also Persistent dictionary recipe with widely supported storage formats and having the speed of native dictionaries:
https://code.activestate.com/recipes/576642/
"""
import shelve
with knowledge = open("my_knolwledge_database"):
  # - default option = 'c' = read/write & create if not yet there
  # - additional options: writeback = True:
  #   inefficient: loads *all* into memory an writes back *everything* upon sync() or close().
  #   better do it by hand!
  # - will create a .dir text file which has rows:  'key', (offset,length) 
  #   and a .dat binary datafile which contains the data.
  # NOTE: you MUST call close close() it when done. 

  knowledge['first positive integers'] = [1,2,3] # works
  knowledge['first positive integers'].append( 4 ) # doesn't work without option << writeback = True >>

  tmp = knowledge.get('key', default=[])   # get a copy
  tmp.append( 'something' )                # modify
  knowledge['key'] = tmp                   # write back

while True:
print("I know about the following things:")
for item in knowledge:
  print(item)
