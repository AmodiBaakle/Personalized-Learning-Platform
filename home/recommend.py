import home.scraping as scraping
import home.cnn_model as cnn_model
import home.clustering_self_attention as clustering_self_attention
import pandas as pd

df = pd.read_csv('./static/updated_content.csv')

def main(pid, username):
    preferences = []
    features = [pid['content_stay_gfg'], pid['content_visit_gfg'], pid['video_play'], pid['video_visit'],
              pid['question_remember'], pid['question_understanding'], pid['question_application'], pid['question_analysis'],
              pid['question_evaluation'], pid['self_assess_stay'], pid['self_assess_visit'], pid['content_stay_w3school'],
              pid['content_visit_w3school']]
    if pid["total_interactions"] == 0:
        pref = {
            'GFG': pid['preference_gfg'], 
            'W3Schools': pid['preference_w3school'], 
            'Youtube': pid['preference_youtube']}
        preferences =  sorted(pref, key=pref.get,reverse=True)
    elif pid['total_interactions'] <=100:
        preferences = clustering_self_attention.main([0] + features, pid['level_of_understanding'], username)
    else:
        preferences = cnn_model.cnn(features, username)
    print(preferences)
    return preferences

def recom(preferences, sub):
    output = dict()
    output['pref1'] = dict()
    output['pref2'] = dict()
    output['pref3'] = dict()
    for i in preferences:
        if i == 'GFG':  
            gfg = scraping.gfg(sub)
            gfg_url = list(gfg.keys())[0]
            gfg_content = list(gfg.values())[0]
        elif i == 'W3Schools':
            w3 = scraping.w3schools(sub)
            w3_url = list(w3.keys())[0]
            w3_content = list(w3.values())[0]
        else:
            yb = scraping.youtube(sub)
            yb_url = list(yb.keys())[0]
            yb_content = list(yb.values())[0]

    output['pref1']['source'] = preferences[0]
    if preferences[0] == 'GFG': output['pref1']['credits'], output['pref1']['content'] = gfg_url, gfg_content
    elif preferences[0] == 'W3Schools': output['pref1']['credits'], output['pref1']['content'] = w3_url, w3_content
    elif preferences[0] == 'Youtube': output['pref1']['credits'], output['pref1']['content'] = yb_url, yb_content

    if preferences[1] == 'GFG': output['pref2']['credits'], output['pref2']['content'] = gfg_url, gfg_content
    elif preferences[1] == 'W3Schools': output['pref2']['credits'], output['pref2']['content'] = w3_url, w3_content
    elif preferences[1] == 'Youtube': output['pref2']['credits'], output['pref2']['content'] = yb_url, yb_content

    if preferences[2] == 'GFG': output['pref3']['credits'], output['pref3']['content'] = gfg_url, gfg_content
    elif preferences[2] == 'W3Schools': output['pref3']['credits'], output['pref3']['content'] = w3_url, w3_content
    elif preferences[2] == 'Youtube': output['pref3']['credits'], output['pref3']['content'] = yb_url, yb_content

    return output 

    '''return {
      'topic':'Learn the Basics',
      'subtopic': 'Variables',
      'pref1':{
                  'source': 'GFG',
                  'credits': 'gfg.com', 
                  'content': 'You are studying Variables!!!'
                 },
      'pref2':{
                  'source': 'W3Schools',
                  'credits': 'w3.com', 
                  'content': 'You are studying Variables!!!'
       },
      'pref3':{
                  'source': 'Youtube',
                  'credits': 'youtube.com', 
                  'content': 'youtube video link'},
      'question': {
             'type' : 'remember',
             'ques': 'What is your name?',
             'opt1' : 'val1',
             'opt2' : 'val2',
             'opt3' : 'val3',
             'opt4' : 'val4',
             'ans' : 'val2'
       }
    }'''


if __name__ == '__main__':
    pid = {
        'total_interactions': 80,
        'level_of_understanding': 'Type Casting',
    }
    pid['content_stay_gfg'], pid['content_visit_gfg'], pid['video_play_youtube'], pid['video_visit_youtube'], pid['question_remember'], pid['question_understanding'], pid['question_application'], pid['question_analysis'], pid['question_evaluation'], pid['self_assess_stay'], pid['self_assess_visit'], pid['content_stay_w3school'], pid['content_visit_w3school'] = 93, 94, 0, 62, 23.22, 50, 36.6, 40, 13, 47, 57, 96, 29
    print(pid)
    output = main(pid)
    # print(output)