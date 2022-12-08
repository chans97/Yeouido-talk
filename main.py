from PyPDF2 import PdfFileReader
from dotenv import load_dotenv
import telegram


import os
load_dotenv()

CHAT_ID = os.environ.get('CHAT_ID')
YEOUIDO_TALK = os.environ.get('YEOUIDO_TALK')
# 셀레니움으로 PDF 파일을 받아오기


# PDF 파일에서 파싱
def parse_pdf_to_yeouido_list(filename):
    pdf1 = PdfFileReader(open(filename, 'rb'))
    assm_list = pdf1.pages[0].extractText().split('\n')
    yeouido_list = []
    for assm in enumerate(assm_list):
        if ("여의도" in assm[1]):
            time = assm_list[assm[0]-1][:12]
            location = assm_list[assm[0]-1][12:]
            number = assm_list[assm[0]].split('>')[1].split(' ')[0]
            yeouido_list.append(
                {"time": time, "location": location, "number": number})
    return yeouido_list


yeouido_list = parse_pdf_to_yeouido_list("인터넷집회.pdf")
for yeouido in yeouido_list:
    print(yeouido)


# 텔레그램으로 보내주기
bot = telegram.Bot(token=YEOUIDO_TALK)
text = "12월 9일 여의도 집회 상황 알려드립니다.\n"
text += f"금일 여의도 집회는 {len(yeouido_list)}건 있습니다.\n\n"
for yeouido in yeouido_list:
    text += yeouido['time']
    text += " / "
    text += yeouido['number']
    text += "명 / "
    text += yeouido['location']
    text += "\n"

bot.sendMessage(chat_id=CHAT_ID, text=text)
