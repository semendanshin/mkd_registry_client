import pprint
import httpx
from dadata import Dadata
from .types import DadataAddress, DadataPartyData


class DadataRepository:
    def __init__(self, token, secret):
        self.token = token
        self.dadata = Dadata(token, secret)

    def get_clean_data(self, address: str) -> DadataAddress:
        response = self.dadata.clean("address", address)
        return DadataAddress(**response)

    def get_clean_data_by_cadastral_number(self, cadastral_number: str) -> DadataAddress:
        response = self.dadata.find_by_id("address", cadastral_number, 1)
        if not response:
            return DadataAddress()
        return DadataAddress(**(response[0].get('data', {})), result=response[0].get('value', ''))

    def get_company_data(self, inn: str) -> DadataPartyData:
        response = self.dadata.find_by_id("party", inn, 1)
        pprint.pprint(response)
        if not response:
            return DadataPartyData()
        return DadataPartyData(**(response[0].get('data', {})), value=response[0].get('value', ''))
