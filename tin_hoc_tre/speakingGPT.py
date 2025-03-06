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


def speaking_scripts_maker(level, theme, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang kiểm tra kỹ năng nói tiếng anh của học sinh. Bạn hãy tạo ra một loạt các câu hỏi bằng tiếng anh để kiểm tra kỹ năng nói ở mức trình độ " + \
        str(level)+" về chủ đề "+str(theme) + \
        ". Hãy thêm các từ nối giữa câu hỏi trước và câu hỏi sau và không trả về số thứ tự của các câu. Hãy chỉ trả về các câu hỏi với các dòng cách nhau và không trả về bất kỳ thứ gì khác không liên quan."
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


def speaking_grader(level, title, essay, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang kiểm tra kỹ năng nói tiếng anh của học sinh. Các câu hỏi nói là"+str(title) + \
        ". Hãy đánh giá bài nói của học sinh theo mức trình độ " + \
        str(level)+". Hãy chỉ trả về câu trả lời 'Đạt' với bài viết đạt tiêu chuẩn và độ chính xác của câu trả lời theo trình độ đã nêu và ngược lại trả về 'Chưa đạt'. Không trả về bất cứ thứ gì không liên quan. Sau đây là bài nói của học sinh:"+str(essay)
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


def speaking_reviewer(level, title, essay, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang kiểm tra kỹ năng nói tiếng anh của học sinh. Các câu hỏi nói là"+str(title) + \
        ". Hãy đánh giá bài nói của học sinh theo mức trình độ " + \
        str(level)+".  Hãy chỉ trả về câu trả lời là một đoạn văn trong đó chỉ rõ những điểm tốt và những điểm cần cải thiện cho học sinh. Không trả về bất cứ thứ gì không liên quan. Sau đây là bài nói của học sinh:"+str(essay)
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
