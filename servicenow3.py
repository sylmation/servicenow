import requests

class ServiceNowQuery:
    def __init__(self, instance_url, user, pwd):
        self.instance_url = instance_url
        self.user = user
        self.pwd = pwd
        self.session = requests.Session()
        self.session.auth = (self.user, self.pwd)
        self.session.headers.update({'Accept': 'application/json'})

    def query(self, table_name, sysparm_query=None, sysparm_fields=None, sysparm_display_value=None, sysparm_exclude_reference_link=None, **kwargs):
        query = ''
        # if sysparm_query is provided, add it to the query string
        if sysparm_query:
            query += f'sysparm_query={sysparm_query}'
        # Iterate over all the key value pair from kwargs and add them to the query string
        for key, value in kwargs.items():
            if value is True:
                query += f'{key}=true^'
            elif value is False:
                query += f'{key}=false^'
            elif value[0] == '!':
                query += f'{key}NOT{value[1:]}^'
            elif value[0] == '|':
                query += f'{key}{value}^'
            else:
                query += f'{key}={value}^'
        # if sysparm_display_value is passed, add it to the query string
        if sysparm_display_value or sysparm_display_value is None:
            query += 'sysparm_display_value=true^'
        # if sysparm_exclude_reference_link is passed, add it to the query string
        if sysparm_exclude_reference_link or sysparm_exclude_reference_link is None:
            query += 'sysparm_exclude_reference_link=true^'
         # if sysparm_fields is provided, add it to the query string
        if sysparm_fields:
            query += f'sysparm_fields={sysparm_fields}^'
        if query:
            self.session.params = {'sysparm_query': query[:-1]}
        response = self.session.get(f'{self.instance_url}/api/now/table/{table_name}')
        return response.json()

sn = ServiceNowQuery('https://yourinstance.service-now.com', 'your_user', 'your_password')
result = sn.query('incident', active='true', priority='!1', resolved=False, sysparm_display_value, sysparm_exclude_reference_link, sysparm_fields='number,short_description')
print(result)