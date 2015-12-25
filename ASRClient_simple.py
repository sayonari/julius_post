import requests
url = "http://nishimura-asr.local:8000/asr_julius"
files = {
    'myFile': open('test_16000.wav', 'rb')
}
s = requests.Session()
r = s.post(url, files=files)
print r.text