from behave import given, when, then
from primordia.integrity import verify_integrity
import datetime

@given('the Primordia AI system is active')
def step_impl(context):
    pass

@when('I request an integrity check')
def step_impl(context):
    context.response = verify_integrity()

@then('the system status should be "operational"')
def step_impl(context):
    assert context.response['status'] == 'operational'

@then('the response should contain a timestamp')
def step_impl(context):
    assert 'timestamp' in context.response
    assert isinstance(context.response['timestamp'], str)
