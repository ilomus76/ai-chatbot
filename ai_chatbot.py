
#0 . 모듈 설치 
# pip install streamlit
# pip install openai
# pip install dotenv  # open ai 는 키를 한번밖에 보지 못하기 때문에 환경변수에 써놓고 읽어와야 함. 

# #1. 환경변수 .env 파일의 openap api key 값을 읽어오는 모듈 사용
# from dotenv import load_dotenv  # 색깔이 보라색이라 함수임을 알수 있다
# load_dotenv()
# # 함수만 호출하면 끝

# 1. api key 읽어오기 -streamlit cloud 의 secret에 저장한 변수
import streamlit as st
if "OPENAI_API_KEY" in st.secrets:
    api_key=st.secrets['OPENAI_API_KEY']




#2. OpenAI 생성형 api를 요청하는 객체생성
from openai import OpenAI
# client=OpenAI()
client=OpenAI(api_key=api_key)


#사용자 '질문'dmf 파라미터로 받아 OPEN API로 응답한 글씨를 리턴해주는 기능함수 만들기
def get_ai_response(question): # 사용자 채팅 을 받아 응답을 주자
    # 이것은 아주 최근것이고 이것부터해서 책의 처음으로 가서 할 예정이다. 이것만으로는 보기 힘들다. #너무 고수준이지만 워크플로우를 느끼기 위해서.. 책에는 나오지 않음

    response = client.responses.create(
        model='gpt-4o-mini', #o : 옴니 , gpt 5까지 써도 될듯.
        max_output_tokens=10000, # 미세조정 fine tuning이라고 함 
        temperature=1.5, #창의적인 답변 , 같은 답을 하지 않음.
        instructions='너는 고양이야. 이름은 네코냥이야. 고양이처럼 답변해.',  # 지침 ( 바로 여기에 프롬프트엔지니어링 prompting enginnering 기법 적용될수 있음)
        input=question , #사용자의 질문
    ) 

    #응답결과중 메타데이타를 제외한 응답글씨를 전달
    return response.output_text
    # return response  # 메타데이타까지 전부 출력 낭비 
#--------------------------------------------------------------


#3. 채팅 UI 만들기
import streamlit as st

#페이지만 만들어 내자
#1] 페이지 기본 설정 - 브라우저의 탭 영역에 표시되는 내용
st.set_page_config(
    page_title='AI 네코냥봇',
    page_icon='./logo/logo_nekonyang.png'

)

#2] 화면을 2개의 영역으로 분리
col1,col2 = st.columns([1.2,4.8]) # 화면을 1.2대 4.8로 나눔
with col1:
    st.image('./logo/logo_nekonyang.png',width=200)
with col2:
    #화면을 HTML로 만들어 보기 : 어차피 HTML이니가 
    st.markdown(
        '''
        <h1 style='margin-bottome:0;'>AI 네코냥봇 </h1>
        <p style='color:gray; margin-top:0;'> 이 챗본은 모든 답변을 고챵이처럼 합니다. </p>


        '''  ,     
        unsafe_allow_html=True
		) # 이 설정이 있어야 HTML을 그대로 출력해냄.
    
    #구분선 
    st.markdown('---')

    #a. messages 라는 이름의 변수가 st.session_state에 있는지 확인 후 첫 메세지 저장
    if "messages" not in st.session_state:
        st.session_state.messages = [{'role':'assistant','content':'무엇이든 물어보세요.'}]
    #b 저장된 메세지들을 화면에 표시(이전 메세지들이 표시되는 역할)
    for msg in st.session_state.messages:
        st.chat_message(msg['role']).markdown(msg['content'])


    #c. 사용자 채팅메세지를 입력받아 session_state에 저장하고 화면에 표시
    question = st.chat_input('질문을 입력하세요.')

    if question:
        question = question.replace('\n','  \n') # 마크다운 경우 띄어쓰기 리턴 표현
        st.session_state.messages.append({'role':'user','content':question})
        st.chat_message('user').markdown(question)  # 화면에 사용자 입력을 찍는 것

        #응답 - AI에게 응답요구 기능 함수 호출.... [ 응답할때까지 시간이 걸리기에... spinner]
        with st.spinner('AI 네코냥봇이 응답중입니다....잠시만 기다려 주세요'):
            response = get_ai_response(question=question)
            st.session_state.messages.append({'role':'assistant','content':response})
            st.chat_message('assistant').markdown(response)
    #--------------------------------------------------
    #[실행] 터미널에서 streamlit run 파일명.py


    #-----------------------------------------------------
    #[배포]스트림릿으로 만든 웹앨을 배포[streamlit은 기본적으로 html/css/js로 변환해주는 기능]

    #Streamlit Community Clouse 배포 
    #1) 프로젝트를 GitHub에 업로드 
    #2)그 다음에 Streamlit Cloud 접속 및 (GitHub계정)로그인 [ 회원가입했다는 전제]
    #3) [New app]버튼을 클릭 후 GitHub저장소를 선택 
    #4) 그러면 자동으로 배포됨 (도메인 일부 수정 가능)

    #외부 모듈을 사용했다면 에러발생 .. streamlit cloud에는 module이 설치되어 있지 않기에...
    #직접 설치는 안되고.. 특정 이름의 문서를 주면 이를 기반으로 자동 설치됨...
    #파이썬의 모듈 목록을 저장해 놓은 문서 requirements.txt를 만들고 안에 설치할 모듈 목록 등록
    #github에 push

    #외부 api key를 사용한다면 역시 에러가 또 발생..
    #.env 파일은 업로드 하면 완되는 비밀파일이기에..

    #streamlit cloud에서 배포된 프로젝트마다 사용한 인증키나 비밀번호 같은 정보들을 
    #설정해 놓을 수 있는 기능이 제공됨. 


# git init
# git add --all or git add . # 이폴더안에 있는 것을 깃으로 관리하겠다
# git commit -m init
# github에서 폴더 만들기 
# git remote add origin   [ git remote add origin https://github.com/ilomus76/ai-chatbot.git]
# git push -u origin main 

#streamlit community cloud -> free -> github 


