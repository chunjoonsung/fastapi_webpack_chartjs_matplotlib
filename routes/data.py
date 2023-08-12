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
