from ..util.postgresdb import PostgresDB
from ..daos.reimbursementrequestdao import ReimbursementRequestDAO
from ..entities.reimbursementrequest import ReimbursementRequest
from pathlib import Path
import json

credeitnal_file = open(
    f"{Path(__file__).parent.parent}\\config\\db_credentials.json")
credentials = json.load(credeitnal_file)
TABLE_NAME = "test_requests"
database = PostgresDB(credentials["host"],
                      credentials["username"],
                      credentials["password"])
request_dao = ReimbursementRequestDAO(database, TABLE_NAME)


def test_save_load_request():
    request = ReimbursementRequest("example@mail.com", 100,
                                   "Some reason", 100001)
    request_dao.save_object(request)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    request_dao.save_object(request)
    results = request_dao.load_objects(request.get_email())
    assert len(results) == 1
    result = results[0]
    assert result.get_email() == request.get_email()
    assert result.get_amount() == request.get_amount()
    assert result.get_closing_date() == request.get_closing_date()
    assert result.get_creation_date() == request.get_creation_date()
    assert result.get_id() != 0
    assert result.get_reason() == request.get_reason()
    assert result.get_responder() == request.get_responder()
    assert result.get_response() == request.get_response()


def test_load_multiple_requests():
    request1 = ReimbursementRequest("example@mail.com", 101,
                                    "Some reason1", 100001)
    request2 = ReimbursementRequest("example@mail.com", 102,
                                    "Some reason2", 100002)
    request_dao.save_object(request1)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    request_dao.save_object(request1)
    request_dao.save_object(request2)
    results = request_dao.load_objects(request1.get_email())
    assert len(results) == 2
    result1 = results[0]
    result2 = results[1]
    assert result1.get_email() == result2.get_email()
    assert result1.get_amount() != result2.get_amount()
    assert result1.get_creation_date() != result2.get_creation_date()
    assert result1.get_closing_date() == result2.get_closing_date()
    assert result1.get_id() != result2.get_id()
    assert result1.get_reason() != result2.get_reason()
    assert result1.get_responder() == result2.get_responder()
    assert result1.get_response() == result2.get_response()


def test_load_only_matching_requests():
    request1 = ReimbursementRequest("example@mail.com", 101,
                                    "Some reason1", 100001)
    request2 = ReimbursementRequest("example2@mail.com", 102,
                                    "Some reason2", 100002)
    request_dao.save_object(request1)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    request_dao.save_object(request1)
    request_dao.save_object(request2)
    results = request_dao.load_objects(request1.get_email())
    assert len(results) == 1


def test_remove_specific_request():
    request1 = ReimbursementRequest("example@mail.com", 101,
                                    "Some reason1", 100001)
    request2 = ReimbursementRequest("example2@mail.com", 102,
                                    "Some reason2", 100002)
    request_dao.save_object(request1)
    database.execute(f"DELETE FROM {TABLE_NAME}")
    request_dao.save_object(request1)
    request_dao.save_object(request2)
    results = request_dao.load_all_objects()
    assert len(results) == 2
    results = request_dao.load_objects(request1.get_email())
    assert len(results) == 1
    request_dao.remove_object(results[0].get_id())
    results = request_dao.load_objects(request1.get_email())
    assert len(results) == 0
    results = request_dao.load_all_objects()
    assert len(results) == 1
