// Copyright (c) 2024, siva and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Details", {
    refresh: function(frm) {
        add_custom_button(frm);
        frm.events.set_dashboard_indicators(frm); 
    },

    set_dashboard_indicators: function(frm) {
        function process_invoices(invoices, includeOutstanding = false) {
            var totals = { grandTotal: 0, outstandingTotal: 0 };
            if (invoices && invoices.length > 0) {
                invoices.forEach(function(invoice) {
                    totals.grandTotal += invoice.base_grand_total;
                    if (includeOutstanding) {
                        totals.outstandingTotal += invoice.outstanding_amount;
                    }
                });
            }
            return totals;
        }

        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Sales Invoice',
                filters: {
                    custom_job_number: frm.doc.name,
                    docstatus: 1
                },
                fields: ['base_grand_total', 'outstanding_amount']
            },
            callback: function(response) {
                var salesInvoiceTotals = process_invoices(response.message, true);

                frappe.call({
                    method: 'frappe.client.get_list',
                    args: {
                        doctype: 'Purchase Invoice',
                        filters: {
                            custom_job_number: frm.doc.name,
                            docstatus: 1
                        },
                        fields: ['base_grand_total', 'outstanding_amount']
                    },
                    callback: function(response) {
                        var purchaseInvoiceTotals = process_invoices(response.message, true);

                        var profitAndLoss = salesInvoiceTotals.grandTotal - purchaseInvoiceTotals.grandTotal;

                        frm.dashboard.add_indicator(__('Total Sales Invoice: {0}', [format_currency(salesInvoiceTotals.grandTotal, frm.doc.currency)]), 'blue');
                        frm.dashboard.add_indicator(__('Total Purchase Invoice: {0}', [format_currency(purchaseInvoiceTotals.grandTotal, frm.doc.currency)]), 'orange');
                        // frm.dashboard.add_indicator(__('Total Sales Outstanding: {0}', [format_currency(salesInvoiceTotals.outstandingTotal, frm.doc.currency)]), salesInvoiceTotals.outstandingTotal ? 'red' : 'green');
                        // frm.dashboard.add_indicator(__('Total Purchase Outstanding: {0}', [format_currency(purchaseInvoiceTotals.outstandingTotal, frm.doc.currency)]), purchaseInvoiceTotals.outstandingTotal ? 'red' : 'green');
                        frm.dashboard.add_indicator(__('Profit & Loss: {0}', [format_currency(profitAndLoss, frm.doc.currency)]), profitAndLoss >= 0 ? 'green' : 'red');

                    }
                    
                });
            }
        });
    }
});

function add_custom_button(frm) {
    frm.add_custom_button(__('Generate Project'), function() {
        frappe.call({
            method: 'logistics_management.logistics_management.doctype.job_details.job_details.generate_project',
            args: {
                docname: frm.docname
            },
            callback: function(response) {
                if (response.message) {
                    frm.reload_doc();
                    // frappe.msgprint('Waybill generated successfully.');
                }
            }
        });
    });
}
