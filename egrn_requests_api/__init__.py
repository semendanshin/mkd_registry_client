from .egrn_requests_repo import EGRNRequestsAPI
from config import config

egrn_requests_api = EGRNRequestsAPI(host=config.EGRN_REQUESTS_API_HOST)