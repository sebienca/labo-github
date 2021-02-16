import csv, io, os
import sys, getopt,json
import logging
from datetime import datetime
from optparse import OptionParser
from csv import DictReader
import MySQLdb as mdb


def main():

	# First entry in log file
        logging.basicConfig(filename='convertCsvToJson.log',filemode='w',level=logging.DEBUG,format='%(asctime)s -- %(levelname)s -- %(message)s')
        logging.info("version : 1.0.0")
        db_sh = mdb.connect (host="172.30.33.1", user="homeassistant", passwd="genetique95;", db="homeassistant")
        cursor_sh = db_sh.cursor()

        # Check if expected parameters are presents
        #try:
        #    parser = OptionParser("usage: %prog --path <path/to/csvfile>" ,version="%prog 1.0")
        #    parser.add_option("-p", "--path",metavar="/path/to/csv/file.csv", dest="csv_path", help="CSV File to import, give absolute path if needed")
        #    [options, args] = parser.parse_args()
		
        #    if options.csv_path is None:
        #        logging.error ('--path parameter is missing')
        #        parser.error('--path parameter is missing')
		
        #except:
        #        logging.error ('Error Detected...')
        #        exit(1)


        # Check if CSV File exist at the location given
        csvFilePath = 'historique_jours_litres.csv'
        if not os.path.isfile(csvFilePath):
            print("Error : File " + csvFilePath + " is missing")
            logging.error ("File " + csvFilePath + " is missing")
            exit(1)
            logging.info("File Processing is : " + csvFilePath + " - Target Environement is : " + options.env_target)


        # Open CSV File
        with open (csvFilePath,'r') as csvFile:
            reader = csv.reader(csvFile)
            next(reader, None)  # skip the headers
            for row in reader:
                # process each row
                splrow    = row[0].split(";")
                spldatadte   = splrow[0].split(" ")
                datadte = spldatadte[0]
                #datadte    = datetime.strptime(datadte, "%d/%m/%Y").strftime('%Y-%m-%d')
                indexr  = splrow[1]
                datacons = splrow[2]
                datatype  = splrow[3]
                print ("INSERT INTO METRICS_DATA_VEOLIA_LITRES(MetricTimestamp,Indexrel,Litres,Type)    values ('" + datadte + "','" + indexr + "','" + datacons + "','" + datatype + "')")
                sql_sh = "INSERT INTO METRICS_DATA_VEOLIA_LITRES(MetricTimestamp,Indexrel,Litres,Type) values ('" + datadte + "','" + indexr + "','" + datacons + "','" + datatype + "') ON DUPLICATE KEY UPDATE Type=Type"
                try:
                    cursor_sh.execute(sql_sh)
                except:
                    print("error")
                    db_sh.rollback()

        db_sh.commit()




                # Check if CSV File exist at the location given
        csvFilePath = 'historique_jours_Euros €.csv'
        if not os.path.isfile(csvFilePath):
            print("Error : File " + csvFilePath + " is missing")
            logging.error ("File " + csvFilePath + " is missing")
            exit(1)
            logging.info("File Processing is : " + csvFilePath + " - Target Environement is : " + options.env_target)


        # Open CSV File
        with open (csvFilePath,'r') as csvFile:
            reader = csv.reader(csvFile)
            next(reader, None)  # skip the headers
            for row in reader:
                # process each row
                splrow    = row[0].split(";")
                spldatadte   = splrow[0].split(" ")
                datadte = spldatadte[0]
                #datadte    = datetime.strptime(datadte, "%d/%m/%Y").strftime('%Y-%m-%d')
                indexr  = splrow[1]
                dataprice = splrow[2]
                datatype  = splrow[3]
                print ("INSERT INTO METRICS_DATA_VEOLIA_PRICE(MetricTimestamp,Indexrel,Price,Type)    values ('" + datadte + "','" + indexr + "','" + dataprice + "','" + datatype + "')")
                sql_sh = "INSERT INTO METRICS_DATA_VEOLIA_PRICE(MetricTimestamp,Indexrel,Price,Type) values ('" + datadte + "','" + indexr + "','" + dataprice + "','" + datatype + "') ON DUPLICATE KEY UPDATE Type=Type"
                try:
                    cursor_sh.execute(sql_sh)
                except:
                    print("error")
                    db_sh.rollback()

        db_sh.commit()
        db_sh.close()




if __name__ == '__main__':
    main()
