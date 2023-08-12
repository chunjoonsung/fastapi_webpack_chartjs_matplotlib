# fastapi_webpack_chartjs_matplotlib


## fastapi 인스톨
$ pip install fastapi
$ pip install jinja2
$ pip install matplotlib
$ pip install uvicorn

## 웹서버 구동
$ uvicorn server:app --port 3080 --reload

## 디렉토리 구조
- src 밑에 있는 javascript 파일을 합쳐서 public 밑에 있는 bundle.js 파일로 번들링한다.
- express 로 server.js 를 구동하여 public/index.html 를 서비스 한다.
```
├─ static
│  ├─ bundle.js
│  ├─ js
│  │  ├─ chart.js
│  │  ├─ jquery.js       
│  │  └─ bootstrap.js       
│  └─ css
│     └─ bootstrap.css
│─ templates
│  └─ index.html
│─ src
│  ├─ index.js
│  └─ mychart.js
│─ routes
│  ├─ data.py
│  └─ unage.py
├─ package.json
├─ webpack.config.js
├─ webpack.prod.config.js
└─ server.py
```

## 패키지 인스톨
```bash
npm install jquery
npm install chart.js
npm install webpack webpack-cli --save-dev
```

## package.json
- `npm run dev` 명령어를 이용하여 development 모드로 번들링한다.
- `npm run build` 명령어를 이용하여 production 모드로 번들링한다.
```json
{
  "name": "webpack_simple",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "dev": "webpack --mode development",
    "build": "webpack --mode production"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "webpack": "^5.88.2",
    "webpack-cli": "^5.1.4"
  },
  "dependencies": {
    "bootstrap": "^5.3.1",
    "chart.js": "^4.3.3",
    "jquery": "^3.7.0"
  }
}
```

##webpack.config.js
-  src / index.js 파일에서 시작하여 의존성 있는 파일들을 모두 포함하여 public / bundle.js 파일로 번들링한다. 
```js
const { resolve } = require('path')

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: resolve(__dirname, 'public')
  }
}
```

## server.py
- public 폴더를 기본 디렉토리로 해서 서비스를 시작한다.
- /data/chart 요청하면 json 데이터를 전송한다.

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes import data

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(data.router)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})
```

## routes / data.py

```python
from fastapi import APIRouter
import json

router = APIRouter(
    prefix="/data",
)

graph_data = {
	'labels': ["HTML", "CSS", "JAVASCRIPT", "CHART.JS", "JQUERY", "BOOTSTRP"],
	'datasets': [{
	   'label': "color",
	   'data': [20, 40, 30, 35, 30, 20],
	   'backgroundColor': ['yellow', 'aqua', 'pink', 'lightgreen', 'lightblue', 'gold'],
	   'borderColor': ['black'],
	   'borderWidth': 2,
	   'pointRadius': 5,
	},{
	   'label': "grey",
	   'data': [10, 50, 20, 25, 40, 30],
	   'borderColor': ['red'],
	   'borderWidth': 2,
	   'pointRadius': 5,
	}],
}
   
   
@router.get("/chart")
def data():
	return graph_data

routes / image.py
from fastapi import APIRouter
from fastapi.responses import Response
import io
import matplotlib.pyplot as plt

def getLineChart():
    with io.BytesIO() as buffer:
        plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
        plt.axis([0.5, 4.5, 0, 20])
        plt.savefig(buffer, format='png') #plt.show()
        buffer.seek(0)
        image = buffer.getvalue()
    return image

router = APIRouter(
    prefix="/image",
)

@router.get("/chart", 
    responses = { 200: { "content": {"image/png": {}}}},
    response_class=Response)
def image():
    image_bytes = getLineChart()
    return Response(content=image_bytes, media_type="image/png")
```

## src / index.js
- 문서가 로딩되면 그래프를 그린다.
- mychart.js 플 포함하여 번들링 되도록 한다.
```js
const MyChart = require('./mychart.js')

$(document).ready( () => {
     fetch(window.location.origin + "/data/chart", {
        method: "get", 
     })
     .then((response) => response.json())
     .then((data) => {
        console.log(data)
		MyChart.drawChart('chartId1','line',data)
		MyChart.drawChart('chartId','bar',data)
     }) 
})
```

## src / mychart.js
- drawChart 함수를 export 하여 다른 곳에서 사용할 수 있도록 한다.
```js
export const drawChart = function(id,type,data) {
    const chrt = document.getElementById(id).getContext("2d");
    return new Chart(chrt, {
        type: type,
        data: data,
        options: {
            responsive: false,
        },
    });
}
```

## templates/ index.html
- bundle.js 를 포함하여 관련된 자바스크립트를 모두 포함시킨다.
```html
<html>
<head>
   <meta charset- "UTF-8" />
   <title>chart.js</title>
   <link rel="stylesheet" type="text/css" href="static/css/bootstrap.css">
   <script src="static/js/bootstrap.js"></script>
   <script src="static/js/jquery.js"></script>
   <script src="static/js/chart.js"></script>
   <script src="static/bundle.js"></script>
</head>
<body>
  <div class="d-flex m-1">
    <div class="card text-center p-0 m-1" style="overflow: hidden">
      <div class="card-header">
        Featured
      </div>
      <div class="card-body">
        <canvas id="chartId1" style="min-height: 200px"></canvas>
      </div>
      <div class="card-footer">
        <a href="#" class="btn btn-primary">Go somewhere</a>
      </div>
    </div>
    <div class="card text-center p-0 m-1" style="overflow: hidden">
      <div class="card-header">
        Featured
      </div>
      <div class="card-body">
         <canvas id="chartId" style="min-height: 200px"></canvas>
      </div>
      <div class="card-footer d-flex justify-content-end"">
        <a href="#" class="btn btn-primary">Go somewhere</a>
      </div>
    </div>
  </div>
  <div class="d-flex m-1">
    <div class="card text-center p-0 m-1" style="overflow: hidden">
      <div class="card-header">
        Featured
      </div>
      <div class="card-body">
        <img src="/image/chart" width="300" height="200"></img>
      </div>
      <div class="card-footer">
        <a href="#" class="btn btn-primary">Go somewhere</a>
      </div>
    </div>
  </div>
</body>
</html>
```

![image](https://github.com/chunjoonsung/fastapi_webpack_chartjs_matplotlib/assets/33312464/b0df75c0-084d-4096-892f-0f79487a0589)





