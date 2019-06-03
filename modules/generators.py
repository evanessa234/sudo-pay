import asyncio
import asyncpg
import json

# load config;
# {
#     "user": "",
#     "password": "",
#     "db_name": ""
# }

f = open("config.json", 'r')
config = json.loads(f.read())

# Database handling class


class Database_handler:

    def __init__(self):
        self.cursor = None

    async def initialize_psql(self):
        """
        Initializing the database, similar way used to work
        with Redis.
        """
        self.cursor = await asyncpg.connect(user=config["user"], password=config["password"],
                                            database=config["db_name"], host='127.0.0.1')
        

    async def get_creds(self):
        """
        Fetch the following PayTm credentials
        {
            "MID" : "",
            "merchant_key": "",
        }
        """
        await self.initialize_psql()
        return json.loads(await self.cursor.fetchval("SELECT info from creds"))


    async def get_user_info(self, quot_id: str):
        """
        Retrive user data from the PSQL database.
        MOCK ==>

        {
            "orderId": "succmahdicc", 
            "customerId": "bigdaddysmaldicc", 
            "txn_amount": "999"
        }
        
        """
        return json.loads(await self.cursor.fetchval("SELECT data from customer_info WHERE quot_id=$1", quot_id))

    async def post_user_info(self, user_data: dict,  quot_id: str):
        await self.cursor.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
        await self.cursor.execute("""INSERT INTO customer_info VALUES ($1::json, $2)""", user_data, quot_id)


# Main function
# some noob-ish debugging
# async def main():
#     var = Database_handler()
#     await var.initialize_psql()
#     print(await var.get_user_info("dhsldnss82347nad"))

