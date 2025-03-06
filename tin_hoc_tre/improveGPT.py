import requests
# import json

# Replace with your actual values
personal_access_token = "pat_XSNlrVHnA3TtGOZIOZhsHJk0YkPEMAvRITqsobgau2QPFep3OJXHajsBHe9U2EBJ"
bot_id = "7470094688335200272"
# yourquery = "Make a polite and short greeting and then introduce about yourself and tell about what you can do"

url = "https://api.coze.com/open_api/v2/chat"

headers = {
    "Authorization": f"Bearer {personal_access_token}",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Host": "api.coze.com",
    "Connection": "keep-alive"
}

'''
def search_image(image, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy đọc và kiểm tra nội dung nhạy cảm nếu chúng xuất hiện trong bức ảnh trong đường link: http://localhost:8000" + \
        str(image)
    data = {
        "conversation_id": "123",
        "bot_id": bot_id,
        "user": "123333333",
        "query": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        # data = json.loads(data)
        # print(data[1]["content"])
        # print(response.json())
        # answer_content = response.json()["content"]
        # print(f"Answer content: {answer_content}")
        for message in data["messages"]:
            if message["type"] == "answer":
                return message["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"
        # print(response.text)
'''


def Writting_improve(review, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang giúp một học sinh cải thiện trình độ tiếng anh. Từ đánh giá của bài writting gần nhất, phân tích kết quả và đánh giá đó và hãy đưa ra những thống kê, đánh giá điểm mạnh và yếu của học sinh rồi từ đó đưa ra lời khuyên, giải pháp để cải thiện khả năng viết của học sinh. Sau đây là đánh giá: " + \
        str(review)+". Hãy chỉ trả về đoạn đánh giá, phân tích, lời khuyên, giải pháp và không trả về bất kỳ thứ gì khác không liên quan."
    data = {
        "conversation_id": "123",
        "bot_id": bot_id,
        "user": "123333333",
        "query": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        # data = json.loads(data)
        # print(data[1]["content"])
        # print(response.json())
        # answer_content = response.json()["content"]
        # print(f"Answer content: {answer_content}")
        for message in data["messages"]:
            if message["type"] == "answer":
                return message["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"
        # print(response.text)


def Speaking_improve(review, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang giúp một học sinh cải thiện trình độ tiếng anh. Từ đánh giá của bài speaking gần nhất,  phân tích kết quả và đánh giá đó và hãy đưa ra những thống kê, đánh giá điểm mạnh và yếu của học sinh rồi từ đó đưa ra lời khuyên, giải pháp để cải thiện khả năng nói của học sinh. Sau đây là đánh giá: " + \
        str(review)+". Hãy chỉ trả về đoạn đánh giá, phân tích, lời khuyên, giải pháp và không trả về bất kỳ thứ gì khác không liên quan."
    data = {
        "conversation_id": "123",
        "bot_id": bot_id,
        "user": "123333333",
        "query": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        # data = json.loads(data)
        # print(data[1]["content"])
        # print(response.json())
        # answer_content = response.json()["content"]
        # print(f"Answer content: {answer_content}")
        for message in data["messages"]:
            if message["type"] == "answer":
                return message["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"
        # print(response.text)


def Listening_improve(review, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang giúp một học sinh cải thiện trình độ tiếng anh. Từ 5 kết quả của bài listening gần nhất, phân tích kết quả đó và hãy đưa ra những thống kê, đánh giá điểm mạnh và yếu của học sinh rồi từ đó đưa ra lời khuyên, giải pháp để cải thiện khả năng nghe của học sinh. Sau đây là 5 kết quả gần nhất: " + \
        str(review)+". Hãy chỉ trả về đoạn đánh giá, phân tích, lời khuyên, giải pháp và không trả về bất kỳ thứ gì khác không liên quan."
    data = {
        "conversation_id": "123",
        "bot_id": bot_id,
        "user": "123333333",
        "query": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        # data = json.loads(data)
        # print(data[0]["content"])
        # print(response.json())
        # answer_content = response.json()["content"]
        # print(f"Answer content: {answer_content}")
        for message in data["messages"]:
            if message["type"] == "answer":
                return message["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"
        # print(response.text)


def Reading_improve(review, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang giúp một học sinh cải thiện trình độ tiếng anh. Từ 5 kết quả của bài reading gần nhất, phân tích kết quả đó và hãy đưa ra những thống kê, đánh giá điểm mạnh và yếu của học sinh rồi từ đó đưa ra lời khuyên, giải pháp để cải thiện khả năng đọc của học sinh. Sau đây là 5 kết quả gần nhất: " + \
        str(review)+". Hãy chỉ trả về đoạn đánh giá, phân tích, lời khuyên, giải pháp và không trả về bất kỳ thứ gì khác không liên quan."
    data = {
        "conversation_id": "123",
        "bot_id": bot_id,
        "user": "123333333",
        "query": prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        # data = json.loads(data)
        # print(data[1]["content"])
        # print(response.json())
        # answer_content = response.json()["content"]
        # print(f"Answer content: {answer_content}")
        for message in data["messages"]:
            if message["type"] == "answer":
                return message["content"]
    else:
        return f"Error: API request failed with status code {response.status_code}"
        # print(response.text)
