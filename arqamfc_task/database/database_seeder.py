
# 5- start generating fake data 

# myFactory for generating fake data
myFactory = Faker()


# generate fake data for matches table
for match in range(100):
    deadline = myFactory.date_between_dates(date_start=date(2010, 7, 1), date_end=date(2010, 7, 20))
    
    new_match_query = """INSERT INTO matches 
                            (deadline) VALUES ('{}')""".format(deadline)
                            
    my_database.execute(new_match_query)
    
    db_connection.commit()
    
# generate fake data for shifts table
for shift in range(150):
    if((shift % 2) == 0):
        shift_type = "morning"
    else:
        shift_type = "night"
    
    shift_date = myFactory.date_between_dates(date_start=date(2010, 7, 1), date_end=date(2010, 7, 20))
    
    user_id = myFactory.random_int()
    
    new_shift_query = """INSERT INTO shifts 
                            (user_id, date, type) VALUES ({}, '{}', '{}')""".format(user_id, shift_date, shift_type)
                            
    my_database.execute(new_shift_query)
    
    db_connection.commit()
