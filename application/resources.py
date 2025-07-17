from flask_restful import Api, Resource, reqparse
from .models import *
from flask_security import auth_required, roles_accepted, current_user

api = Api()

def roles_list(roles):
    role_list = []
    for role in roles:
        role_list.append(role.name)
    return role_list

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
            this_trans['user'] = transaction.user_id
            trans_jsons.append(this_trans)
        
        if trans_jsons:
            return trans_jsons
        
        return {
            "message" : "No transactions found"
        }, 404
    
api.add_resource(TransApi, '/api/get')
