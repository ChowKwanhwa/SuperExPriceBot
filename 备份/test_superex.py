import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
from typing import Dict, Optional
from datetime import datetime
import socket

class SuperExAPI:
    def __init__(self):
        self.base_url = "https://api.superex.com"
        # 禁用SSL验证警告
        requests.packages.urllib3.disable_warnings()
        
        # 创建会话并配置重试策略
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.verify = False

    def _make_request(self, url: str, headers: Dict) -> requests.Response:
        """
        发送HTTP请求的辅助方法
        """
        # 强制使用IPv4
        original_has_ipv6 = requests.packages.urllib3.util.connection.HAS_IPV6
        requests.packages.urllib3.util.connection.HAS_IPV6 = False
        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=10,
                proxies={'http': None, 'https': None}  # 禁用代理
            )
            return response
        finally:
            requests.packages.urllib3.util.connection.HAS_IPV6 = original_has_ipv6

    def get_market_summary(self, symbol: str = "BTC_USDT") -> Dict:
        """
        获取市场摘要信息
        Args:
            symbol: 交易对，例如 "BTC_USDT"
        Returns:
            包含价格信息的字典
        """
        try:
            url = f"{self.base_url}/spot/public/v3/summary"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            
            print(f"Requesting summary from {url}")
            response = self._make_request(url, headers)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("Summary data:", json.dumps(data, indent=2))
                
                if data.get("code") == 200 and "data" in data:
                    for pair_info in data["data"]:
                        if pair_info["trading_pairs"] == symbol:
                            return {
                                "symbol": symbol,
                                "last_price": float(pair_info["last_price"]),
                                "24h_high": float(pair_info["highest_price_24h"]),
                                "24h_low": float(pair_info["lowest_price_24h"]),
                                "24h_volume": float(pair_info["base_volume"]),
                                "24h_change": float(pair_info["price_change_percent_24h"])
                            }
                    return {"error": f"Trading pair {symbol} not found"}
                else:
                    return {"error": f"API error: {data.get('msg', 'Unknown error')}"}
            else:
                return {"error": f"HTTP error: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"error": f"JSON decode error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    def get_ticker(self, symbol: str = "BTC_USDT") -> Dict:
        """
        获取ticker信息
        Args:
            symbol: 交易对，例如 "BTC_USDT"
        Returns:
            包含价格信息的字典
        """
        try:
            url = f"{self.base_url}/spot/public/v3/ticker"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            
            print(f"\nRequesting ticker from {url}")
            response = self._make_request(url, headers)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("Ticker data:", json.dumps(data, indent=2))
                
                if data.get("code") == 200 and symbol in data.get("data", {}):
                    ticker_data = data["data"][symbol]
                    return {
                        "symbol": symbol,
                        "last_price": float(ticker_data["last_price"]),
                        "base_volume": float(ticker_data["base_volume"]),
                        "quote_volume": float(ticker_data["quote_volume"]),
                        "is_frozen": ticker_data["isFrozen"]
                    }
                else:
                    return {"error": f"Trading pair {symbol} not found or API error: {data.get('msg', 'Unknown error')}"}
            else:
                return {"error": f"HTTP error: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"error": f"JSON decode error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()

def main():
    api = SuperExAPI()
    
    # 测试BTC/USDT交易对的两个端点
    print("\nTesting SuperEx API for BTC/USDT:")
    
    # 测试summary端点
    print("\n1. Testing summary endpoint:")
    summary_result = api.get_market_summary("BTC_USDT")
    print(json.dumps(summary_result, indent=2))
    
    # 测试ticker端点
    print("\n2. Testing ticker endpoint:")
    ticker_result = api.get_ticker("BTC_USDT")
    print(json.dumps(ticker_result, indent=2))

if __name__ == "__main__":
    # 强制使用IPv4
    socket.setdefaulttimeout(10)
    requests.packages.urllib3.util.connection.HAS_IPV6 = False
    main()
