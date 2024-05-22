# Copyright (c) 2024, siva and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobDetails(Document):
	pass

@frappe.whitelist()
def generate_project(docname):
    if not docname:
        frappe.msgprint("Document name is required to generate the waybill.")
        return

    doc = frappe.get_doc("Job Details", docname)

    if doc.project:
        frappe.throw(f"Project already exists for this Job: {doc.project}")
    else:
        data = frappe.get_doc({
            "doctype": "Project",
            "project_name": doc.name,
            "custom_job_details": doc.name,
            
        })
        data.insert(ignore_permissions=True)
        frappe.msgprint(f"Project generated successfully: {data.name}")

        doc.project = data.name
        doc.save(ignore_permissions=True)

        return doc.project