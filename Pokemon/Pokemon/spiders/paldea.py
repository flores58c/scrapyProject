import scrapy
import sqlite3
import csv 

class PaldeaSpider(scrapy.Spider):
    name = "paldea"
    allowed_domains = ["pokemon.fandom.com"]
    start_urls = ["https://pokemon.fandom.com/wiki/Paldea_Pokédex"]

    def parse(self, response):
        connection = sqlite3.connect("paldea.db")

        # table (no. , name, artwork)
        db_table = 'Create table pokemon (no integer primary key ,name text, japanese text, artwork text)'
        cursor = connection.cursor()
        cursor.execute(db_table)
        connection.commit()

        #making csv
        csv_file = open('paldea.csv','w')
        writer = csv.writer(csv_file)
        writer.writerow(['no.','name', 'japanese','art'])

        
       #extract 11 rows of the table [1-11] 
       #index 1 has the headers
        table = response.xpath('//table')[1].xpath('//tbody/tr')

       #loop with header
       #for i in range(1,11):
       
       #for first row:
       #number:table[2].xpath('td/text()')[0].extract()

       #number
       #table[2].xpath('td/text()')[0]

       #japanese name 
       #table[2].xpath('td/text()')[2]

       #art of 2nd
       #table[3].xpath('td/a/img/@data-src').extract()
       
       # first pokemon in english: response.xpath('//table')[1].xpath('//tbody/tr/td/a/text()')[0].extract()
       # it goes up to 399

        firstNum = table[2].xpath('td/text()')[0].extract()
        first_name = response.xpath('//table')[1].xpath('//tbody/tr/td/a/text()')[0].extract()
        jName= table[2].xpath('td/text()')[2].extract()
        #first artwork image response.xpath('//table')[1].xpath('//tbody/tr/td/a/img/@src')[0].extract()

        sprigatitoArt = response.xpath('//table')[1].xpath('//tbody/tr/td/a/img/@src')[0].extract()
       
        query1 = "Insert into pokemon(no ,name,japanese,artwork) values(?,?,?,?)"

        #for sqlite3
        cursor.execute(query1,(firstNum,first_name,jName,sprigatitoArt))
        connection.commit()

        #for csv
        writer.writerow([firstNum,first_name,jName,sprigatitoArt])
 

    
       
        #for first row:
       #number:table[2].xpath('td/text()')[0].extract()

        for i in range(1,9):
            num = table[2+i].xpath('td/text()')[0].extract()

            name = table[3+i].xpath('td/a/text()')[0].extract()

            jName = table[2+i].xpath('td/text()')[2].extract()

            
            art = table[3+i].xpath('td/a/img/@data-src')[0].extract()
                
                
            
            cursor.execute(query1,(num,name,jName,art))
            connection.commit()

            #for csv
            writer.writerow([num,name,jName,art])
        
        


        csv_file.close()
        

        pass
