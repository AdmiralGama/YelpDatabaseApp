import json
import psycopg2

def cleanStr4SQL(s):
    return s.replace("'","`").replace("\n"," ")

def int2BoolStr (value):
    if value == 0:
        return 'False'
    else:
        return 'True'

def insert2BusinessTable():
    #reading the JSON file
    with open('./yelp_business.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='YelpDB' user='postgres' host='localhost' password='POTestPass123!'")
        except:
            print('Unable to connect to the database!')
            return
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the cussent business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            sql_str = "INSERT INTO business (business_id, name, address,state,city,zipcode,stars,review_count,num_Checkins) " \
            "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(data["name"]) + "','" + cleanStr4SQL(data["address"]) + "','" + \
            cleanStr4SQL(data["state"]) + "','" + cleanStr4SQL(data["city"]) + "','" + cleanStr4SQL(data["postal_code"]) + "'," + str(data["stars"]) + ",0.0,0.0" + ");"
            
            try:
                cur.execute(sql_str)
            except:
                print("Insert to business failed!")
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2ReviewTable():
    #reading the JSON file
    with open('./yelp_review.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='YelpDB' user='postgres' host='localhost' password='POTestPass123!'")
        except:
            print('Unable to connect to the database!')
            return
        cur = conn.cursor()

        while line: #and count_line < 1000: # adding a limit here so it actually finishes before the heat death of the universe :/
            data = json.loads(line)
            # Generate the INSERT statement for the cussent business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            sql_str = "INSERT INTO review (review_id, business_id, review_stars, text, useful_vote, funny_vote, cool_vote) " \
            "VALUES ('" + cleanStr4SQL(data['review_id']) + "','" + cleanStr4SQL(data["business_id"]) + "'," + str(data["stars"]) + ",'" + \
            cleanStr4SQL(data["text"]) + "'," + str(data["useful"]) + "," + str(data["funny"]) + "," + str(data["cool"]) + ");"
            
            try:
                cur.execute(sql_str)
            except:
                print("Insert to review failed!")
                print(sql_str)
            conn.commit()
            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2CheckinTable():
    #reading the JSON file
    with open('./yelp_checkin.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='YelpDB' user='postgres' host='localhost' password='POTestPass123!'")
        except:
            print('Unable to connect to the database!')
            return
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the cussent business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            
            for day in data['time']:
                #print("Day: " + day)
                times = data['time'][day]
                
                for time in times:
                    #print("Time: " + time)
                    count = times[time]
                    #print("Count: " + str(count))

                    sql_str = "INSERT INTO checkin (business_id, day, time, count) " \
                    "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(day) + "','" + cleanStr4SQL(time) + "'," + \
                    str(count) + ");"
                    #print(sql_str)

                    try:
                        cur.execute(sql_str)
                    except:
                        print("Insert to checkin failed!")
                    conn.commit()

            # Example: INSERT INTO checkin (business_id, day, time, count) VALUES ('dwQEZBFen2GdihLLfWeexA', 'Friday', '20:00', 2);

            #try:
            #    cur.execute(sql_str)
            #except:
            #    print("Insert to checkin failed!")
            #conn.commit()

            # optionally you might write the INSERT statement to a file.
            # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

def insert2CategoryTable():
    #reading the JSON file
    with open('./yelp_business.JSON','r') as f:    #TODO: update path for the input file
        #outfile =  open('./yelp_business.SQL', 'w')  #uncomment this line if you are writing the INSERT statements to an output file.
        line = f.readline()
        count_line = 0

        #connect to yelpdb database on postgres server using psycopg2
        #TODO: update the database name, username, and password
        try:
            conn = psycopg2.connect("dbname='YelpDB' user='postgres' host='localhost' password='POTestPass123!'")
        except:
            print('Unable to connect to the database!')
            return
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # Generate the INSERT statement for the cussent business
            # TODO: The below INSERT statement is based on a simple (and incomplete) businesstable schema. Update the statement based on your own table schema and
            # include values for all businessTable attributes
            for category in data["categories"]:
                sql_str = "INSERT INTO category (business_id, category_name) " \
                "VALUES ('" + cleanStr4SQL(data['business_id']) + "','" + cleanStr4SQL(category) + "');"
            
                try:
                    cur.execute(sql_str)
                except:
                    print("Insert to category failed!")
                conn.commit()
                # optionally you might write the INSERT statement to a file.
                # outfile.write(sql_str)

            line = f.readline()
            count_line +=1

        cur.close()
        conn.close()

    print(count_line)
    #outfile.close()  #uncomment this line if you are writing the INSERT statements to an output file.
    f.close()

insert2BusinessTable()
insert2ReviewTable()
insert2CheckinTable()
insert2CategoryTable()