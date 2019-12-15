from PIL import Image
import io
import json
import numpy as np
from .return_results import return_results
from .mtcnn.detector import detect_faces


def construct_handler(th0=0.65, th1=0.2, th2=0.2, **kwargs):
    def handle_passport(ch, method, properties, body):
        jdata = json.loads(body.decode('utf-8'))
        image = Image.open(io.BytesIO(jdata['img']))
        return_results(correct=compute_result(image))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def compute_result(image, th0=th0, th1=th1, th2=th2, **ignore) -> bool:
        bounding_boxes, _ = detect_faces(image)
        if len(bounding_boxes) == 0 or th0 > np.max(bounding_boxes[:, -1]):
            return False
        if len(bounding_boxes) > 1:
            sbb = sorted(bounding_boxes, key=lambda x: x[-1], reverse=True)[:2]
            if sbb[0][-1] - sbb[1][-1] > th2:
                if (sbb[0][2] - sbb[0][0]) * (sbb[0][3] - sbb[0][1]) / np.product(image.size) > th1:
                    return True
        elif len(bounding_boxes) == 1:
            if (bounding_boxes[0, 2] - bounding_boxes[0, 2]) * \
                    (bounding_boxes[0, 2] - bounding_boxes[0, 2]) / \
                    np.product(image.size) > th1:
                return True
        return False

    return handle_passport
