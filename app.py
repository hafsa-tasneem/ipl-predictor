import streamlit as st
import pickle
import os
import pandas as pd
#import joblib

#print(os.listdir())

#teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders',
  #       'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Capitals']

#cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
 #         'Chandigarh', 'Jaipur']

#pipe = pickle.load(open('model.pkl', 'rb'))
#pipe_dict = joblib.load("model.pkl")
#pipe = pipe_dict['model']  # make sure the key is correct\
#pipe_dict = joblib.load(r"C:\Users\moham\PycharmProjects\PythonProject\PythonProject1\model.pkl")
#pipe = pipe_dict['model']  # Adjust key if needed

#st.title('IPL Win Predictor')

#col1, col2= st.columns(2)

#with col1:
 #   batting_team = st.selectbox('select the batting team',teams)
#with col2:
 #   bowling_team = st.selectbox('Select the bolinng team',teams)

#selected_city = st.selectbox('Select host city', sorted(cities))

#target = st.number_input('Target')

#col3,col4,col5 = st.columns(3)

#with col3:
 #   score = st.number_input('Score')
#with col4:
 #   overs = st.number_input('Overs completed')
#with col5:
 #   wickets = st.number_input('Wickets out')

#if st.button('Predict Probability'):
   # runs_left = target - score
   # balls_left = 120 - (overs*6)
    #wickets = 10 - wickets
    #crr = score/overs
    #rrr = (runs_left*6)/balls_left

    #input_df = pd.DataFrame({'batting_team':[batting_team], 'bowling_team':[bowling_team],
     #                        'city':[selected_city], 'runs_left':[runs_left], 'balls_left':[balls_left], 'wickets':[wickets],
      #                       'total_runs_x':[target], 'crr':[crr], 'rrr':[rrr]})


   # pipe_dict = joblib.load("model.pkl")
  #  pipe = pipe_dict['model']  # adjust key if different
 #   result = pipe.predict_proba(input_df)


#    st.text(result)


import streamlit as st
import pickle
import os
import pandas as pd
import pandas as pd

df = pd.read_csv('matches.csv')
print(df.head())

print(os.listdir())
model_path = 'pipe.pkl'
if os.path.exists(model_path):
    pipe = pickle.load(open(model_path, 'rb'))
else:
    st.error(f"Model file '{model_path}' not found! Please put it in the project folder.")

teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 'Kolkata Knight Riders',
         'Kings XI Punjab', 'Chennai Super Kings', 'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur']

# Load model using pickle (make sure pipe.pkl exists in same folder)
pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', teams)
with col2:
    bowling_team = st.selectbox('Select the bowling team', teams)

selected_city = st.selectbox('Select host city', sorted(cities))

target = st.number_input('Target')

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Score')
with col4:
    overs = st.number_input('Overs completed')
with col5:
    wickets = st.number_input('Wickets out')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = score / overs
    rrr = (runs_left * 6) / balls_left

    input_df = pd.DataFrame({
        'team1': [batting_team],  # ✅ change here
        'team2': [bowling_team],  # ✅ change here
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets_left],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })
    # prediction
    result = pipe.predict_proba(input_df)

    # ✅ FIRST define variables
    loss_prob = result[0][0]
    win_prob = result[0][1]

    # ✅ THEN use them
    st.header(batting_team + " Win Probability: " + str(round(win_prob * 100)) + "%")
    st.header(bowling_team + " Win Probability: " + str(round(loss_prob * 100)) + "%")

    # progress bars
    st.subheader("Match Prediction")

    st.progress(int(win_prob * 100))
    st.success(batting_team + " → " + str(round(win_prob * 100)) + "%")

    st.progress(int(loss_prob * 100))
    st.warning(bowling_team + " → " + str(round(loss_prob * 100)) + "%")