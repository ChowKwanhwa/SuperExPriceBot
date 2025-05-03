Logo
 Logo
Search
General Info
Market Data Endpoints
Summary
Assets
Ticker
Order Book
Trades
General Info
General API Information
The base endpoint is: https://api.superex.com
Market Data Endpoints
24hr Ticker Price Change Statistics
request method: /spot/public/v3/summary

request method: GET

consumes

produces ["*/*"]

Interface description

Parameters

Name	Description	Request Type	Mandatory	Type	schema
No Data			
Response Status:

Status	Description	schema
200	OK	ReturnResult«List«SummaryResponse»»
401	Unauthorized	
403	Forbidden	
404	Not Found	
Response Parameter:

Response


        {
        "code": 200,
        "data": [
           {
            "base_currency": "BTC",
            "base_volume": "7248.4294",
            "highest_bid": "29726.2",
            "highest_price_24h": "30221.2",
            "last_price": "29726.2",
            "lowest_ask": "29726.4",
            "lowest_price_24h": "28670.0",
            "price_change_percent_24h": "1.47",
            "quote_currency": "USDT",
            "quote_volume": "215468262.03028",
            "trading_pairs": "BTC_USDT",
            }
           ],
        "msg": "20001",
        }
    
Name	Description	Type	schema
code		integer(int32)	integer(int32)
data		array	SummaryResponse
   base_currency		string	
   base_volume		string	
   highest_bid		string	
   highest_price_24h		string	
   last_price		string	
   lowest_ask		string	
   lowest_price_24h		string	
   price_change_percent_24h		string	
   quote_currency		string	
   quote_volume		string	
   trading_pairs		string	
msg		string	
Assets
interface address: /spot/public/v3/assets

request method: GET

consumes

produces ["*/*"]

Interface description

Parameters

Name	Description	Request Type	Mandatory	Type	schema
No Data			
Response Status:

Status	Description	schema
200	OK	ReturnResult«JSONObject»
401	Unauthorized	
403	Forbidden	
404	Not Found	
Response Parameter:

Response

{
        "BTC": {
          "can_deposit": "true",
          "can_withdraw": "true",
          "maker_fee": "0.002",
          "max_withdraw": "100.0",
          "min_withdraw": "0.001",
          "name": "Bitcoin",
          "taker_fee": "0.002",
          "unified_cryptoasset_id": "bitcoin"
        },
        "ETH": {
          "can_deposit": "true",
          "can_withdraw": "true",
          "maker_fee": "0.002",
          "max_withdraw": "100.0",
          "min_withdraw": "0.001",
          "name": "Ethereum",
          "taker_fee": "0.002",
          "unified_cryptoasset_id": "ethereum"
        }
}
        
Name	Description	Type	schema
code		integer(int32)	integer(int32)
data		object	
msg		string	
Ticker
request method: /spot/public/v3/ticker

request method: GET

consumes

produces ["*/*"]

Interface description

request parameters

Name	Description	Request Type	Mandatory	Type	schema
No Data			
Response Status:

Status	Description	schema
200	OK	ReturnResult«JSONObject»
401	Unauthorized	
403	Forbidden	
404	Not Found	
Response Parameter:

Response

{
        "BTC_USDT": {
          "base_id": "",
          "base_volume": "7252.3393",
          "isFrozen": "0",
          "last_price": "29754.8",
          "quote_id": "",
          "quote_volume": "215791905.40364"
        },
        "ETH_USDT": {
          "base_id": "",
          "base_volume": "98610.416",
          "isFrozen": "0",
          "last_price": "1972.403",
          "quote_id": "",
          "quote_volume": "194499480.349648"
        }
}
Name	Description	Type	schema
code		integer(int32)	integer(int32)
data		object	
msg		string	
Order Book
request method: /spot/public/v3/orderbook

request method: GET

consumes

produces ["*/*"]

Interface description

Parameters

Name	Description	Request Type	Mandatory	Type	schema
market_pair	BTC_ETH	query	true	string	
depth	depth	query	false	integer	
level	level	query	false	integer	
Response Status:

Status	Description	schema
200	OK	ReturnResult«OrderBookResponse»
401	Unauthorized	
403	Forbidden	
404	Not Found	
Response Parameter:

Response

        
          {
            "asks":[
              [
                "29780.5",
                "0.0072"
              ]
              [
                "29780.6",
                "0.0065"
              ]
            ],
            "bids": [
            [
              "29780.4",
              "0.0517"
            ]
            [
              "29779.9",
              "0.0195"
            ]
            "ticker_id": "",
            "timestamp": "1653471558927"
          }
      
Name	Description	Type	schema
code		integer(int32)	integer(int32)
data		OrderBookResponse	OrderBookResponse
   asks		array	array
   bids		array	array
   ticker_id		string	
   timestamp		string	
msg		string	
Trades
request method: /spot/public/v3/trades

request method: GET

consumes

produces ["*/*"]

Interface description

Parameters

Name	Description	Request Type	Mandatory	Type	schema
market_pair	BTC_ETH	query	true	string	
Response Status:

Status	Description	schema
200	OK	ReturnResult«OrderBookResponse»
401	Unauthorized	
403	Forbidden	
404	Not Found	
Response Parameter:

Response

        
          {
            "code": 200,
            "data": [
              {
                "base_volume": "0.0355",
                "price": "29771.2",
                "quote_volume": "1056.87760",
                "timestamp": "1653471658515",
                "trade_id": "1",
                "type": "sell",
              }
            ],
            "msg": "20001",
          }
        
Name	Description	Type	schema
code		integer(int32)	integer(int32)
data		array	TradesResponse
   base_volume		string	
   price		string	
   quote_volume		string	
   timestamp		string	
   trade_id		string	
   type		string	
msg		string	