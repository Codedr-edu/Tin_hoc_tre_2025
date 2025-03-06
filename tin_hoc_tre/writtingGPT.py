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


def writting_topic_maker(level, theme, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang kiểm tra kỹ năng viết tiếng anh của học sinh. Bạn hãy tạo ra một đề tài viết để kiểm tra kỹ năng viết ở mức trình độ " + \
        str(level)+" về chủ đề "+str(theme) + \
        ". Hãy chỉ trả về đề bài (đề bài chỉ bao gồm nội dung cần viết) và không trả về bất kỳ thứ gì khác không liên quan."
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


def writting_require_maker(level, title, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang kiểm tra kỹ năng viết tiếng anh của học sinh. Đề bài là"+str(title) + \
        ". Hãy thêm những yêu cầu về bài viết của học sinh, ví dụ như độ dài, số câu, từ ngữ,... Những yêu cầu đó cần phải phù hợp với trình độ " + \
        str(level)+". Hãy chỉ trả về các yêu cầu trong một đoạn văn và không trả về thêm bất kỳ thứ gì khác."
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


def writting_grader(level, title, essay, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang kiểm tra kỹ năng viết tiếng anh của học sinh. Đề bài là"+str(title) + \
        ". Hãy đánh giá bài viết của học sinh theo mức trình độ " + \
        str(level)+". Hãy chỉ trả về câu trả lời 'Đạt' với bài viết đạt tiêu chuẩn của trình độ đã nêu và ngược lại trả về 'Chưa đạt'. Nếu phát hiện bài viết có dấu hiệu đạo văn hay sử dụng AI để viết cũng trả về 'Chưa đạt'.Chỉ đánh giá về khả năng sử dụng tiếng anh với đề bài của học sinh và không kiểm tra, đánh giá sự đúng sai của thông tin có trong bài. Không trả về bất cứ thứ gì không liên quan. Sau đây là bài viết của học sinh: "+str(essay)
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


def writting_reviewer(level, title, essay, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang kiểm tra kỹ năng viết tiếng anh của học sinh. Đề bài là"+str(title) + \
        ". Hãy viết một đoạn đánh giá bài viết của học sinh theo mức trình độ " + \
        str(level)+". Hãy chỉ trả về câu trả lời là một đoạn văn trong đó chỉ rõ những điểm tốt và những điểm cần cải thiện cho học sinh. Nếu phát hiện bài viết có dấu hiệu đạo văn hay sử dụng AI để viết trả về 'Có dấu hiệu đạo văn hoặc sử dụng AI.'. Không trả về bất cứ thứ gì không liên quan. Sau đây là bài viết của học sinh: "+str(essay)
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
def check_content(image, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy đọc và kiểm tra nội dung nhạy cảm nếu chúng xuất hiện trong đoạn văn bản sau: " + \
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
