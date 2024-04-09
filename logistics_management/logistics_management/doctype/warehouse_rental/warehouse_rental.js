frappe.ui.form.on('Warehouse Rental', {
    refresh: function(frm) {
        frm.add_custom_button(__('Generate Invoice'), function() {
            frappe.call({
                method: 'logistics_management.logistics_management.doctype.warehouse_rental.warehouse_rental.generate_invoice',
                args: {
                    'docname': frm.docname
                },
                callback: function(r) {
                    if (r.message) {
                        if (r.message.error) {
                            frappe.msgprint({
                                title: __('Alert'),
                                message: r.message.error,
                                indicator: 'red'
                            });
                        } else if (r.message.invoice_number) {
                            frappe.show_alert({
                                message: __('Sales Invoice already exists: {0}', [r.message.invoice_number]),
                                indicator: 'orange'
                            });
                        } else {
                            frappe.show_alert({
                                message: __('Sales Invoice generated successfully: {0}', [r.message]),
                                indicator: 'green'
                            });
                        }
                    }
                }
            });
        });
    }
});