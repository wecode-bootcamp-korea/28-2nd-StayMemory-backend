# 28-2nd-StayMemory-backend

> 본 repository는 웹개발 학습을 위하여 스테이폴리오(https://www.stayfolio.com/) 사이트를 클론코딩하였습니다.

</br>

## 개발 인원 및 기간
- 개발기간: 2022.01.10. ~ 2022.01.21.
- Frontend: 이가윤, 옥채현, 이석호 (repository: https://github.com/wecode-bootcamp-korea/28-2nd-StayMemory-frontend)
- Backend: 김재엽, 이찬영

## 협업 도구
- slack
- Github
- Trello

## 사용기술
- Django Framework를 사용하여 웹서버 구축 및 API 개발
- MySQL을 사용하여 데이터베이스 구축
- 카카오 로그인 API를 사용하여 소셜로그인
- AWS(EC2, RDS, S3)를 사용하여 배포

## 구현 기능
### user
- 로그인, 회원가입: 카카오 로그인 API를 활용하여 로그인 기능 구현, 회원 정보가 없을 시 회원가입 진행
- 회원 정보를 조회하는 기능
### stays
- 주어진 조건에 맞는 스테이 목록을 조회하는 기능
- 상세페이지에 필요한 정보를 조회하는 기능
- 숙박 예약 정보를 확인하고 가능 날짜를 조회하는 기능
- 주어진 날짜에 맞는 숙박료를 계산하는 기능

### reservations
- 예약 정보를 조회하는 기능
- 예약 요청 시 정보를 DB에 기입하는 기능

### admins
- 어드민이 소유한 숙박 정보를 조회하는 기능
- 어드민이 소유한 숙박 정보를 수정하는 기능(이미지의 경우에는 S3에 업로드)
- 어드민이 소유한 숙박 정보를 삭제하는 기능
