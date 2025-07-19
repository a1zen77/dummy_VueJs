from flask_restful import Api, Resource, reqparse
from .models import *
from flask_security import auth_required, roles_accepted, roles_required, current_user

api = Api()

def roles_list(roles):
    role_list = []
    for role in roles:
        role_list.append(role.name)
    return role_list

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('type')
parser.add_argument('date')
parser.add_argument('source')
parser.add_argument('destination')
parser.add_argument('description')

class TransApi(Resource):
    @auth_required('token')
    @roles_accepted('user', 'admin')
    def get(self):
        transaction = []
        trans_jsons = []
        if "admin" in roles_list(current_user.roles):
            transactions = Transaction.query.all()
        else:
            transactions = current_user.trans
        for transaction in transactions:
            this_trans = {}
            this_trans['id'] = transaction.id
            this_trans['name'] = transaction.name
            this_trans['type'] = transaction.type
            this_trans['date'] = transaction.date
            this_trans['delivery'] = transaction.delivery
            this_trans['source'] = transaction.source
            this_trans['destination'] = transaction.destination
            this_trans['internal_status'] = transaction.internal_status
            this_trans['delivery_status'] = transaction.delivary_status
            this_trans['description'] = transaction.description
            this_trans['user'] = transaction.bearer.username
            trans_jsons.append(this_trans)
        
        if trans_jsons:
            return trans_jsons
        
        return {
            "message" : "No transactions found"
        }, 404
    @auth_required('token')
    @roles_required('user')
    def post(self):
        args = parser.parse_args()
        try:
            transaction = Transaction(name = args['name'], 
                                  type = args['type'], 
                                  date = args['date'], 
                                  source = args['source'], 
                                  destination = args['destination'], 
                                  description = args['description'],
                                  user_id = current_user.id)
            db.session.add(transaction)
            db.session.commit()
            return {
                "message" : "Transaction created successfully"
            }, 201
        except:
            return {
                "message" : "One or more fields are missing"
            }, 400

    @auth_required('token')
    @roles_required('user')    
    def put(self, trans_id):
        args = parser.parse_args()
        trans = Transaction.query.get(trans_id)
        trans.name = args['name']
        trans.type = args['type']
        trans.date = args['date']
        trans.source = args['source']
        trans.destination = args['destination']
        trans.description = args['description']
        db.session.commit()
        return {
            "message" : "Transaction updated successfully"
        }, 200
    
    @auth_required('token')
    @roles_required('user')
    def delete(self, trans_id):
        trans = Transaction.query.get(trans_id)
        if trans:
            db.session.delete(trans)
            db.session.commit()
            return {
                "message": "Transaction deleted successfully"
            }, 200
        else:
            return {
                "message": "Transaction not found"
            }, 404
        
api.add_resource(TransApi, '/api/get', '/api/create', '/api/update/<int:trans_id>', '/api/delete/<int:trans_id>')
