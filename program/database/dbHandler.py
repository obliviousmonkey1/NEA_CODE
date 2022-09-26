import sqlite3

"""
This handles for everything 
so have seperate functions for each database and stuff y
"""

class DBManager:
    def __init__(self, dbPath='') -> None:
        self.conn = sqlite3.connect(dbPath)
    
    def getPopulation(self, mapID):
        c = self.conn.cursor()
        c.execute(f'''
        SELECT *
        FROM Person, Map, Population
        WHERE Map.ID = {mapID} and Map.populationID = Population.id and Person.populationID = Population.id 
        ''')
        return c.fetchall()   
        
    def createPopulationDB(self):
        cTable = '''
        CREATE TABLE IF NOT EXISTS Person(
            ISBN  INTEGER,
            title    TEXT,
            author  TEXT,
            year    TEXT,
            PRIMARY KEY(ISBN)
        );
        '''    
        c = self.conn.cursor()
        c.execute(cTable)
        self.conn.commit()
    
    
    def aBook(self, isbn:int,title:str,author:str,year:str) -> bool:
        iBook = '''
        INSERT INTO Book VALUES
        (?,?,?,?)
        '''
        c = self.conn.cursor()
        try:
            c.execute(iBook, (isbn,title,author,year))
            self.conn.commit()
        except sqlite3.IntegrityError as sqIE:
            print(sqIE)
            return False
        return True 


    def sBooks(self):
        sBooks = '''
            SELECT *
            FROM Book
            '''
        c = self.conn.cursor()
    
        c.execute(sBooks)
        book = c.fetchall()
        return True, book


    def sBook(self ,isbn:int) -> bool:
        sBook = '''
            SELECT *
            FROM Book
            WHERE ? = Book.ISBN
            '''
        c = self.conn.cursor()
    
        c.execute(sBook,(isbn,))
        book = c.fetchone()

        if book == None:
            return False, book
        return True, book


    # Need to refactor this code 
    def uBook(self, isbn:int, type:int, change:str) -> bool:
        t = self.types[type-1]
        uBook = '''
        UPDATE Book 
        SET {0} = '{1}'
        WHERE Book.ISBN = {2};
        '''.format(t,change,isbn)
        c = self.conn.cursor()
        c.execute(uBook)
        self.conn.commit()

        # add error shit

        return True 


    def dBook(self, type:int, change:str):
        t = self.types[type-1]
        if t == 'ISBN':
            change = int(change)
        dBook = '''
        DELETE FROM Book
        WHERE {0} = '{1}'
        '''.format(t,change)  
        c = self.conn.cursor()
        c.execute(dBook)
        self.conn.commit()

        return True 


    def close(self):
        self.conn.close()
        
db = DBManager()

db.close