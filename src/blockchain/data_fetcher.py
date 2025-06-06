import requests

class DataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_from_etherscan(self, address):
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&apikey={self.api_key}"
        response = requests.get(url)
        return response.json()

    def fetch_from_the_graph(self, query):
        url = "https://api.thegraph.com/subgraphs/name/your-subgraph-name"
        response = requests.post(url, json={'query': query})
        return response.json()

    def fetch_from_alchemy(self, address):
        url = f"https://eth-mainnet.alchemyapi.io/v2/{self.api_key}/getAssetTransfers"
        params = {
            "fromBlock": "0x0",
            "toBlock": "latest",
            "fromAddress": address,
            "category": ["external", "internal", "erc20", "erc721", "erc1155"]
        }
        response = requests.post(url, json=params)
        return response.json()

    def get_wallet_data(self, address):
        etherscan_data = self.fetch_from_etherscan(address)
        # Example query for The Graph
        graph_query = f"{{ transactions(where: {{ from: \"{address}\" }}) {{ id, value }} }}"
        graph_data = self.fetch_from_the_graph(graph_query)
        alchemy_data = self.fetch_from_alchemy(address)

        return {
            "etherscan": etherscan_data,
            "the_graph": graph_data,
            "alchemy": alchemy_data
        }