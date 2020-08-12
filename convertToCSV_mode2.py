import sqlite3
from sqlite3 import Error
import ast
import csv


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

    return data

def write_to_csv(data):
    """
    Write all of the user data to CSV file
    :param data: array containing the datastrings pulled from the SQL databsae
    :return:
    """

    csv_content = []

    # print("Data 0: \n" + str(data[-1]))

    # CSV Format:
    # Anchor, All choices, Positive
    # Throw out all cases where we don't have at least one negative and a positive

    num_decisions = 0

    # This loops through each participant's entry
    for entry in data:  
        if entry[0] is not None:
            entry = entry[0].replace("null", "None")

            entry = ast.literal_eval(entry)

            # Handle the special case of the first entry?
            
            for decision in range(3, len(entry["data"])):
                # Find which object was the anchor
                post_decision = entry["data"][decision]["trialdata"]
                pre_decision = entry["data"][decision - 1]["trialdata"]

                top_shelf_array = pre_decision[0]
                mid_shelf_array = pre_decision[1]
                bottom_shelf_array = pre_decision[2]


                if len(post_decision[0]) > len(pre_decision[0]):
                    anchor = post_decision[0][-1]
                elif len(post_decision[1]) > len(pre_decision[1]):
                    anchor = post_decision[1][-1]
                elif len(post_decision[2]) > len(pre_decision[2]):
                    anchor = post_decision[2][-1]
                else:
                    anchor = None

                print(anchor)
                print(top_shelf_array)
                print(mid_shelf_array)
                print(bottom_shelf_array)
                anchor_index = 0 if len(post_decision[0]) > len(pre_decision[0]) else 1 if len(post_decision[1]) > len(pre_decision[1]) else 2
                
		# Decide whether or not this is actually a valid triplet
                has_anchor = anchor is not None
                shelves_all_full = len(top_shelf_array) > 0 and len(mid_shelf_array) > 0 and len(bottom_shelf_array) > 0
                is_valid_sample = has_anchor and shelves_all_full

                if is_valid_sample:
                    for i in range(0, 4):
                        csv_content.append([])

                    csv_content[num_decisions].append(anchor)
                    csv_content[num_decisions + 1].extend(top_shelf_array)
                    csv_content[num_decisions + 2].extend(mid_shelf_array)
                    csv_content[num_decisions + 3].extend(bottom_shelf_array)

                    num_decisions += 4

    # Append to a CSV that already exists
    with open("human_choice_data_mode2.csv", "a") as f:
        csv.writer(f).writerows(csv_content)

def main():
    database = "participants.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        datastring = select_data(conn)
        write_to_csv(datastring)


if __name__ == '__main__':
    main()
