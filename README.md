# intellij
intellij test


====> 기본환경에서 prompt 실행
vscode, python311 설치 (앱 실행 별칭 관리: 선택제거, 환경변수 path )
extension : pip manager
pip manager : openai 검색 설치. 

===> 가상환경에서 prompt 실행 
pip 설치 
C:\Users\08215>python --version
Python 3.11.4

C:\Users\08215>curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 2518k  100 2518k    0     0  11.5M      0 --:--:-- --:--:-- --:--:-- 11.7M

C:\Users\08215>python get-pip.py
Collecting pip
  Downloading pip-23.1.2-py3-none-any.whl (2.1 MB)
     ---------------------------------------- 2.1/2.1 MB 33.1 MB/s eta 0:00:00
Collecting wheel
  Downloading wheel-0.40.0-py3-none-any.whl (64 kB)
     ---------------------------------------- 64.5/64.5 kB 3.6 MB/s eta 0:00:00
Installing collected packages: wheel, pip
  WARNING: The script wheel.exe is installed in 'D:\dev\Python\Python311\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  Attempting uninstall: pip
    Found existing installation: pip 23.1.2
    Uninstalling pip-23.1.2:
      Successfully uninstalled pip-23.1.2
  WARNING: The scripts pip.exe, pip3.11.exe and pip3.exe are installed in 'D:\dev\Python\Python311\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed pip-23.1.2 wheel-0.40.0

C:\Users\08215>pip --version
'pip'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는
배치 파일이 아닙니다.

===> path 추가 : D:\dev\Python\Python311\Scripts
cmd 재시작 

C:\Users\08215>pip --version
pip 23.1.2 from D:\dev\Python\Python311\Lib\site-packages\pip (python 3.11)

pip can be upgraded using the following command.
python -m pip install -U pip

[python] 윈도우(window)에 pipenv 설치하고 실행해보기
https://fenderist.tistory.com/361
1. 설치
 -  pip install pipenv

2. 설치 확인
 - pipenv

cd D:\dev\workspace_vscode\flask01
3. 가상환경 만들기
D:\dev\workspace_vscode\flask01>pipenv --python 3.11
Creating a virtualenv for this project...
Pipfile: D:\dev\workspace_vscode\flask01\Pipfile
Using D:/dev/Python/Python311/python.exe (3.11.4) to create virtualenv...
[=   ] Creating virtual environment...created virtual environment CPython3.11.4.final.0-64 in 3521ms
  creator CPython3Windows(dest=C:\Users\08215\.virtualenvs\flask01-lhp7V4TH, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=C:\Users\08215\AppData\Local\pypa\virtualenv)
    added seed packages: pip==23.1.2, setuptools==67.8.0, wheel==0.40.0
  activators BashActivator,BatchActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator

Successfully created virtual environment!
Virtualenv location: C:\Users\08215\.virtualenvs\flask01-lhp7V4TH
Creating a Pipfile for this project...

shell에서 가상환경 사용할때 
D:\dev\workspace_vscode\flask01>pipenv shell
Launching subshell in virtual environment...
Microsoft Windows [Version 10.0.19042.2965]
(c) Microsoft Corporation. All rights reserved.

4. VSCode에서 해당 폴더 열기
5. F1 --> select interpreter --> 가상환경 실행
ipynb 파일열고 오른쪽위 select kernel에서 위의 가상환경 선택제거
terminal( cmd ) 실행하면 가상환경 실행됨 (D:\dev\workspace_vscode\flask01>C:/Users/08215/.virtualenvs/flask01-lhp7V4TH/Scripts/activate.bat )

6. 패키지 설치

(flask01) D:\dev\workspace_vscode\flask01>pip install openai
 pip install ipykernel
pip install openai  => 가상환경 마다 따로 설치해줘야 한다. 
실행파일 마다 가상환경 선택해야 한다. 

* 기본 터미널 변경 : F1 > Terminal: Select Default Profile
flask 설치
pip install flask
실행 
(flask01) D:\dev\workspace_vscode\flask01>flask --app start run
~~~
 * Running on http://127.0.0.1:5000
