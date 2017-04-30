import os
import re
import psycopg2

db_name = os.environ['dbname']
password = os.environ['password']
user = os.environ['user']
host = os.environ['host']


def _fetch_token(token):
    query = 'SELECT token FROM api_accesstoken WHERE token = %s'
    conn = psycopg2.connect(dbname=db_name,
                            host=host,
                            user=user,
                            password=password)

    cursor = conn.cursor()
    cursor.execute(query, (token, ))

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result


def handler(event, context):
    principalId = 'user'
    method_arn = event.get('methodArn')
    request_token = event.get('authorizationToken')

    if not request_token:
        raise Exception('No authorizationToken')

    policy = AuthPolicy(principalId)

    token = _fetch_token(request_token)
    if token:
        policy.allowMethod(method_arn)
    else:
        raise Exception('Unauthorized')

    authResponse = policy.build()
    return authResponse


class AuthPolicy(object):
    principalId = ""
    version = "2012-10-17"
    pathRegex = "^[/.a-zA-Z0-9-\*]+$"
    allowMethods = []
    denyMethods = []


    def __init__(self, principal):
        self.principalId = principal
        self.allowMethods = []

    def _addMethod(self, effect, method_arn, conditions=[]):
        resourceArn = method_arn

        if effect.lower() == "allow":
            self.allowMethods.append({
                'resourceArn' : resourceArn,
                'conditions' : conditions
            })

    def _getEmptyStatement(self, effect):
        statement = {
            'Action': 'execute-api:Invoke',
            'Effect': effect[:1].upper() + effect[1:].lower(),
            'Resource': []
        }

        return statement

    def _getStatementForEffect(self, effect, methods):
        statements = []

        if len(methods) > 0:
            statement = self._getEmptyStatement(effect)

            for curMethod in methods:
                if curMethod['conditions'] is None or len(curMethod['conditions']) == 0:
                    statement['Resource'].append(curMethod['resourceArn'])
                else:
                    conditionalStatement = self._getEmptyStatement(effect)
                    conditionalStatement['Resource'].append(curMethod['resourceArn'])
                    conditionalStatement['Condition'] = curMethod['conditions']
                    statements.append(conditionalStatement)

            statements.append(statement)

        return statements

    def allowMethod(self, method_arn):
        self._addMethod("Allow", method_arn)

    def build(self):
        if (self.allowMethods is None or len(self.allowMethods) == 0):
            raise NameError("No statements defined for the policy")

        policy = {
            'principalId' : self.principalId,
            'policyDocument' : {
                'Version' : self.version,
                'Statement' : []
            }
        }

        policy['policyDocument']['Statement'].extend(self._getStatementForEffect("Allow", self.allowMethods))

        return policy
