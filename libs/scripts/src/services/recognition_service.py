import requests
import json


def recognize_wav_file(wav_name, recognize_service_url):

    with open(wav_name, "rb") as binary_file:
        wav_data = bytearray(binary_file.read())

    print("Data saved to {}".format(wav_name))

    try:
        rsp = requests.post(recognize_service_url, data = wav_data)
        print("Response from recognize service {}".format(str(rsp)))
        return json.loads(rsp.text)["text"]
    except Exception as e:
        print(e)
        return "< ERROR > Ошибка в консоле"
