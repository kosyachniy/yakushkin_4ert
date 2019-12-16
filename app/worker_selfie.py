from PIL import Image
import io
import json
from return_results import return_results
from hogmodel.detector import detect_faces
import logging


def construct_handler(th0=0.65, th1=0.2, th2=0.2, **kwargs):
    def handle_passport(ch, method, properties, body):
        logging.warning('in handler')
        jdata = json.loads(body.decode('utf-8'))
        image = Image.open(io.BytesIO(jdata['img']))
        id = jdata['id']
        logging.warning(f'{id} priletelo!!!!!!')
        return_results(id=id, correct=detect_faces(image))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    return handle_passport
