from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reports_of_employees.db'

db = SQLAlchemy(app)

# Создаем таблицу в базе данных
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    department = db.Column(db.String(50)) #департамент сотрудника
    type = db.Column(db.String(50)) #тип оборудования
    description = db.Column(db.String(50)) #описание работы
    status = db.Column(db.String(50)) #статус работы

    def __init__(self, first_name, last_name, department, type, description, status):
        self.first_name = first_name
        self.last_name = last_name
        self.department = department
        self.type = type
        self.description = description
        self.status = status


with app.app_context():
    db.create_all()


# Метод для добавления репорта
@app.route('/add_report', methods=['POST'])
def add_report():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    department = request.form['department']
    type = request.form['type']
    description = request.form['description']
    status = request.form['status']
    report = Report(first_name, last_name, department, type, description, status)
    db.session.add(report)
    db.session.commit()
    return {"success": 'Report added successfully'}


# Метод для получения отчетов по id сотрудника
@app.route('/get_report/<int:id>')
def get_report(id):
    report = Report.query.get(id)
    if report:
        return jsonify({
            'first_name': report.first_name,
            'last_name':report.last_name,
            'department': report.department,
            'type': report.type,
            'description': report.description,
            'status': report.status
        })
    else:
        return {'error': f'This report of {id} id is not found'}

# Метод для получения списка всех отчетов
@app.route('/get_all_reports', methods=['GET'])
def get_all_reports():
    reports = Report.query.all()
    response = []
    for report in reports:
        response.append({
            'id': report.id,
            'first_name': report.first_name,
            'last_name': report.last_name,
            'department': report.department,
            'type': report.type,
            'description': report.description,
            'status': report.status
        })
    return jsonify(response)

# Метод для удаления базы данных
@app.route('/delete_db')
def delete_db():
    db.drop_all()  # Удаляем все таблицы из базы данных
    db.create_all()  # Создаем новые таблицы
    return {"success": 'Database deleted successfully'}

@app.route('/delete_last_report')
def delete_last_report():
    last_report = Report.query.order_by(Report.id.desc()).first()  # Получаем последнюю запись из базы данных
    if last_report:
        db.session.delete(last_report)  # Удаляем последнюю запись
        db.session.commit()
        return jsonify({"success": 'Last report deleted successfully'})
    return jsonify({"error": 'No report found to delete'})


if __name__ == "__main__":
    app.run(debug=True)
