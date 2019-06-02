import aiohttp
from modules.generators import Database_handler
from modules.checksum import generate_checksum

# creating db handler obj

db = Database_handler()

# <input type="hidden" name="MID" value="rxazcv89315285244163">
# <input type="hidden" name="WEBSITE" value="WEBSTAGING">
# <input type="hidden" name="ORDER_ID" value="order1">
# <input type="hidden" name="CUST_ID" value="cust123">
# <input type="hidden" name="MOBILE_NO" value="7777777777">
# <input type="hidden" name="EMAIL" value="username@emailprovider.com">
# <input type="hidden" name="INDUSTRY_TYPE_ID" value="Retail">
# <input type="hidden" name="CHANNEL_ID" value="WEB">
# <input type="hidden" name="TXN_AMOUNT" value="100.12">
# <input type="hidden" name="CALLBACK_URL" value="https://Merchant_Response_URL>">
# <input type="hidden" name="CHECKSUMHASH" value="ZWdMJOr1yGiFh1nns2U8sDC9VzgUDHVnQpG
# pVnHyrrPb6bthwro1Z8AREUKdUR/K46x3XvFs6Xv7EnoSOLZT29qbZJKXXvyEuEWQIJGkw=">


class Requester:

    def __init__(self, quot_id: str):
        self.data = None
        self.order_id = quot_id
        self.base_url_s = "https://securegw-stage.paytm.in/theia/processTransaction"
        self.base_url_prod = "https://securegw.paytm.in/theia/processTransaction"

    async def template_renderer(self):
        creds = await db.get_creds()
        customer = await db.get_user_info(self.order_id)
        data_template = {
            "MID": creds["MID"],
            "WEBSITE": "WEBSTAGING",
            "ORDER_ID": self.order_id,
            "CUST_ID": customer["customerId"],
            "TXN_AMOUNT": customer["txn_amount"],
            "CALLBACK_URL": "https://pay.sudodevs.com/success",
            "CHANNEL_ID": "WEB",
            "INDUSTRY_TYPE_ID": "Retail"
        }

        checksum = generate_checksum(data_template, creds['merchant_key'])
        data_template.update({"CHECKSUMHASH": checksum})

        self.data = data_template

    async def do_req(self):
        """
        Request the PayTm servers to generate a 
        payment page for the provided data.
        """
        await self.template_renderer()
        async with aiohttp.ClientSession() as session:
            resp = await session.post(self.base_url_s, data=self.data)
            return await resp.text()


