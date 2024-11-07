from database_layer.database import Users, Receipts, Invoices, user_receipts, user_invoices, session


def add_test_receipt() -> None:
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
    receipts = [[receipt.id, receipt.receipt_name, receipt.receipt_description, receipt.receipt_amount] for receipt in all_receipts]

    return receipts


def add_test_invoice() -> None:
    for i in range(10):
        new_invoice = Invoices(invoice_name=f'Invoice {i}',
                               invoice_description=f"Gitara siema : {i}",
                               invoice_amount=f"{i*i}")
        session.add(new_invoice)
        session.commit()


def list_all_invoices() -> list:
    # Find all reports
    all_invoices = session.query(Invoices).all()

    # Collect report details into a list
    invoices = [[invoice.id, invoice.invoice_name, invoice.invoice_description, invoice.invoice_amount] for invoice in all_invoices]

    return invoices