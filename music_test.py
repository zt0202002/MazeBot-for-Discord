# import os
# pw = os.getenv('db_pw')
# print(pw)

from Database.dbloader import *
initialize_db()
dbloader = DBloader()
session = dbloader.db.session
session.add(MusicSQL(mname='test', mlink='test', mtime='test'))
session.commit()