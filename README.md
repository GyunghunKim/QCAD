# QCAD

Quantum Circuit Simulating Tools

# 설치 방법

1. 리눅스 기반의 운영체제에서 동작합니다.
2. 원하는 경로로 이동한 후 다음 명령어로 설치합니다.
~~~
	git clone https://github.com/GyunghunKim/QCAD.git
~~~
3. QCAD/Backend/build.sh 스크립트를 실행해 csim.so 파일을 빌드합니다.
4. QCAD 폴더 내부에 있는 Test.ipynb 파일과 Tutorial.ipynb 파일을 jupyter notebook을 통해 확인합니다.

## 사전에 설치되어야 하는 패키지들

1. python2

우선 terminal에서 어떤 명령어로 python2가 실행되는지 확인합니다.
이후 QCAD/CircuitDrawer/qasm2png 에서 python2 부분을 해당 명령어로 바꿔줍니다.
기본은 python2로 세팅되어 있습니다.

2. python3

핵심 코드들은 모두 python3 기반으로 동작합니다.

3. numpy
4. latex with xypic
5. netpbm

# 기타

- 그림은 모두 QCAD/CircuitDrawer/에 저장됩니다.

- 회로를 그리기 위해 I. Chuang의 qasm2circ 패키지가 활용되었음을 밝힙니다.&nbsp;링크: https://www.media.mit.edu/quanta/qasm2circ/
