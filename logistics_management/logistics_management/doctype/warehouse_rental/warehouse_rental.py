# Copyright (c) 2024, siva and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import date_diff
from frappe.model.document import Document

class WarehouseRental(Document):
    def calculate_total_amount(self):
        months_rented = frappe.utils.date_diff(self.rent_end_date, self.rent_start_date) / 30.0
        self.months_rented = months_rented
        self.total_amount = self.rental_rate * self.rent_space * months_rented

    def validate(self):
        self.calculate_total_amount()

@frappe.whitelist()
def generate_invoice(docname):
    if not docname:
        frappe.msgprint("Document name is required to generate the invoice.")
        return

    doc = frappe.get_doc("Warehouse Rental", docname)

    if doc.status == "Occupied":
        if doc.invoice_number:
            return {"error": f"Sales Invoice already exists for this Warehouse Rental: {doc.invoice_number}"}
        else:
            doc.calculate_total_amount()

            invoice = frappe.get_doc({
                "doctype": "Sales Invoice",
                "customer": doc.customer,
                "custom_job_number": doc.job_details,
                "posting_date": frappe.utils.today(),
                "due_date": frappe.utils.add_days(frappe.utils.today(), 30),
                "items": [
                    {
                        "item_code": doc.warehouse_space_item,
                        "qty": 1,
                        "rate": doc.total_amount,
                        "amount": doc.total_amount
                    }
                ]
            })

            invoice.insert(ignore_permissions=True)
            frappe.msgprint(f"Sales Invoice generated successfully: {invoice.name}")

            # Update the existing Warehouse Rental document with the sales invoice number
            doc.invoice_number = invoice.name
            doc.save(ignore_permissions=True)

            return doc.invoice_number
    else:
        frappe.msgprint("Invoice generation is only allowed for 'Occupied' status.")