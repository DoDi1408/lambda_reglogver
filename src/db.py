import logging
import pymysql
import os
import sys


# rds settings
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']


logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.

def connect():
        try:
                return pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
        except pymysql.MySQLError as e:
                logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
                logger.error(e)
                sys.exit(1)
                return e
        
conn = connect()