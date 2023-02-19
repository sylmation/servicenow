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
        if sysparm_query:
            url += f'?sysparm_query={sysparm_query}'
        else:
            url += '?'
            for key, value in kwargs.items():
                if value[0] == '!':
                    url += f'{key}NOT{value[1:]}^'
                elif value[0] == '|':
                    url += f'{key}{value}^'
                else:
                    url += f'{key}={value}^'
        response = requests.get(url, auth=(self.user, self.pwd), headers=self.headers)
        return response.json()


sn = ServiceNowQuery('https://yourinstance.service-now.com', 'your_user', 'your_password')
result = sn.query('incident', active='true', priority='!1|2')
print(result)
