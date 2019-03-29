# coding: utf-8
from openerp.tests.common import TransactionCase


class TestSupplierMinQty(TransactionCase):
    def setUp(self):
        super(TestSupplierMinQty, self).setUp()
        company = self.env['res.company'].create({
            'name': 'Test Company',
            'currency_id': self.env.ref('base.EUR').id,
            'country_id': self.env.ref('base.fr').id,
        })
        user = self.env.ref('base.user_demo')
        product = self.env.ref('product.product_product_48')
        product.seller_ids.unlink()
        self.env['product.supplierinfo'].create({
            'product_tmpl_id': product.product_tmpl_id.id,
            'name': self.env.ref('base.res_partner_16').id,
            'min_qty': 2,
            'company_id': user.company_id.id,
            'sequence': 2,
        })
        self.env['product.supplierinfo'].create({
            'product_tmpl_id': product.product_tmpl_id.id,
            'name': self.env.ref('base.res_partner_16').id,
            'min_qty': 5,
            'company_id': company.id,
            'sequence': 1,
        })
        self.procurement = self.env(user=user)['procurement.order'].create({
            'name': __name__,
            'product_id': product.id,
            'product_qty': 1,
            'product_uom': product.uom_id.id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'procure_method': 'make_to_order'
        })

    def test_supplier_min_qty(self):
        self.procurement.run()
        self.assertTrue(self.procurement.purchase_line_id)
        self.assertEqual(self.procurement.purchase_line_id.product_qty, 2)
