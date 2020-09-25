# CI and CD ด้วย Docker, Image Registry และ Kubernetes บน Localhost(Window 10)
เพื่อให้เข้าใจการทำงานของ CI และ CD ก่อนที่จะทำการส่ง Code ของเราขึ้น Cloud โดยผูกขั้นตอนต่างๆ เข้ากับ Tool อย่างพวก Jenkins จึงชวนทุกคนมา เล่น Docker, Image Registry และ Kubernetes บนเครื่อง Local ที่ไม่ว่าจะเล่นอย่างไรก็ยังไม่ต้องเสียค่าใช้จ่ายให้ Cloud Provider 

![BigPicture](resource/Bigpicture.png?raw=true "BigPicture")


## 0. Python web app
เครียมแอพของเราที่จะ deploy ขึ้น server ซึ่งในทีนี้เราจะใช้ภาษา python ดังนั้นเราต้องเตรียม environment โดยเริ่มจากโหลด [python](https://www.python.org/downloads/) จากนั้นจึงเตรียม library สำหรับแอพของเราด้วยการรันคำสั่ง

    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org flask

เราเตรียม Code ที่เป็น python webapp ง่ายๆที่ใช้บริการ Framework ที่ชื่อว่า Flask 

    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def homepage():
        return "Welcome to my webpage"
    
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port='5000')

