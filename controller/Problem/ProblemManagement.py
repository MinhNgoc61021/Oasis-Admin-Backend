import pytz
from flask import (
    Blueprint,
    # Blueprint is a way to organize a group of related views and other code
    # There will be 2 blueprints: one for authentication and one for posts function
    request,
    jsonify
)
from db.oasis_entites import Problem, ProblemCategory
from datetime import datetime

problem = Blueprint('ProblemManagement', __name__, url_prefix='/problem')


@problem.route('/records', methods=['GET'])
def get_records():
    try:
        page_index = request.args.get('page_index')
        per_page = request.args.get('per_page')
        sort_field = request.args.get('sort_field')
        sort_order = request.args.get('sort_order')
        record = Problem.getRecord(page_index, per_page, sort_field, sort_order)

        return jsonify({
            'status': 'success',
            'records': record[0],
            'page_number': record[1].page_number,
            'page_size': record[1].page_size,
            'num_pages': record[1].num_pages,
            'total_results': record[1].total_results
        }), 200
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400


@problem.route('/create-record', methods=['POST'])
def create():
    try:
        new_problem = request.get_json()
        title = new_problem.get('new_title')
        problem_statement = new_problem.get('new_problem_statement')
        input_format = new_problem.get('new_input_format')
        constraints = new_problem.get('new_constraints')
        output_format = new_problem.get('new_output_format')
        junit_rate = new_problem.get('new_junit_rate')
        mark_io = new_problem.get('new_mark_io')
        mark_junit = new_problem.get('new_mark_junit')
        level = new_problem.get('new_level')
        point = new_problem.get('new_point')
        submit_type = new_problem.get('new_submit_type')
        sample_code = new_problem.get('new_sample_code')
        category_id = new_problem.get('category_id')
        created_at = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        mark_parser = new_problem.get('new_mark_parser')
        parser_rate = new_problem.get('new_parser_rate')
        print()
        isProblemCreated = Problem.createRecord(created_at, title, problem_statement, input_format, constraints,
                                                output_format, int(level), int(point),
                                                float(junit_rate), mark_io, int(mark_junit), int(mark_parser), float(parser_rate),
                                                submit_type, sample_code, category_id)
        if isProblemCreated is True:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'already-exist'}), 202
    except Exception as e:
        return jsonify({'status': 'bad-request', 'error_message': e.__str__()}), 400
