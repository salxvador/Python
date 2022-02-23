import sqlite3
#declare conn variable and open connection:
conn = sqlite3.connect('submission.db')

# Create DB and table structure:
with conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS files (\
        ID INTEGER PRIMARY KEY AUTOINCREMENT,\
        fileName TEXT \
        )")
    conn.commit() #saves the result of the above statement to sqlite
conn.close()

#This tuple will hold the designated file names:
fileList = ('information.docx','Hello.txt','myImage.png',\
            'myMovie.mpg','World.txt','data.pdf','myPhoto.jpg')

#reopen the connection to db:
conn = sqlite3.connect('submission.db')

#Loop throug the array of file names to find the ones that end with '.txt':
for i in fileList:
    if i.endswith('.txt'): #if it's a txt file, add it to db:
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO files (fileName) VALUES (?)", (i,))
            #when inserting i above, need comma after to indicate it is a tuple.
            print(i) #print only the txt files to the console
conn.close() #close connection to db.
