from django.db import transaction

@transaction.commit_manually
def flush_transaction():
    """
    used to mannually commit the transaction
    """
    transaction.commit()
