import re
import pymysql
from trend import Trend

class TrendStore:
    def __init__(self, config) -> None:
        self.dbname = config['dbname']
        self.date = config['date']

        try:
            self.mydb = pymysql.connect(
                host=config['host'],       # 数据库主机地址
                port=config['port'],
                user=config['user'],    # 数据库用户名
                password=config['password'],   # 数据库密码
                database=self.dbname,     
            )
        except:
            print("Unable to connect to database")
            pass
        pass

    def __del__(self):
        if self.mydb:
            self.mydb.close()
        pass

    def getTbName(self):
        return 'T' + self.date
    
    def checkTable(self):
        flag = False
        sqlStr = "show tables like '{tbname}'".format(tbname=self.getTbName())
        with self.mydb.cursor() as curs:
            curs.execute(sqlStr)
            data = curs.fetchall()
            if len(data):
                flag = True
        return flag
    
    def createTable(self):
        flag = False
        sqlStrCreateTable = "CREATE TABLE `{dbname}`.`{tbname}` (\
                    `id` INT NOT NULL AUTO_INCREMENT,\
                    `position` INT UNSIGNED NULL,\
                    `title` VARCHAR(63) NOT NULL,\
                    `views` INT UNSIGNED NULL,\
                    `time` INT UNSIGNED NULL,\
                    PRIMARY KEY (`id`),\
                    UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);"\
                    .format(dbname=self.dbname, tbname=self.getTbName())
        try:
            with self.mydb.cursor() as curs:
                curs.execute(sqlStrCreateTable)
                flag = True
                #self.mydb.commit()
        except:
            #self.mydb.rollback()
            print("Error occurred when creating table")
            print(sqlStrCreateTable)
        
        return flag
        
    def logTable(self):
        if len(self.date) > 4:
            year = int(self.date[0:4])
            date = int(self.date[4:])
            sqlStrLogTable = "INSERT INTO `{dbname}`.`recorddates` (`year`, `date`) VALUES ({year}, {date});".format(dbname=self.dbname, year=year, date=date)
            try:
                with self.mydb.cursor() as curs:
                    curs.execute(sqlStrLogTable)
                    self.mydb.commit()
            except:
                self.mydb.rollback()
                print("Error occurred when inserting table log")        
            return True

        return False

    def createAndLog(self):
        if self.checkTable():
            return True
        try:
            if self.createTable():
                self.logTable()
            #self.mydb.commit()
        except:
            #self.mydb.rollback()
            pass
            return False
        return True
    
    def insertTrends(self, trends, time):
        # INSERT INTO `demo`.`T20080426` (`position`, `title`, `views`, `time`) VALUES ('2', 'titlecontent', '1564653', '1805');        
        flag = False
        sqlStrInsertTrend = "INSERT INTO `{dbname}`.`{tbname}` (`position`, `title`, `views`, `time`) VALUES ".format(dbname=self.dbname, tbname=self.getTbName())
        sqlArr = []

        with self.mydb.cursor() as curs:
            try:
                for trend in trends:
                    # myViews = int(re.findall("\d+",trend.getViews())[0])

                    sqlArr.append(" ({position}, '{title}', {views}, {time}) "\
                                        .format(position=trend.getPosition(), \
                                            title=trend.getTitle(), \
                                            views=trend.getViews(), \
                                            time=time))
                sqlStrInsertTrend += ','.join(sqlArr) + ';'
                curs.execute(sqlStrInsertTrend)
                self.mydb.commit()         
                flag = True   
            except:
                self.mydb.rollback()                
                print("Error occured when inserting trends")
                print(sqlStrInsertTrend)
        return flag
        
    


