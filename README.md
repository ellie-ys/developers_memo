# Developer's Memo

![image](https://user-images.githubusercontent.com/91821953/141883495-19a84390-49bc-4d1d-99e3-ba52d6407f3c.png)

- 개인 미니 사이드 프로젝트입니다.
- 같은 관심사를 가진 guild원이 모여서 회원가입을 하고, 간단한 메모나 고민, 링크 등을 공유하고 수정 삭제 또한 가능한 게시판을 만들어보았습니다. 
- 추후 댓글 기능을 추가할 예정입니다.



## Installing
### 1. 가상환경 설정
기본적인 실행하기 위한 과정은 다음과 같습니다.
```bash
python -m venv venv
source venv/Scripts/activate
```
### 2. 시스템 환경 설정
동작을 위해 cuda 10.0, cudnn 7.6.5, tensorflow(-gpu) 1.15.0 버전은 반드시 맞춰주세요.  
패키지들의 설치를 위해 다음 명령어를 실행해 주세요.
```bash
pip install -r requirements.txt
```
### 3. Api 서버 Flask 동작시키기
```bash
export Flask_App = flask_board
flask run
```
