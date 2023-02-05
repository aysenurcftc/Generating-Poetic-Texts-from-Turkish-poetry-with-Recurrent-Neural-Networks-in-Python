import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Activation, Dropout
from tensorflow.keras.optimizers import RMSprop


filepath = "C:/Users/Lenovo/Desktop/rnnprojem/rnnproje/poetry.txt"
filepath2 = "C:/Users/Lenovo/Desktop/rnnprojem/rnnproje/poetry3.txt"

#kendi oluşturduğum 1012 tane şiirden oluşan text'i kullanıyorum.
text = open(filepath, 'r',encoding='iso-8859-9', errors='ignore').read().lower()
text2 = open(filepath2, 'r',encoding='iso-8859-9', errors='ignore').read().lower()

#Sinir ağını eğitebilmemiz için karakterleri sayısal değerlere dönüştürmemiz
#Ardından bu verilerden tahminlemeden sonra tekrar metne dönüştürebiliriz.
text = text + text2
#metinde geçen karakterlerin sıralanmış bir kümesi. Hiçbir eleman tekrar etmiyor
characters = sorted(set(text))  

char_to_index = dict((c, i) for i, c in enumerate(characters))
index_to_char = dict((i, c) for i, c in enumerate(characters))


#Bir dizinin ne kadar süreceğini ve sonraki cümleye başlamak için kaç karakter 
#gideceğini tanımlıyoruz.

SEQ_LENGTH = 60
STEP_SIZE = 5

sentences = []
next_char = []
"""
#Ağımızın eğitim verileri için tüm cümleleri ve sonraki karakterleri alıyoruz

for i in range(0, len(text) - SEQ_LENGTH, STEP_SIZE):
    sentences.append(text[i: i + SEQ_LENGTH])
    next_char.append(text[i + SEQ_LENGTH])
    
    
    
x = np.zeros((len(sentences), SEQ_LENGTH,
              len(characters)), dtype=np.bool)
y = np.zeros((len(sentences),
              len(characters)), dtype=np.bool)

#Bir karakterin cümle içinde görüldüğü yerde onu true olarak işaretliyoruz.
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_to_index[char]] = 1
    y[i, char_to_index[next_char[i]]] = 1
    

#Building Recurrent Neural Network
    
model = Sequential()

model.add(LSTM(256,return_sequences=True,input_shape=(SEQ_LENGTH,len(characters))))

model.add(Dense(len(characters)))
model.add(Activation('softmax'))


model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))


model.fit(x, y, batch_size=256, epochs=60)


model.save("textgenerator.model")


"""

model = tf.keras.models.load_model("textgenerator.model")

# Helper Function

def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)



#Generating Text


def generate_text(length, temperature):
    start_index = random.randint(0, len(text) - SEQ_LENGTH - 1)
    generated = ''
    sentence = text[start_index: start_index + SEQ_LENGTH]
    generated += sentence
    for i in range(length):
        x_predictions = np.zeros((1, SEQ_LENGTH, len(characters)))
        for t, char in enumerate(sentence):
            x_predictions[0, t, char_to_index[char]] = 1

        predictions = model.predict(x_predictions, verbose=0)[0]
        next_index = sample(predictions,
                                 temperature)
        next_character = index_to_char[next_index]

        generated += next_character
        sentence = sentence[1:] + next_character
    return generated

#Results

print(generate_text(500, 0.2))
print(generate_text(500, 0.4))
print(generate_text(500, 0.5))
print(generate_text(500, 0.6))
print(generate_text(500, 0.7))
print(generate_text(500, 0.8))

