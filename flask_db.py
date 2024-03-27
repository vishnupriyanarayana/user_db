from flask import Flask, request, jsonify


class UserDatabase:
    def __init__(self):
        self.users = {}

    def add_user(self, age, first_name, last_name, dob):
        user_id = first_name[:3] + last_name[:3] + dob[:2] + age
        if user_id not in self.users:
            self.users[user_id] = (age, first_name, last_name, dob)
            return True, "User added successfully."
        else:
            return False, "User already exists."

    def update_user(self, user_id, new_age=None, new_first_name=None, new_last_name=None, new_dob=None):
        if user_id in self.users:
            user_info = list(self.users[user_id])
            if new_age is not None:
                user_info[0] = new_age
            if new_first_name is not None:
                user_info[1] = new_first_name
            if new_last_name is not None:
                user_info[2] = new_last_name
            if new_dob is not None:
                user_info[3] = new_dob
            self.users[user_id] = tuple(user_info)
            return True, "User information updated successfully."
        else:
            return False, "User not found."

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            return True, "User removed successfully."
        else:
            return False, "User not found."

    def get_user(self, user_id):
        if user_id in self.users:
            return True, self.users[user_id]
        else:
            return False, None


# Initialize Flask app
app = Flask(__name__)
user_db = UserDatabase()


# API endpoint for adding a user
@app.route('/')
def home():
    return 'Welcome to user database'


@app.route('/database/')
def user_database():
    return jsonify(user_db.users)


@app.route('/database/add_user', methods=['POST'])
def add_user():
    data = request.json
    success, message = user_db.add_user(data['age'], data['first_name'], data['last_name'], data['dob'])
    return jsonify({'success': success, 'message': message})


# API endpoint for updating a user
@app.route('/database/update_user', methods=['PUT'])
def update_user():
    data = request.json

    updated_data = {}
    if "new_age" in data:
        updated_data["new_age"] = data["new_age"]
    elif "new_first_name" in data:
        updated_data["new_first_name"] = data["new_first_name"]
    elif "new_last_name" in data:
        updated_data["new_last_name"] = data["new_last_name"]
    elif "new_dob" in data:
        updated_data["new_dob"] = data["new_dob"]

    success, message = user_db.update_user(data['user_id'], **updated_data)
    return jsonify({'success': success, 'message': message})


# API endpoint for removing a user
@app.route('/database/remove_user', methods=['DELETE'])
def remove_user():
    data = request.json
    success, message = user_db.remove_user(user_id=data['user_id'])
    return jsonify({'success': success, 'message': message})


# API endpoint for getting a user
@app.route('/database/get_user', methods=['GET'])
def get_user():
    data = request.json
    success, user_info = user_db.get_user(user_id=data['user_id'])
    if success:
        return jsonify({'success': True, 'user_info': user_info})
    else:
        return jsonify({'success': False, 'message': 'User not found.'})


if __name__ == '__main__':
    app.run(debug=True)
