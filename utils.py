#!/usr/bin/env python3

def db_query(db_connection, query, commit_enabled=False):
    """Runs a query on MySQL DB

    Args:
        db_connection: pymysql.connections.Connection object.
        query: string containing the query to be executed.

    Returns:
        Tuple containing rows with query output, if any.

    Raises:
        ...: TBD
    """
    cursor = db_connection.cursor()

    try:
        cursor.execute(query)
        if commit_enabled:
            db_connection.commit()
            return tuple()
        return cursor.fetchall()

    except Exception as e:
        if commit_enabled:
            db_connection.rollback()
        print(e)
        return tuple()


def wp_get_term_id(db_connection, term_name='', term_slug=''):
    """Gets term_id from term_name or term_slug

    Args:
        db_connection: pymysql.connections.Connection object.
        term_name: user-friendly name (ex. '9:00 - 9:29')
        term_slug: slug (ex. '0900-0929')

    Returns:
        term_id or None in not found
    """

    table = "wp_terms"
    database = "bitnami_wordpress"
    condition = ''

    if len(term_name) > 0:
        condition = "name = '{}'".format(term_name)
    else:
        condition = "slug = '{}'".format(term_slug)

    query = "SELECT term_id FROM {}.{} WHERE {};".format(database, table, condition)

    q_res = db_query(db_connection, query)

    if len(q_res) == 0:
        print("No term with name: '{}' or slug: '{}' found.".format(term_name, term_slug))
        return None
    else:
        return q_res[0][0]


def wp_get_term_taxonomy_id(db_connection, term_id):
    """Gets term_taxonomy_id

    Args:
        db_connection: pymysql.connections.Connection object.
        term_id: term_id

    Returns:
        term_taxonomy_id
    """

    table = "wp_term_taxonomy"
    database = "bitnami_wordpress"

    query = "SELECT term_taxonomy_id FROM {}.{} WHERE term_id = '{}';".format(database, table, term_id)
    q_res = db_query(db_connection, query)

    if len(q_res) == 0:
        print("No taxonomy with term_id: '{}' found.".format(term_id))
        return None
    else:
        return q_res[0][0]


def wp_create_taxonomy(db_connection, term_name, term_slug, taxonomy_type):
    """Creates a new taxonomy

    Args:
        db_connection: pymysql.connections.Connection object.
        term_name: user-friendly name (ex. '9:00 - 9:29')
        term_slug: slug (ex. '0900-0929')
        taxonomy_type: wordpress taxonomy (ex. 'download_category')

    Returns:
        term_taxonomy_id
    """

    database = "bitnami_wordpress"

    # check if term is already present
    term_id = wp_get_term_id(db_connection, term_slug=term_slug)

    if term_id is None:
        # add term
        print("Adding new term name: '{}'.".format(term_name))
        table = "wp_terms"
        query = "INSERT INTO {}.{} (name, slug) \
                VALUES ('{}', '{}');".format(database, table, term_name, term_slug)
        db_query(db_connection, query, commit_enabled=True)
    else:
        print("Term name: '{}' already exists.".format(term_name))

    # get term_id
    term_id = wp_get_term_id(db_connection, term_slug=term_slug)

    # check if taxonomy is already present
    term_taxonomy_id = wp_get_term_taxonomy_id(db_connection, term_id)

    if term_taxonomy_id is None:
        # add taxonomy
        print("Adding a new taxonomy with term_id: '{}'.".format(term_id))
        table = "wp_term_taxonomy"
        query = "INSERT INTO {}.{} (taxonomy, description, term_id) \
                VALUES ('{}', '', '{}');".format(database, table, taxonomy_type, term_id)
        db_query(db_connection, query, commit_enabled=True)
        
        # get created taxonomy id
        term_taxonomy_id = wp_get_term_taxonomy_id(db_connection, term_id)

    else:
        print("A taxonomy with term_id: '{}' already exists.".format(term_id))

    return term_taxonomy_id