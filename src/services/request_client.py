import requests

class HttpClient():
    def __init__(self):
        self.session = requests.Session()
        self.headers = {}
        self.timeout = 20
        self.url = ''
        self.body = {}
        self.params = {}
        self.response = None

    def set_header(self, key, value):
        self.headers[key] = value
        self.session.headers.update(self.headers)
        
    def set_headers(self, headers: dict):
        self.headers = headers
        self.session.headers.update(self.headers)

    def get_headers(self):
        return self.headers

    def delete_header(self, key):
        if key in self.headers:
            del self.headers[key]
            self.session.headers.pop(key, None)

    def set_body(self, body: dict):
        self.body = body
    
    def add_to_body(self, key, value):
        self.body[key] = value

    def get_body(self):
        return self.body
    
    def set_url(self, url: str):
        self.url = url

    def get_url(self) -> str:
        return self.url

    def set_params(self, params: dict):
        self.params = params

    def get_params(self) -> dict:
        return self.params

    def add_to_params(self, key, value):
        self.params[key] = value

    def delete_param(self, key):
        if key in self.params:
            del self.params[key]
    
    def get_request(self):
        self.response = self.session.get(self.url, timeout=self.timeout,params=self.params, headers=self.headers)

    def post_request(self):
        self.response = self.session.post(self.url, timeout=self.timeout,params=self.params, json=self.body, headers=self.headers)

    def delete_request(self):
        self.response = self.session.delete(self.url, timeout=self.timeout,params=self.params, json=self.body, headers=self.headers)

    def put_request(self):
        self.response = self.session.put(self.url, timeout=self.timeout,params=self.params, json=self.body, headers=self.headers)

    def patch_request(self):
        self.response = self.session.patch(self.url, timeout=self.timeout,params=self.params, json=self.body, headers=self.headers)

    def head_request(self):
        self.response = self.session.head(self.url, timeout=self.timeout,params=self.params, headers=self.headers)

    def get_response(self):
        return self.response
    
    def get_response_status_code(self):
        if self.response:
            return self.response.status_code
        return None

http_client = HttpClient()