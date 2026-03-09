import feedparser
import requests
import os

# 泛科學的 RSS 網址
RSS_URL = "https://pansci.asia/feed"

# 從環境變數讀取 Webhook URL (這樣才安全！)
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def main():
    print("正在獲取泛科學最新文章...")
    # 讀取 RSS
    feed = feedparser.parse(RSS_URL)
    
    # 如果沒抓到東西就提早結束
    if not feed.entries:
        print("找不到文章！")
        return

    # 抓取最新的一篇文章（清單中的第 0 筆）
    latest_entry = feed.entries[0]
    title = latest_entry.title
    link = latest_entry.link
    
    # 準備傳給 Discord 的資料 (使用 Embed 格式看起來比較專業)
    payload = {
        "content": "🔬 **理科生的每日補充包來囉！**",
        "embeds": [{
            "title": title,
            "url": link,
            "color": 15233582, # 泛科學的橘色色碼
            "author": {
                "name": "PanSci 泛科學"
            }
        }]
    }

    # 把資料推送到你的 Discord Webhook
    if WEBHOOK_URL:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print(f"✅ 成功發送：{title}")
        else:
            print(f"❌ 發送失敗，錯誤碼：{response.status_code}")
    else:
        print("⚠️ 找不到 Webhook 網址，請檢查 GitHub Secrets 設定！")

if __name__ == "__main__":
    main()