โดยเราสามารถรัน application ของเราด้วย command ด้านล่างนี้ซึ่งถ้าไม่มีปัญหาอะไร เราจะสามารถเรียก application ของเราผ่าน browser ด้วย URL: [http://127.0.0.1:5000/](http://127.0.0.1:5000/) ซึ่งแสดงคำว่า "Welcome to my webpage" ออกมา
    
    python app.py


## 1. Docker
ทีนี้เราพร้อมที่จะเอา application ของเราส่งขึ้น Docker ที่อยู่บนเครื่องของเราเอง พระเอกของงานนี้คือ Docker Desktop บน window 10 โดยสามารถ Download ได้จาก [docker-ce-desktop-windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows/) เมื่อโหลดเสร็จแล้ว รบกวนกดที่ Switch to Linux containers เพราะจากที่ลองใช้ Window container แล้วมัน crash ตัวมันเองบ่อยๆ

พอโหลดแล้วสิ่งที่เราต้องเตรียมต่อไปก็คือ [Dockerfile](/Dockerfile) ซึ่งเป็นโครงสร้างเพื่อสร้าง image ขึ้นมา 

### 1.1 Image 
เราสามารถทดสอบว่า Dockerfile ที่เราเขียนขึ้นมานั้นทำงานได้ถูกต้องด้วยการสั่ง Command ด้านล่าง

    docker image build -t oujai/myweb .

### 1.2 Container
และสามารถ Run application ให้สามารถใช้งานได้ด้วยการ

    docker container run oujai/myweb

### 1.3 Command เพิ่มเติม

    docker container ls
    docker logs [CONTAINER ID]
    docker exec -it [CONTAINER ID] /bin/sh
    docker exec -it [CONTAINER ID] /bin/bash
    
    $docker ps -q | xargs docker stats

    __Standard command__
    $ docker image ls
    $ docker container ls
    $ docker container run oujai/myweb:1.0.0
    __Run in background service__
    $ docker container run -d oujai/myweb:1.0.0
    $ curl localhost:5000
    $ docker container stop 1052821d0562
    __Connect port__
    $ docker container run -d -p 8080:5000 oujai/myweb:1.0.0
    $ curl -s localhost:8080
    __Start shell__
    $ docker container ls
    $ docker container exec -it e53fed3d19fa /bin/sh
    # curl localhost:5000
    $ docker container stop e53fed3d19fa
    __Map local directory__
    $ docker container run -d -p 8080:5000 -v $(pwd):/app oujai/myweb:1.0.0
    $ echo "hi" > a.log
    $ docker container exec -it b0c5377138ec /bin/sh
    $ echo "hello" > b.log

## 2. Image Registry
ความสำคัญของ Image Registry คือ เป็นสถานที่เก็บ Image ที่เราสร้างขึ้น และปล่อยให้ผู้ใช้คนอื่นๆสามารถดึง Image ของเราไปใช้งานได้ผ่าน Docker หรือผ่าน Kubernetes ก็ได้ โดยทั่วไปเราสามารถส่ง Image เราขึ้นไปด้วย Command *docker image push [imagename]* ซึ่งจะส่ง Image ของเราไปที่ [https://hub.docker.com/](https://hub.docker.com/) แต่กรณีที่เราไม่สามารถเอา image ไปวางที่นี่ได้ ไม่ว่าจะเพราะ Code ของบริษัทหรืออะไรก็ตามแต่ เราก็สามารถเอา Image ไปวางไว้ที่ Local Image Registry ได้

เนื่องจากเรามี Docker บนเครื่องแล้ว เราจึงสามารถเสก Application อะไรก็ได้บนเครื่องเรา ซึ่งเราก็จะเสก Image Registry version 2 ขึ้นมาใช้งานบนเครื่องเราเอง ขั้นตอนง่ายๆ ก็คือการ Run command ด้านล่าน โดยลองสังเกตุดูดีๆ จะเห็นว่าเราเปิด port 8080 ใช้งาน

    docker run -d -p 8080:5000 --name registry --restart=always registry:2 

เมื่อเราได้ Image Registry ขึ้นมาแล้วเราก็สามารถ ส่ง Image ของเราขึ้นไปได้เลยโดย Commanhd ด้านล่างซึ่งจะเห็นว่า เรามีการเพิ่ม [localhost:8080/] ซึ่งเป็น path ของ Local Image Registry ที่เราพึ่งสร้างขึ้นมาเมื่อตั่งกี้นี่เอง

    docker image build -t localhost:8080/asnpahp/myweb . 
    docker image tag myweb localhost:8080/asnpahp/myweb
    docker image push localhost:8080/asnpahp/myweb

    docker container run localhost:8080/asnpahp/myweb

เราสามารถเช็คว่าเราได้ทำการ push Image เข้า Registry เรียบร้อยแล้วโดยการเช็คที่ URL [http://localhost:8080/v2/_catalog](http://localhost:8080/v2/_catalog) เราก็จะเห็น Image ที่ชื่อ asnpahp/myweb โพล่ขึ้นมา!!!


## 3. Kubernetes
เมื่อเราต้องการใช้งาน Kubernetes เราสามารถ Enable Kubernetes มาใช้งานได้โดยเข้าไปตั้งค่าใน Docker Desktop โดยกดที่ Settings > Kubernetes > Enable Kubernetes > Apply & Restart ซึ่งถ้าหากเรา Run command ด้านล่าง ก็จะเห็นว่า Docker ทำการโหลด Image พวก K8S มารันภายในเครื่องเรา

    docker image ls

สุดท้ายแล้ว เราก็พร้อมที่จะเอา application myweb ขึ้น Kubernetes โดยใช้ไฟล์ [deployment.yaml](/kube-myweb/deployment.yaml) และ สร้างทางเข้า application ผ่านไฟล์ [service.yaml](/kube-myweb/service-nodeport.yaml) 

    kubectl apply -f deployment.yaml
    kubectl get deployment

    kubectl apply -f service.yaml
    kubectl get service

แถม Command ที่ใช้บ่อยๆของ Kubernetes

    __แสดง pods__
    kubectl get pods
    kubectl get pods | findstr myweb
    __ดูรายละเอียด pods__
    kubectl describe pods
    kubectl describe pods [pod id] // แสดงเฉพาะ demo-nginx
    __ลบ pods__
    kubectl delete pods [pod id]
    __แสดง services__
    kubectl get services
    kubectl get services demo-nginx // แสดงเฉพาะ demo-nginx
    __เข้าถึง containers ผ่าน shell__
    kubectl exec -it demo-nginx-548685f5cc-v7rmc sh
    __แสดง logs__
    kubectl logs -f demo-nginx-548685f5cc-v7rmc
    kubectl logs --max-log-requests=8 -f -l app=myweb > mylog.log

การ Install ทั้ง Docker และ Kubernetes จะแอบแก้ไขไฟล์ C:\Windows\System32\drivers\etc\hosts ให้เราอัติโนมัติ
    __# Added by Docker Desktop__
    192.168.48.118 host.docker.internal
    192.168.48.118 gateway.docker.internal
    __# To allow the same kube context to work on the host and the container:__
    127.0.0.1 kubernetes.docker.internal


## 4. Additional
เมื่อเรามี Kubernetes เราสามารถเสก Kubernetes Dashboard ขึ้นมาใช้งานได้ด้วยคำสั่งด้านล่าง

    kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml
    kubectl proxy

สามารถเข้าใช้งาน Dashboard ด้วย URL http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/. ซึ่งก่อนที่จะเข้าไปดูข้อมูลได้นั้นเราต้องไปเอา token จาก command ด้านล่างมาใส่ในหน้า login

    kubectl -n kube-system describe secret default

หรือถ้าใช้ Visural Studio Code แล้วหละก็แนะนำ Extension สองตัวนี้โลดดดดด [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) กับ [Kubernetes](https://marketplace.visualstudio.com/items?itemName=ms-kubernetes-tools.vscode-kubernetes-tools)
