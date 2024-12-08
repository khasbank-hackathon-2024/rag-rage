import requests

def synthesize(text):
    url = "https://api.chimege.com/v1.2/synthesize"
    headers = {
        'Content-Type': 'plain/text',
        'Token': '8a152297c73ab9c38e108ad3493966e54ae52f794634f4e8613f769262d672b6',
    }
    r = requests.post(url, data=text.encode('utf-8'), headers=headers)
    print(r.status_code)
    if r.status_code == 200:
        with open("C:/Users\ohusl\hackathon-xac\core\output.wav", 'wb') as out:
            out.write(r.content)
        return "Synthesis successful, saved to output.wav"
    else:
        return f"Error: {r.status_code} - {r.text}"
