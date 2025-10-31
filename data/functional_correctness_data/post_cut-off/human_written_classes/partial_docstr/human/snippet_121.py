import requests
from genrl.blockchain.connections import get_contract, send_via_api, setup_web3
from genrl.logging_utils.global_defs import get_logger

class PRGCoordinator:
    """
    Coordinator for the PRG game. We don't need contract address or ABI because we rely on the modal proxy app
    to handle routing requests to the correct backend via the endpoints.
    """

    def __init__(self, org_id: str, modal_proxy_url: str) -> None:
        self.org_id = org_id
        self.modal_proxy_url = modal_proxy_url

    def bet_token_balance(self, peer_id: str) -> int:
        try:
            response = send_via_api(self.org_id, self.modal_proxy_url, 'bet-token-balance', {'peerId': peer_id})
            if isinstance(response, dict) and 'result' in response:
                return int(response['result'])
            else:
                get_logger().debug(f'Unexpected response format: {response}')
                return 0
        except requests.exceptions.HTTPError as e:
            if e.response is None or e.response.status_code != 500:
                raise
            get_logger().debug('Unknown error calling bet-token-balance endpoint! Continuing.')
            return 0

    def guess_answer(self, game_id: int, peer_id: str, clue_id: int, choice_idx: int, bet: int) -> None:
        try:
            send_via_api(self.org_id, self.modal_proxy_url, 'guess-answer', {'gameId': game_id, 'peerId': peer_id, 'clueId': clue_id, 'choiceIdx': choice_idx, 'bet': bet})
        except requests.exceptions.HTTPError as e:
            raise

    def claim_reward(self, game_id: int, peer_id: str) -> None:
        try:
            send_via_api(self.org_id, self.modal_proxy_url, 'claim-reward', {'gameId': game_id, 'peerId': peer_id})
        except requests.exceptions.HTTPError as e:
            raise