import streamlit as st
import json
import random
st.set_page_config(layout="wide")

fa_css = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
'''

st.write(fa_css, unsafe_allow_html=True)



file_path = "./data.json"


with open(file_path, 'r') as json_file:
    data = json.load(json_file)

with open('./static/main.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


def renderRejects(rejects):

    s=""
    for i in rejects:
    
        if i=="~" or i==" ":  # - Blank
            s+= f"<div class='letterWordBreak'></div>" # This is the space between words. Do not render anything
        else:
            s+= f"<div class='reject'><del>{i}<del></div>" # This is the rejected letters

    
    return s
       
def renderRejectedList(rejects):
    html=f"""
        <div class="container">
           {renderRejects(rejects)} 
        </div>
    """
    st.markdown(html,unsafe_allow_html=True)

def renderWord(word):
    s=""
    for i in word:
      if i=="~":  # - Blank
        s+= f"<div class='letterWordBreak'></div>" # This is the space between words. Do not render anything
      elif i ==" ":
        s+= f"<div class='letter'>{i}</div>" # This is the empty unfilled letter
      else:
         s+= f"<div class='filledLetter'>{i}</div>" # filled letter
    return s

def renderGame(word):
    html=f"""
        <div class="container">
           {renderWord(word)} 
        </div>
    """
    st.markdown(html,unsafe_allow_html=True)

def initResult(word):
   result=word.copy()
   for index, letter in enumerate(word):
      if letter==' ':
         result[index]='~'  # word breaks
      else:
         result[index]=' ' # Clear out letters 
   return result


         
def generateNewGuessWord():
     random_item = random.choice(data["vulnerabilities"])
     return random_item
     

st.title('Software Security Word Game')



if 'guessWord' not in st.session_state:
 randomItem= generateNewGuessWord()
 st.session_state.status="IN-PROGRESS"
 st.session_state["guessWord"]=list(randomItem["name"]) 
 st.session_state["clue"]= randomItem["clue"]
 st.session_state["url"]= randomItem["link"]
 attempts=0
 gaps=0
 for i, c in enumerate (st.session_state.guessWord):
    if c ==' ':
       gaps+=1
    else:
      attempts+=1
 st.session_state.attempts=attempts
 st.session_state.gaps=gaps
 st.session_state.remainingAttempts=attempts


guessWord =st.session_state.guessWord
attempts=st.session_state.attempts
remainingAttempts=st.session_state.remainingAttempts

if 'result' not in st.session_state:
 st.session_state.result=initResult(guessWord)
 st.session_state.rejectResult=st.session_state.result.copy()

result=st.session_state.result  # Stores accepted letters with `~`(spaces) filled in
rejectResult=st.session_state.rejectResult # Stores rejected letters `~` (spaces) filled in
status=st.session_state.status




def findAndPopulateChar(s, guessStr, result,rejectResult,remainingAttempts):
    for i, c in enumerate(guessStr):
        positions=[pos for pos, char in enumerate(s) if char.lower() == c.lower()] # find positions in which this char exists

        if  len(positions) ==0 and c not in rejectResult : # add the reject leter to a empty spot by scanning left to right (avoid ~). Just so it looks aligned
            st.session_state.remainingAttempts = st.session_state.remainingAttempts-1
            for index, letter in enumerate(rejectResult):
                if letter==' ':
                    rejectResult[index]=c   
                    break
            
        # Populate results in correct spots   
        for i  in positions:
         result[i]= c

def evalGuess():
   findAndPopulateChar(list(guessWord),st.session_state.guess, result,rejectResult, remainingAttempts)
   

def updateStatus(result):
   positions=[pos for pos, char in enumerate(result) if char == ' '] # find unfilled positions 
   if  len(positions) ==0:
      st.session_state.status="SUCCESS"

   


game_col, details_col = st.columns([50,50])

with game_col:
    st.markdown(f"<div class='clue'> <i class='fa-sharp fa-solid fa-lightbulb fa-xl'></i>  {st.session_state.clue}  </div>", unsafe_allow_html=True)
    guess= st.text_input(label="Enter your guess here. One or more letters" , max_chars=remainingAttempts, key="guess" , on_change=evalGuess)
    renderGame(result)
    renderRejectedList(rejectResult)
    updateStatus(result)
   

with details_col:
   if st.session_state.status=="SUCCESS":
    st.markdown(f"<iframe src='{st.session_state.url}' width='100%' height='100vh' > </iframe>", unsafe_allow_html=True)


if st.session_state.status=="SUCCESS":
       st.button("Play Again")
       st.balloons()
else:
    st.metric("Remaining Attempts", remainingAttempts)