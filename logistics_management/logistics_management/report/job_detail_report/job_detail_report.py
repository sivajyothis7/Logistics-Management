# Assuming this code is placed in a file named job_detail_report.py within your custom app
import frappe
from frappe import _, msgprint

def get_columns():
    return [
        {
            'fieldname': 'name',
            'label': _('Name'),
            'fieldtype': 'Link',
            'options': 'Job Details',
            'width': '200'
        },
        {
            'fieldname': 'customer',
            'label': _('Customer'),
            'fieldtype': 'Link',
            'options': 'Customer',
            'width': '200'
        },
        
        {
            'fieldname': 'job_status',
            'label': _('Job Status'),
            'fieldtype': 'Select',
            'options': 'Pending\nIn Progress\nCompleted\nOn Hold\nCancelled',
            'width': '250'
        },
        {
            'fieldname': 'created_user',
            'label': _('Created User'),
            'fieldtype': 'Link',
            'options': 'User',
            'width': '250'
        },
        {
            'fieldname': 'sales_person',
            'label': _('Sales Person'),
            'fieldtype': 'Link',
            'options': 'Sales Partner',
            'width': '200'
        },
        {
            'fieldname': 'amount',
            'label': _('Amount'),
            'fieldtype': 'Float',
            'width': '100'


        }
    ]

def get_data(filters):
    fields = ['name','job_id', 'job_status', 'created_user', 'sales_person','amount']

    data = frappe.get_all('Job Details', fields=fields, filters=filters)

    return data


def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    data = get_data(filters)

    return columns, data
