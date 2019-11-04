
# 3- Create the needed tables
create_shifts_table_query = """CREATE TABLE shifts (
                                    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                                    user_id INT(10) UNSIGNED NOT NULL,
                                    date DATE NOT NULL,
                                    type ENUM("morning", "night") NOT NULL
                                )"""

my_database.execute(create_shifts_table_query);

create_matches_table_query = """CREATE TABLE matches (
                                    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                                    deadline DATE NOT NULL
                                )"""

my_database.execute(create_matches_table_query);

# 4- commit the tables to database
db_connection.commit()
