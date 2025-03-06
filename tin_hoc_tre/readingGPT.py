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


def reading_maker(level, theme, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang kiểm tra kỹ năng đọc tiếng anh của học sinh. Bạn hãy tạo ra một bài đọc bằng tiếng anh để kiểm tra kỹ năng kỹ năng đọc ở mức trình độ " + \
        str(level)+" về chủ đề "+str(theme) + \
        ". Hãy chỉ trả về bài đọc và không trả về các câu hỏi, tiêu đề hay bất kỳ thứ gì thừa thãi khác không trả về bất kỳ thứ gì khác không liên quan."
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


def reading_title_maker(level, essay, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang kiểm tra kỹ năng đọc tiếng anh của học sinh. Bài đọc: "+str(essay) + \
        ". Hãy tạo ra một tiêu đề để tóm tắt đoạn văn trên bằng tiếng anh. Tiêu đề hãy nêu rõ nội dung tóm tắt của đoạn văn. Hãy chỉ trả lại tiêu đề và không kèm bất kỳ một thông tin không liên quan nào khác."
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


def reading_question_maker(level, essay, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang kiểm tra kỹ năng đọc tiếng anh của học sinh. Bài đọc:"+str(essay) + \
        ". Hãy tạo ra 5 câu hỏi bằng tiếng anh liên quan tới các thông tin trong bài đọc trên với mức trình độ " + \
        str(level)+". Chỉ trả về các câu hỏi được cách dòng với nhau và không trả về bất cứ thứ gì không liên quan."
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


def reading_question_grader(level, question, essay, answer, bot_id=bot_id, url=url, headers=headers):
    prompt = "Hãy tưởng tượng bạn là một giáo viên đang kiểm tra kỹ năng đọc tiếng anh của học sinh. bài đọc là: "+str(essay) + \
        ". Hãy dựa vào thông tin trong đó và kiểm tra câu trả lời của học sinh về câu hỏi " + \
        str(question)+" ở mức trình độ "+str(level)+". Hãy chỉ trả về câu trả lời 'Đạt' với câu trả lời đạt tiêu chuẩn của trình độ và trả lời đúng câu hỏi đã nêu và ngược lại trả về 'Chưa đạt'. Không trả về bất cứ thứ gì không liên quan. Sau đây là câu trả lời của học sinh: "+str(answer)
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
