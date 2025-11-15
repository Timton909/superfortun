import aiohttp
import asyncio

# Number of requests per JWT token
TOTAL_REQUESTS = 1020

async def send_request(session, jwt_token, proxy):
    url = "https://api.app.superfortune.xyz/beat-villain/beat"
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "cookie": f"access-token={jwt_token}",
        "origin": "https://app.superfortune.xyz",
        "referer": "https://app.superfortune.xyz/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    }
    payload = {"weapon_level": 2}
    
    for _ in range(TOTAL_REQUESTS):
        try:
            async with session.post(url, headers=headers, json=payload, proxy=proxy) as response:
                if response.status == 201:
                    data = await response.json()
                    print(f"Token {jwt_token[:6]}...: Success, Fortune: {data['data']['final_fortune_amount']}")
                else:
                    print(f"Token {jwt_token[:6]}...: Failed, Status: {response.status}")
        except Exception as e:
            print(f"Token {jwt_token[:6]}...: Error: {str(e)}")
        await asyncio.sleep(0.5)  # 0.5s delay between requests

async def main():
    # Read files
    with open("proxy.txt", "r") as f:
        proxies = [line.strip() for line in f if line.strip()]
    with open("jwt.txt", "r") as f:
        jwt_tokens = [line.strip() for line in f if line.strip()]

    # Ensure matching lengths
    min_length = min(len(proxies), len(jwt_tokens))
    proxies = proxies[:min_length]
    jwt_tokens = jwt_tokens[:min_length]

    async with aiohttp.ClientSession() as session:
        tasks = []
        for jwt_token, proxy in zip(jwt_tokens, proxies):
            tasks.append(send_request(session, jwt_token, proxy))
        
        # Run up to 3 accounts in parallel
        for i in range(0, len(tasks), 4):
            await asyncio.gather(*tasks[i:i+4])

if __name__ == "__main__":
    asyncio.run(main())