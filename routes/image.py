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
