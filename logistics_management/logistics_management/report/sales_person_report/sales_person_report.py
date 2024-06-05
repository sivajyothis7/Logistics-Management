# Copyright (c) 2024, siva and contributors
# For license information, please see license.txt

from frappe.utils import flt
import frappe

def execute(filters=None):
    columns, data = [], []

    # Define columns
    columns = [
        {"label": "Job Details", "fieldname": "job_details", "fieldtype": "Link", "options": "Job Details", "width": 125},
        {"label": "Invoice Type", "fieldname": "invoice_type", "fieldtype": "Data", "width": 135},
        {"label": "Invoice ID", "fieldname": "invoice_id", "fieldtype": "Dynamic Link", "options": "invoice_type", "width": 195},
        {"label": "Item", "fieldname": "item", "fieldtype": "Data", "width": 175},
        {"label": "Quantity", "fieldname": "quantity", "fieldtype": "Float", "width": 100},
        {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 150},
        {"label": "Credit", "fieldname": "credit", "fieldtype": "Currency", "width": 150},
        {"label": "Debit", "fieldname": "debit", "fieldtype": "Currency", "width": 150},
        # {"label": "Sales Outstanding", "fieldname": "sales_outstanding_amount", "fieldtype": "Currency", "width": 170},
        # {"label": "Purchase Outstanding", "fieldname": "purchase_outstanding_amount", "fieldtype": "Currency", "width": 175},
        {"label": "Profit & Loss", "fieldname": "profit_and_loss", "fieldtype": "Currency", "width": 150},
    ]

    # Get filters
    job_details_filter = filters.get('job_details') if filters else None
    sales_person_filter = filters.get('sales_person') if filters else None
    from_date = filters.get('from_date') if filters else None
    to_date = filters.get('to_date') if filters else None

    # Fetch job details based on filters
    job_details_filters = {}
    if job_details_filter:
        job_details_filters['name'] = ['in', job_details_filter]
    if sales_person_filter:
        job_details_filters['sales_person'] = ['in', sales_person_filter]
    if from_date and to_date:
        job_details_filters['date'] = ['between', [from_date, to_date]]  

    job_details_list = frappe.get_all('Job Details', filters=job_details_filters, fields=['name'])

    overall_credit_total = 0
    overall_debit_total = 0
    overall_sales_outstanding_total = 0
    overall_purchase_outstanding_total = 0
    overall_profit_and_loss = 0

    has_data = False

    for job in job_details_list:
        total_credit = 0
        total_debit = 0
        total_sales_outstanding = 0
        total_purchase_outstanding = 0

        # Fetch and process Sales Invoices
        sales_invoices_filters = {'custom_job_number': job.name, 'docstatus': 1}
        if sales_person_filter:
            sales_invoices_filters['sales_person'] = ['in', sales_person_filter]

        sales_invoices = frappe.get_all('Sales Invoice', filters=sales_invoices_filters, fields=['name', 'base_grand_total', 'outstanding_amount'])
        if sales_invoices:
            has_data = True
        for inv in sales_invoices:
            items = frappe.get_all('Sales Invoice Item', filters={'parent': inv.name}, fields=['item_code', 'qty', 'rate', 'amount'])
            for item in items:
                data.append({
                    'job_details': job.name,
                    'invoice_type': 'Sales Invoice',
                    'invoice_id': inv.name,
                    'item': item.item_code,
                    'quantity': item.qty,
                    'rate': item.rate,
                    'amount': item.amount,
                    'credit': flt(item.amount),
                    'debit': 0,
                    'sales_outstanding_amount': flt(inv.outstanding_amount),
                    'purchase_outstanding_amount': 0,
                    'profit_and_loss': ''
                })
            total_credit += flt(inv.base_grand_total)
            total_sales_outstanding += flt(inv.outstanding_amount)

        # Fetch and process Purchase Invoices
        purchase_invoices_filters = {'custom_job_number': job.name, 'docstatus': 1}

        purchase_invoices = frappe.get_all('Purchase Invoice', filters=purchase_invoices_filters, fields=['name', 'base_grand_total', 'outstanding_amount'])
        if purchase_invoices:
            has_data = True
        for inv in purchase_invoices:
            items = frappe.get_all('Purchase Invoice Item', filters={'parent': inv.name}, fields=['item_code', 'qty', 'rate', 'amount'])
            for item in items:
                data.append({
                    'job_details': job.name,
                    'invoice_type': 'Purchase Invoice',
                    'invoice_id': inv.name,
                    'item': item.item_code,
                    'quantity': item.qty,
                    'rate': item.rate,
                    'amount': item.amount,
                    'credit': 0,
                    'debit': flt(item.amount),
                    'sales_outstanding_amount': 0,
                    'purchase_outstanding_amount': flt(inv.outstanding_amount),
                    'profit_and_loss': ''
                })
            total_debit += flt(inv.base_grand_total)
            total_purchase_outstanding += flt(inv.outstanding_amount)

        # Fetch and process Journal Entries (only debit items)
        journal_entries_filters = {'custom_job_number': job.name, 'docstatus': 1}

        journal_entries = frappe.get_all('Journal Entry', filters=journal_entries_filters, fields=['name'])
        if journal_entries:
            has_data = True
        for entry in journal_entries:
            entries = frappe.get_all('Journal Entry Account', filters={'parent': entry.name, 'debit': ['>', 0]}, fields=['account', 'debit'])
            for je in entries:
                data.append({
                    'job_details': job.name,
                    'invoice_type': 'Journal Entry',
                    'invoice_id': entry.name,
                    'item': je.account,
                    'quantity': '',
                    'rate': '',
                    'amount': je.debit,
                    'credit': 0,
                    'debit': flt(je.debit),
                    'sales_outstanding_amount': '',
                    'purchase_outstanding_amount': '',
                    'profit_and_loss': ''
                })
                total_debit += flt(je.debit)

        # Calculate profit and loss
        if has_data:
            profit_and_loss = total_credit - total_debit
            overall_profit_and_loss += profit_and_loss

            # Append totals for each job
            data.append({
                'job_details': job.name,
                'invoice_type': '<b>Totals</b>',
                'invoice_id': '',
                'item': '',
                'quantity': '',
                'rate': '',
                'amount': '',
                'credit': total_credit,
                'debit': total_debit,
                'sales_outstanding_amount': total_sales_outstanding,
                'purchase_outstanding_amount': total_purchase_outstanding,
                'profit_and_loss': profit_and_loss
            })

            overall_credit_total += total_credit
            overall_debit_total += total_debit
            overall_sales_outstanding_total += total_sales_outstanding
            overall_purchase_outstanding_total += total_purchase_outstanding

    if not has_data:
        frappe.msgprint("No data found for the selected period")

    # Append overall totals if data is present
    if has_data:
        data.append({
            'job_details': '',
            'invoice_type': '<b>Overall Totals</b>',
            'invoice_id': '',
            'item': '',
            'quantity': '',
            'rate': '',
            'amount': '',
            'credit': overall_credit_total,
            'debit': overall_debit_total,
            'sales_outstanding_amount': overall_sales_outstanding_total,
            'purchase_outstanding_amount': overall_purchase_outstanding_total,
            'profit_and_loss': overall_profit_and_loss
        })

    return columns, data
