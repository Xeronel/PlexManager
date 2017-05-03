from tornado.ioloop import IOLoop as ioloop
import tornado.web
from page_handlers import api, pages
import sqlite3
import config
import os
import logging
from systemd import journal


def make_app():
    return tornado.web.Application(
        [(r'/api/watched', api.Watched),
         (r'/api/unwatched', api.Unwatched),
         (r'/api/added_episodes', api.AddedEpisodes),
         (r'/api/empty', api.EmptyObject),
         (r'/', pages.MainHandler),
         (r'/requests', pages.Requests)],
        compiled_template_cache=config.web.compiled_template_cache,
        static_path='web/static',
        template_path='web/templates',
        debug=True if config.logging.level == logging.getLevelName('DEBUG') else False
    )


if __name__ == '__main__':
    # Setup logging facilities
    if config.logging.stdout:
        logging.basicConfig(format="[%(filename)s:%(lineno)s %(funcName)s()] %(message)s")
    else:
        logging.basicConfig(format="[%(filename)s:%(lineno)s %(funcName)s()] %(message)s",
                            stream=open(os.devnull, 'w'))
    root_log = logging.getLogger()
    root_log.propagate = True
    root_log.setLevel(config.logging.level)
    log = logging.getLogger('page_handlers')
    log.propagate = True
    if config.logging.journald:
        log.addHandler(journal.JournalHandler())

    # Create a new web application
    app = make_app()
    app.listen(config.web.host_port)

    # Connect to database
    file = 'com.plexapp.plugins.library.db'
    app.db = sqlite3.connect(os.path.join(config.db.path, file), isolation_level=None)

    cursor = app.db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pdb_metadata_types (
        id INT PRIMARY KEY NOT NULL,
        show_type VARCHAR(10));
        """
    )
    cursor.execute(
        """
        INSERT OR IGNORE INTO pdb_metadata_types (id, show_type)
        VALUES (1, 'Movie'), (4, 'TV Episode');
        """
    )
    app.db.commit()
    cursor.close()
    ioloop.current().start()
