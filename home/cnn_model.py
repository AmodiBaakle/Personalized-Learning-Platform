import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential, load_model
from keras.layers import Dense, Conv2D, Flatten
import pickle
from .models import interface_data

def create_model():
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(13,)))  
    model.add(Dense(32, activation='relu'))
    model.add(Dense(3, activation='softmax'))  
    return model

student_data = pd.read_csv("./static/person_dataset.csv")
student_data.fillna(0, inplace=True)
input_cols = ['content_stay_gfg', 'content_visit_gfg', 'video_play_youtube', 'video_visit_youtube',
              'question_remember', 'question_understanding', 'question_application', 'question_analysis',
              'question_evaluation', 'self_assess_stay', 'self_assess_visit', 'content_stay_w3school',
              'content_visit_w3school']
target_cols = ['preference_gfg', 'preference_w3school', 'preference_youtube']
X = student_data[input_cols].values
y = student_data[target_cols].values
scaler = StandardScaler()
X = scaler.fit_transform(X)
model = create_model()
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=8, batch_size=32, validation_split=0.2)
model.save('./static/model.keras')
with open('./static/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

website_names = ['GFG', 'W3Schools', 'Youtube']

def createe_model():
    model = Sequential()
    model.add(Conv2D(64, activation='relu', input_shape=(13,)))
    model.add(Dense(64, activation='relu', input_shape=(13,)))  
    model.add(Flatten(32, activation='relu'))
    model.add(Dense(3, activation='softmax'))  
    return model

def get_top_websites(prediction, website_names):
    website_weights = list(zip(website_names, prediction))
    sorted_websites = sorted(website_weights, key=lambda x: x[1], reverse=True)
    top_3_websites = [website for website, weight in sorted_websites[:3]]
    return top_3_websites

def cnn(features, username):
    loaded_model = load_model('./static/model.keras')
    with open('./static/scaler.pkl', 'rb') as f:
        loaded_scaler = pickle.load(f)
    features_normalized = loaded_scaler.transform([features])
    predicted_preferences = loaded_model.predict(features_normalized)
    top_websites = get_top_websites(predicted_preferences[0], website_names)
    idd = interface_data.objects.get(user=username)
    idd.preference_gfg = predicted_preferences[0][0]
    idd.preference_w3school = predicted_preferences[0][1]
    idd.preference_youtube = predicted_preferences[0][2]
    idd.save()
    return top_websites


if __name__ == '__main__':
    sample_input = np.array([93, 94, 0, 62, 23.22, 50, 36.6, 40, 13, 47, 57, 96, 29])
    predicted_preferences = cnn(sample_input)
    print("Predicted Top Website Preferences for the sample input:", predicted_preferences)
