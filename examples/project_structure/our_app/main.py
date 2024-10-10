import logging
import uvicorn

from endpoints import app


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8080)
