from flask import Flask, render_template, redirect, request, url_for
import requests
app = Flask(__name__)

group_id = 0
members = 4
access_token = ""

api_endpoint = 'https://utexas.instructure.com/api/v1'

@app.route("/")
def index():
  return render_template('index.html', members=members)

@app.route("/success")
def success():
  return render_template('success.html')

@app.route("/create", methods=['POST'])
def create():
  headers = {"Authorization": "Bearer " + access_token}

  # Create the group
  payload = {"name": request.form['name']}
  response = requests.post(api_endpoint + '/group_categories/' + str(group_id) + '/groups', headers=headers, data=payload)
  new_id = response.json()['id']

  # Add the members to the group
  for i in range(0, members):
    if request.form['email' + str(i)] is None:
      continue
    payload = {"invitees[]": request.form['email' + str(i)]}
    response = requests.post(api_endpoint + '/groups/' + str(new_id) + '/invite', headers=headers, data=payload)

  # Redirect on success
  return redirect(url_for('success'))

if __name__ == "__main__":
  app.debug = True
  app.run()
