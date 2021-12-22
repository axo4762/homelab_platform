from flask import Flask, jsonify
from flask.globals import request
from mctools import RCONClient, QUERYClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


def minecraft_command(command) -> str:
  print(os.getenv('RCON_HOST'))
  print(os.getenv('RCON_PORT'))
  rcon = RCONClient(os.getenv('RCON_HOST'),os.getenv('RCON_PORT'))
  print(rcon)
  success = rcon.authenticate(os.getenv('RCON_PASSWORD'))
  print(rcon.is_connected())
  print(rcon.is_authenticated())
  print(success)

  return rcon.command(command).replace('\u001b[0m','')

  #raise ConnectionError('Failed to connect to RCON')


def minecraft_query() -> dict:
  query = QUERYClient(os.getenv('QUERY_HOST'),os.getenv('QUERY_PORT'))
  res = query.get_full_stats()

  if type(res) == dict:
    res['motd'] = res.get('motd').replace('\u001b[0m','')

    cleaned_players = []
    for player in res.get('players'):
      cleaned_players.append(player.replace('\u001b[0m',''))
    res['players'] = cleaned_players

    return res

  raise ConnectionError('Failed to connect to Query')


@app.route('/stats', methods=['GET'])
def stats():
  return jsonify(minecraft_query())


@app.route('/version', methods=['GET'])
def version():
  return jsonify(minecraft_query().get('version'))


@app.route('/whitelist', methods=['GET','POST','DELETE'])
def whitelist():
  if request.method == 'POST':
    data = request.get_json()
    return jsonify({
      'message': minecraft_command(f"whitelist add {data.get('username')}")
      })

  elif request.method == 'DELETE':
    data = request.get_json()
    return jsonify({
      'message': minecraft_command(f"whitelist remove {data.get('username')}")
      })

  else:
    return jsonify({
    'players': minecraft_command('whitelist list').split(': ')[1]
    })


@app.route('/command', methods=['POST'])
def command():
  data = request.get_json()
  return jsonify({
    'message': minecraft_command(data.get('command'))
    })


if __name__ == '__main__':
  #print(rcon_command("whitelist remove test"))
  app.run(host='0.0.0.0', port=5000)
