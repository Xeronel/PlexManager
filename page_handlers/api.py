from .base import ApiBase
from tornado.escape import json_encode


class Watched(ApiBase):
    def get(self):
        cursor = self.db.cursor()
        cursor.execute(
            """
            SELECT account_id, name, title, view_count, metadata_type, metadata_item_settings.guid
            FROM metadata_item_settings
            JOIN accounts, metadata_items
            WHERE account_id = accounts.id
            AND metadata_item_settings.guid = metadata_items.guid
            AND metadata_type IN (1, 2);
            """
        )
        self.write(json_encode(self.parse_query(cursor.fetchall(), cursor.description)))
        cursor.close()


class Unwatched(ApiBase):
    def get(self):
        cursor = self.db.cursor()
        cursor.execute(
            """
            WITH
                metadata AS (
                    SELECT M1.id, M1.title, M1.metadata_type, M1.guid, M1.title AS parent_name
                    FROM metadata_items M1
                    WHERE parent_id IS NULL
                    UNION ALL
                    SELECT M2.id, M2.title, M2.metadata_type, M2.guid, metadata.parent_name AS parent_name
                    FROM metadata_items M2
                    JOIN metadata
                    ON metadata.id = M2.parent_id
                )
            SELECT title, parent_name, show_type
            FROM metadata
            LEFT JOIN pdb_metadata_types
            ON pdb_metadata_types.id = metadata.metadata_type
            WHERE NOT EXISTS (
                SELECT metadata.guid
                FROM metadata_item_settings M1
                WHERE M1.guid = metadata.guid
            )
            AND metadata_type IN (1, 4)
            """
        )
        self.write(json_encode(self.parse_query(cursor.fetchall(), cursor.description)))
        cursor.close()


class EmptyObject(ApiBase):
    def get(self):
        self.write('{}')
