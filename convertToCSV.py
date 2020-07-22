import sqlite3
from sqlite3 import Error
import ast


def create_connection(db_file):
    """ 
    create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_data(conn):
    """
    Select the column from the table containing all of the user decision data
    :param conn: the Connection object
    :return: array containing data 
    """
    cur = conn.cursor()
    # TODO: The name of the table needs to change here to amt_hit when we actually run the experiment
    cur.execute("SELECT datastring FROM turkdemo")

    data = cur.fetchall()

    print(data)
    return data

def write_to_csv(data):
    """
    Write all of the user data to CSV file
    :param data: array containing the datastrings pulled from the SQL databsae
    :return:
    """

    csv_content = []

    print("Data 0: \n" + str(data[-1]))

    # This loops through each participant's entry
    for entry in data:
   
        if entry[0] is not None:
            # print(entry[0])
            # print(ast.literal_eval(entry[0])["data"])
            entry[0] = ast.literal_eval(entry[0])
            print(type(entry[0]))

            # Handle the special case of the first entry?
            
            for decision in entry[0]['data'][1:]:
                # Find which object was the anchor
                top_shelf_array = decision["trialdata"][0]
                mid_shelf_array = decision["trialdata"][1]
                bottom_shelf_array = decision["trialdata"][2]

                print(top_shelf_array)
                print(mid_shelf_array)
                print(bottom_shelf_array)

def main():
    database = "participants.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        datastring = select_data(conn)
        write_to_csv(datastring)


if __name__ == '__main__':
    main()
