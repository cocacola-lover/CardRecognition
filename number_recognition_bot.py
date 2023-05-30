
# Working with bot

import telebot;
import matplotlib.pyplot as plt

import keras_ocr

token = ''
with open('token.txt') as f:
    token = f.read()

# keras-ocr will automatically download pretrained
# weights for the detector and recognizer.
pipeline = keras_ocr.pipeline.Pipeline()

bot = telebot.TeleBot(token)

def downloadFile (message) :
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

def makeAPrediction () :
    images = [
        keras_ocr.tools.read(url) for url in [
            'image.jpg'
        ]
    ]

    prediction_groups = pipeline.recognize(images)

    return prediction_groups

def filterPrediction (prediction) :
    for pair in prediction :

        word = pair[0]
        word = word.replace('o', '0')

        if len(word) == 6 and word.isdigit() :
            return word
    return 'I could not find the number :('



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
        bot.send_message(message.from_user.id, "...")

@bot.message_handler(content_types=['photo'])
def get_image_messages(message):
    
    bot.send_message(message.from_user.id, "Let me think for a second")

    downloadFile(message)
    predictionGroups = makeAPrediction()

    # for prediction in predictionGroups :
    bot.send_message(message.from_user.id, filterPrediction(predictionGroups[0]))
        
    

bot.polling(non_stop=True, interval=1)