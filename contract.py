from ontology.interop.System.ExecutionEngine import GetCallingScriptHash, GetEntryScriptHash
from ontology.interop.System.Runtime import CheckWitness
from ontology.interop.System.Storage import GetContext, Get, Put, Delete

ctx = GetContext()

APPROVAL_PREFIX = 'APPROVAL-PREFIX-KEY'

def Main(operation, args):
    if operation == 'notProtectedFromCCA':
        Require(len(args) == 1)
        addr = args[0]
        return notProtectedFromCCA(addr)
    elif operation == 'protectedFromCCA':
        Require(len(args) == 1)
        addr = args[0]
        return protectedFromCCA(addr)
    elif operation == 'approveContract':
        Require(len(args) == 2)
        addr = args[0]
        contractHash = args[1]
        return approveContract(addr, contractHash)
    elif operation == 'unapproveContract':
        Require(len(args) == 2)
        addr = args[0]
        contractHash = args[1]
        return unapproveContract(addr, contractHash)
    elif operation == 'isApproved':
        Require(len(args) == 2)
        addr = args[0]
        contractHash = args[1]
        return isApproved(addr, contractHash)
    return False


def notProtectedFromCCA(addr):
    RequireWitness(addr)
    return True


def protectedFromCCA(addr):
    RequireWitness(addr)
    RequireApproved(addr)
    return True


def approveContract(addr, contractHash):
    RequireWallet(addr)
    RequireWitness(addr)
    RequireNotContract()
    key = getApprovalKey(addr, contractHash)
    Put(ctx, key, True)


def unapproveContract(addr, contractHash):
    RequireWallet(addr)
    RequireWitness(addr)
    RequireNotContract()
    key = getApprovalKey(addr, contractHash)
    Delete(ctx, key)


def RequireApproved(addr):
    callerHash = GetCallingScriptHash()
    entryHash = GetEntryScriptHash()
    if entryHash is not callerHash:
        approved = isApproved(addr, callerHash)
        Require(approved)

def isApproved(addr, contractHash):
    RequireWallet(addr)
    key = getApprovalKey(addr, contractHash)
    return Get(ctx, key)


def getApprovalKey(addr, contractHash):
    return concat(concat(APPROVAL_PREFIX, addr), contractHash)


def RequireWitness(addr):
    Require(CheckWitness(addr))


def RequireWallet(addr):
    Require(len(addr) == 20)


def RequireNotContract():
    callerHash = GetCallingScriptHash()
    entryHash = GetEntryScriptHash()
    Require(callerHash == entryHash)


def Require(expr):
    if not expr:
        raise Exception('Expression resulted in false')
