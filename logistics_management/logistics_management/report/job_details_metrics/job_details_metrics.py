import frappe
from frappe.utils import flt

def execute(filters=None):
    columns, data = [], []

    columns = [
        {"label": "Job Details", "fieldname": "job_details", "fieldtype": "Link", "options": "Job Details", "width": 200},
        {"label": "Invoice Type", "fieldname": "invoice_type", "fieldtype": "Data", "width": 175},
        {"label": "Invoice ID", "fieldname": "invoice_id", "fieldtype": "Dynamic Link", "options": "invoice_type", "width": 200},
        {"label": "Grand Total", "fieldname": "base_grand_total", "fieldtype": "Currency", "width": 200},
        {"label": "Profit & Loss", "fieldname": "profit_and_loss", "fieldtype": "Currency", "width": 150},
        {"label": "Outstanding Amount", "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 200},
    ]

    job_details_filter = filters.get('job_details') if filters else None

    job_details_list = []
    if job_details_filter:
        job_details_list = frappe.get_all('Job Details', filters={'name': ['in', job_details_filter]}, fields=['name'])
    else:
        job_details_list = frappe.get_all('Job Details', fields=['name'])

    overall_sales_invoice_total = 0
    overall_purchase_invoice_total = 0
    overall_journal_entry_total = 0
    overall_sales_outstanding_total = 0
    overall_purchase_outstanding_total = 0
    overall_profit_and_loss = 0

    for job in job_details_list:
        total_sales_invoice = 0
        total_purchase_invoice = 0
        total_journal_entry = 0
        total_sales_outstanding = 0
        total_purchase_outstanding = 0

        sales_invoices = frappe.get_all('Sales Invoice', filters={'custom_job_number': job.name, 'docstatus': 1}, fields=['name', 'base_grand_total', 'outstanding_amount'])
        for inv in sales_invoices:
            total_sales_invoice += flt(inv.base_grand_total)
            total_sales_outstanding += flt(inv.outstanding_amount)
            data.append({
                'job_details': job.name,
                'invoice_type': 'Sales Invoice',
                'invoice_id': inv.name,
                'base_grand_total': flt(inv.base_grand_total),
                'outstanding_amount': flt(inv.outstanding_amount),
                'profit_and_loss': ''
            })

        purchase_invoices = frappe.get_all('Purchase Invoice', filters={'custom_job_number': job.name, 'docstatus': 1}, fields=['name', 'base_grand_total', 'outstanding_amount'])
        for inv in purchase_invoices:
            total_purchase_invoice += flt(inv.base_grand_total)
            total_purchase_outstanding += flt(inv.outstanding_amount)
            data.append({
                'job_details': job.name,
                'invoice_type': 'Purchase Invoice',
                'invoice_id': inv.name,
                'base_grand_total': flt(inv.base_grand_total),
                'outstanding_amount': flt(inv.outstanding_amount),
                'profit_and_loss': ''
            })

        journal_entries = frappe.get_all('Journal Entry', filters={'custom_job_number': job.name, 'docstatus': 1}, fields=['name', 'total_debit'])
        for entry in journal_entries:
            total_journal_entry += flt(entry.total_debit)
            data.append({
                'job_details': job.name,
                'invoice_type': 'Journal Entry',
                'invoice_id': entry.name,
                'base_grand_total': flt(entry.total_debit),
                'outstanding_amount': '',
                'profit_and_loss': ''
            })

        profit_and_loss = total_sales_invoice - (total_purchase_invoice + total_journal_entry)
        overall_profit_and_loss += profit_and_loss

        data.append({
            'job_details': '',  
            'invoice_type': '<b>Profit & Loss</b>',
            'invoice_id': None,
            'base_grand_total': None,
            'outstanding_amount': total_sales_outstanding + total_purchase_outstanding,
            'profit_and_loss': profit_and_loss
        })

        overall_sales_invoice_total += total_sales_invoice
        overall_purchase_invoice_total += total_purchase_invoice
        overall_journal_entry_total += total_journal_entry
        overall_sales_outstanding_total += total_sales_outstanding
        overall_purchase_outstanding_total += total_purchase_outstanding

    data.append({
        'job_details': '',  
        'invoice_type': '<b>Overall Profit & Loss</b>',
        'invoice_id': None,
        'base_grand_total': None,
        'outstanding_amount': overall_sales_outstanding_total + overall_purchase_outstanding_total,
        'profit_and_loss': overall_profit_and_loss
    })

    return columns, data
