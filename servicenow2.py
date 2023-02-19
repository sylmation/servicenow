import requests

class ServiceNowQuery:
    def __init__(self, instance_url, user, pwd):
        self.instance_url = instance_url
        self.user = user
        self.pwd = pwd
        self.headers = {
            'Accept': 'application/json'
        }

    def query(self, table_name, sysparm_query=None, **kwargs):
        url = f'{self.instance_url}/api/now/table/{table_name}'
        query = []
        if sysparm_query:
            query.append(sysparm_query)
        for key, value in kwargs.items():
            if value[0] == '!':
                query.append(f'{key}NOT{value[1:]}')
            elif value[0] == '|':
                query.append(f'{key}{value}')
            else:
                query.append(f'{key}={value}')
        if query:
            url += f'?sysparm_query={'^'.join(query)}'
        response = requests.get(url, auth=(self.user, self.pwd), headers=self.headers)
        return response.json()
