from ontology.interop.System.ExecutionEngine import GetCallingScriptHash, GetEntryScriptHash
from ontology.interop.System.Runtime import CheckWitness
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.Ontology.Runtime import Base58ToAddress

ctx = GetContext()

APPROVAL_PREFIX = 'APPROVAL-PREFIX-KEY'
OWNER = Base58ToAddress('<BASE-58-ADDRESS')

def Main(operation, args):
    if operation == 'notProtectedFromCCA':
        Require(len(args) == 0)
        return notProtectedFromCCA()
    elif operation == 'protectedFromCCA':
        Require(len(args) == 0)
        return protectedFromCCA()
    elif operation == 'approveContract':
        Require(len(args) == 1)
        contractHash = args[0]
        return approveContract(contractHash)
    elif operation == 'unapproveContract':
        Require(len(args) == 1)
        contractHash = args[0]
        return unapproveContract(contractHash)
    elif operation == 'isApproved':
        Require(len(args) == 1)
        contractHash = args[0]
        return isApproved(contractHash)
    return False


def notProtectedFromCCA():
    return True


def protectedFromCCA():
    RequireApproved()
    return True


def approveContract(contractHash):
    RequireOwner()
    RequireNotContract()
    key = getApprovalKey(contractHash)
    Put(ctx, key, True)


def unapproveContract(contractHash):
    RequireOwner()
    RequireNotContract()
    key = getApprovalKey(contractHash)
    Delete(ctx, key)


def RequireApproved():
    callerHash = GetCallingScriptHash()
    entryHash = GetEntryScriptHash()
    if entryHash is not callerHash:
        approved = isApproved(callerHash)
        Require(approved)


def isApproved(contractHash):
    key = getApprovalKey(contractHash)
    return Get(ctx, key)


def getApprovalKey(contractHash):
    return concat(APPROVAL_PREFIX, contractHash)


def RequireOwner():
    Require(CheckWitness(OWNER))


def RequireNotContract():
    callerHash = GetCallingScriptHash()
    entryHash = GetEntryScriptHash()
    Require(callerHash == entryHash)


def Require(expr):
    if not expr:
        raise Exception('Expression resulted in false')
