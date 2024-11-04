from database import Users, Receipts, Invoices, user_receipts, user_invoices, session


def add_receipt() -> None:
    for i in range(10):
        new_receipt = Receipts(receipt_name=f'Receipt {i}',
                               receipt_description=f"{i} : {i} : {i}",
                               receipt_amount=f"{i^2}")
        session.add(new_receipt)
        session.commit()


def list_all_receipts() -> list:
    # Find all reports
    all_receipts = session.query(Receipts).all()

    # Collect report details into a list
    receipts = [[receipt.id, receipt.receipt_name, receipt.description, receipt.file_name] for receipt in all_receipts]

    return receipts
