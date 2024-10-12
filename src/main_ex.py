  from flask import Flask, request, jsonify
  from flask_cors import CORS

  app = Flask(__name__)
  CORS(app)

  # DB
  data_store = {}

  @app.route('/send_data', methods=['POST'])
  def send_data():
      user_id = request.json.get('user_id')
      data = request.json.get('data')
      data_store[user_id] = data
      return jsonify({'status': 'success'}), 200

  @app.route('/get_data/<user_id>', methods=['GET'])
  def get_data(user_id):
      data = data_store.get(user_id)
      return jsonify({'data': data}), 200 if data else (404, 'Data not found')

  if __name__ == '__main__':
      app.run(debug=True)
  
