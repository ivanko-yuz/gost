from flask import Flask, jsonify, request

from model.expense import Expense, ExpenseSchema
from model.income import Income, IncomeSchema
from model.transaction_type import TransactionType

app = Flask(__name__)

transactions = [
    Income('Salary', 5000),
    Income('Dividends', 200),
    Expense('pizza', 50),
    Expense('Rock Concert', 100)
]


@app.route('/incomes')
def get_incomes():
    schema = IncomeSchema(many=True)
    incomes = schema.dump(
        filter(lambda t: t.type == TransactionType.INCOME, transactions)
    )
    return jsonify(incomes.data)


@app.route('/incomes', methods=['POST'])
def add_income():
    income = IncomeSchema().load(request.get_json())
    transactions.append(income.data)
    return "", 204


@app.route('/expenses')
def get_expenses():
    schema = ExpenseSchema(many=True)
    expenses = schema.dump(
        filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
    )
    return jsonify(expenses.data)


@app.route('/expenses', methods=['POST'])
def add_expense():
    expense = ExpenseSchema().load(request.get_json())
    transactions.append(expense.data)
    return "", 204

#empDB=[
# {
# 'id':'101',
# 'name':'Saravanan S',
# 'title':'Technical Leader'
# },
# {
# 'id':'201',
# 'name':'Rajkumar P',
# 'title':'Sr Software Engineer'
# }
# ]


#@app.route('/empdb/employee',methods=['GET'])
#def getAllEmp():
#    return jsonify({'emps':empDB})
#@app.route('/empdb/employee/<empId>',methods=['GET'])


#def getEmp(empId):
#    usr = [ emp for emp in empDB if (emp['id'] == empId) ] 
#    return jsonify({'emp':usr})
#@app.route('/empdb/employee/<empId>',methods=['PUT'])


#def updateEmp(empId):
#    em = [ emp for emp in empDB if (emp['id'] == empId) ]
#    if 'name' in request.json : 
#        em[0]['name'] = request.json['name']
#    if 'title' in request.json:
#        em[0]['title'] = request.json['title']
#    return jsonify({'emp':em[0]})
#@app.route('/empdb/employee',methods=['POST'])


#def createEmp():
#    dat = {
#    'id':request.json['id'],
#    'name':request.json['name'],
#    'title':request.json['title']
#    }
#    empDB.append(dat)
#    return jsonify(dat)
#@app.route('/empdb/employee/<empId>',methods=['DELETE'])


#def deleteEmp(empId):
#    em = [ emp for emp in empDB if (emp['id'] == empId) ]
#    if len(em) == 0:
#       abort(404)
#    empDB.remove(em[0])
#    return jsonify({'response':'Success'})



if __name__ == '__main__':
    app.run(debug=True)