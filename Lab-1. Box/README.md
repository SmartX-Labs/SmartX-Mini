#Box Lab
![](https://raw.githubusercontent.com/SmartX-Labs/Mini/master/images/Lab1.Box.JPG)
* Box Lab은 이후 진행할 SmartX Labs을 위한 Lab으로써, Box 내부에 가상 스위치 OpenvSwitch, 하이퍼바이저 KVM, 그리고 Docker Container 환경을 구축합니다. 또한 Box Lab은 구축한 환경에서 OpenvSwitch를 활용하여 KVM으로 생성한 VM과 Docker로 생성한 Container의 연결을 목표합니다.

* 내용은 아래의 네 섹션으로 구성되어 있습니다.
 * 가상스위치 OpenvSwitch를 활용한 Bridge 생성 및 연결
 * 하이퍼바이저 KVM을 활용한 Virtual Machine 환경 구축
 * Docker를 활용한 Container 환경 구축
 * OpenvSwitch를 활용한 Virtual Machine, Container의 연결 및 연결 확인

##Slides Release History

###1.2 (April 2017, written by 남택호)
* Slide Download: [Box_Lab_v1.2.pdf](https://github.com/SmartX-Labs/SmartX-mini/raw/master/Lab-1.%20Box/Box_Lab_v1.2.pdf)
* Release Note
 * KVM VM 생성 부팅 문제 해결, 슬라이드 검수 및 테스트 검증

###1.1 (April 2017, written by 남택호)
* Slide Download: [Box_Lab_v1.1.pdf](https://github.com/SmartX-Labs/SmartX-mini/raw/master/Lab-1.%20Box/Box_Lab_v1.1.pdf)
* Release Note
 * OS version update: 14.04 -> 16.04
 * OS update 이후 발생한 miner한 network setting issue 정리

###1.0 (Jan 2017, written by 남택호)
* Slide Download: [Box_Lab_v1.0.pdf](https://github.com/SmartX-Labs/Mini/raw/master/Lab-1.%20Box/Box_Lab_v1.0.pdf)
* Release Note
 * KVM을 활용한 박스 내부 구성시 사용되는 이미지 파일 링크 변경
 
###0.9 (June 2016, written by 남택호)
* Slide Download: [Box_Lab_v0.9.pdf](https://github.com/SmartX-Labs/Mini/raw/master/Lab-1.%20Box/Box_Lab_v0.9.pdf)
* PowerPoint File Download: [Box_Lab_v0.9.pptx](https://github.com/SmartX-Labs/Mini/raw/master/Lab-1.%20Box/Box_Lab_v0.9.pptx)
* Demostration Movie: [Box_Lab Demo_v0.9.mp4](https://www.dropbox.com/s/blmvfnvcu51ruyg/%5BDemo%5DBoxLab_v09.mp4?dl=0)
* Release Note
 * Box Lab 내용 개선 및 추가: 불필요한 Prerequisite 제거(미러사이트 변경), NUC 디바이스 세팅에 대한 Appendix 추가

###0.8 (April 2016, written by 남택호)
* Slide Download: [Box_Lab_v0.8.pdf](https://github.com/SmartX-Labs/Mini/raw/master/Lab-1.%20Box/Box_Lab_v0.8.pdf)
* Release Note
 * Box Lab 최종본 작성: 실습 진행 중 발생한 이슈에 대한 개선사항 추가, Docker Container Command 관련 이슈 해결

###0.7 (April 2016, written by 남택호)
* Slide Download: [Box_Lab_v0.7.pdf](https://github.com/SmartX-Labs/Mini/blob/master/Lab-1.%20Box/Box_Lab_v0.7.pdf)
* Release Note
 * Box Lab 검수 및 수정: Outline 추가, 검수자 피드백 반영 및 자료 개선, 오탈자 수정

###0.6 (April 2016, written by 남택호)
* Slide Download: [Box_Lab_v0.6.pdf](https://github.com/SmartX-Labs/Mini/blob/master/Lab-1.%20Box/Box_Lab_v0.6.pdf)
* Release Note
 * Box Lab 개선 및 편집: 추가 설명자료 편집 및 단어 교정, History 작성

###0.5 (March 2016, written by 남택호)
* Slide Download: [Box_Lab_v0.5.pdf](https://github.com/SmartX-Labs/Mini/blob/master/Lab-1.%20Box/Box_Lab_v0.5.pdf)
* Release Note
 * Box Lab 초안 작성: Functions Lab(구 Box Lab) 자료 이전 및 세부자료 수정

###0.4 (October 2015, written by 윤희범)
* Release Note
 * Functions Lab(구 Box Lab) 최종본 작성: Ver 0.3 자료 개선 및 실제 실습에 사용할 최종자료 편집

###0.3 (October 2015, written by 배정주)
* Release Note
 * Functions Lab(구 Box Lab) 초안 작성: Ver 0.2 자료 개선 및 전반적인 편집

###0.2 (September 2015, written by 윤희범)
* Release Note
 * Functions Lab(구 Box Lab) 작성: KVM 관련 자료 초안 작성

###0.1 (September 2015, written by 배정주)
* Release Note
 * Functions Lab(구 Box Lab) 작성: OpenVswitch, Docker 관련 자료 초안 작성
