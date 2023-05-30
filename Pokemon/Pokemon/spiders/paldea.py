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
        db_table = 'Create table pokemon (no integer primary key ,name text, artwork text)'
        cursor = connection.cursor()
        cursor.execute(db_table)
        connection.commit()

        #making csv
        csv_file = open('paldea.csv','w')
        writer = csv.writer(csv_file)
        writer.writerow(['no.','name','art'])

        
       
       
       # first pokemon in english: response.xpath('//table')[1].xpath('//tbody/tr/td/a/text()')[0].extract()
       # it goes up to 399
        first_name = response.xpath('//table')[1].xpath('//tbody/tr/td/a/text()')[0].extract()
        #first artwork image response.xpath('//table')[1].xpath('//tbody/tr/td/a/img/@src')[0].extract()

        sprigatitoArt = response.xpath('//table')[1].xpath('//tbody/tr/td/a/img/@src')[0].extract()
       
        query1 = "Insert into pokemon(no ,name,artwork) values(?,?,?)"

        cursor.execute(query1,(1,first_name,sprigatitoArt))
        connection.commit()

        writer.writerow([1,first_name,sprigatitoArt])
       #the rest are in data-src but only 148 available 
       #response.xpath('//table')[1].xpath('//tbody/tr/td/a/img/@data-src')[0]
       #need to skip index by 2
       #table = response.xpath('//table')[1].xpath('//tbody/tr/td/a/img/@data-src')
        
        #trying first 10
        for i in range(0,10):

            name = response.xpath('//table')[1].xpath('//tbody/tr/td/a/text()')[i+1].extract()
            art = response.xpath('//table')[1].xpath('//tbody/tr/td/a/img/@data-src')[i].extract()
      
            
            cursor.execute(query1,(i+2,name,art))
            connection.commit()

            writer.writerow([i+2,name,art])
            

         
        
        


        csv_file.close()
        

        pass
