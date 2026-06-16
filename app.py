from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]
# Read operation
@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

# Create operation
@app.route('/add', methods = ['GET', 'POST'])
def add_transaction():
    if request.method == 'GET':
        return render_template('form.html')
    if request.method == 'POST':
        new = {
            'id': len(transactions) + 1, 
            'date': request.form['date'],
            'amount': float(request.form['amount'])
            }
        transactions.append(new)
        return redirect(url_for('get_transactions'))

# Update operation
@app.route('/update/<int:transaction_id>', methods = ['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])
        
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
                
        return redirect(url_for('get_transactions'))
        
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template('edit.html', transaction=transaction)
        
    return{'message', f'Transaction with id {transaction_id} not found.'}, 404

# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)  # Remove the transaction from the transactions list
            # Redirect to the transactions list page after deleting the transaction
            return redirect(url_for("get_transactions"))
    # If no transaction with the matching ID is found, return a 404 error
    return {"message": "Transaction not found"}, 404

@app.route('/search', methods = ['GET', 'POST'])
def search_transactions():
    if request.method == 'POST':
        min = float(request.form['min_amount'])
        max = float(request.form['max_amount'])
        filtered_transactions = [x for x in transactions if x['amount'] >= min and x['amount'] <= max]
        return render_template('transactions.html', transactions=filtered_transactions)
    return render_template('search.html')    

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)