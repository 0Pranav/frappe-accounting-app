# -*- coding: utf-8 -*-
# Copyright (c) 2019, 0Pranav and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
# import NestedSet
from frappe.utils.nestedset import NestedSet

class Account(NestedSet):
	nsm_parent_field = "parent_tree"
