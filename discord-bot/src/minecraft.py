import requests
import os

class Minecraft():
  def __init__(self) -> None:
    self.base_url = os.getenv('MINECRAFT_SERVICE_URL')
  

  def __whitelist(self, command) -> dict:
    if ' add ' in command:
      body = {'username': command.split(' ')[-1]}
      return requests.post(f'{self.base_url}/whitelist', json=body).json().get('message')
    
    elif ' remove ' in command:
      body = {'username': command.split(' ')[-1]}
      return requests.delete(f'{self.base_url}/whitelist', json=body).json().get('message')
    
    elif ' list' in command:
      return requests.get(f'{self.base_url}/whitelist').json().get('players')
    
    else:
      return {'message': 'Unrecognized Command'}


  def __query(self, command) -> dict:
    if 'stats' in command:
      return requests.get(f'{self.base_url}/stats').json()
    
    if 'version' in command:
      return requests.get(f'{self.base_url}/version').json()


  def __run_command(self, command) -> dict:
    body = {'command': command}
    return requests.post(f'{self.base_url}/command', json=body).json().get('message')


  def handler(self, command) -> dict:
    print(command)
    category = command.split(' ')[0].lower()
    print(category)
    if category == 'whitelist':
      return self.__whitelist(command)

    elif category == 'get':
      return self.__query(command)
    
    else:
      print(f'Unprepared Command: {command}')
      return self.__run_command(command)
    
    