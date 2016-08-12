from tornado.ioloop import IOLoop as ioloop
import tornado.web
from page_handlers import api, pages
import sqlite3


def make_app():
    return tornado.web.Application(
        [(r'/api/watched', api.Watched),
         (r'/api/unwatched', api.Unwatched),
         (r'/api/empty', api.EmptyObject),
         (r'/', pages.MainHandler)],
        compiled_template_cache=False,
        static_path='web/static',
        template_path='web/templates'
    )


if __name__ == '__main__':
    # Create a new web application
    app = make_app()
    app.listen(9999)

    # Connect to database
    path = '/home/plex/Application Support/Plex Media Server/Plug-in Support/Databases/'
    file = 'com.plexapp.plugins.library.db'
    app.db = sqlite3.connect(path + file, isolation_level=None)

    cursor = app.db.cursor()
    cursor.execute(
    "CREATE TABLE IF NOT EXISTS pdb_metadata_types ("
    "id INT PRIMARY KEY NOT NULL, "
    "show_type VARCHAR(10));"
    )
    cursor.execute(
    "INSERT OR IGNORE INTO pdb_metadata_types (id, show_type) "
    "VALUES (1, 'Movie'), (4, 'TV Episode');"
    )
    app.db.commit()
    cursor.close()
    ioloop.current().start()
