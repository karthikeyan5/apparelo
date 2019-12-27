# -*- coding: utf-8 -*-
# Copyright (c) 2019, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from erpnext import get_default_company, get_default_currency
from erpnext.controllers.item_variant import generate_keyed_value_combinations, get_variant
from apparelo.apparelo.utils.item_utils import get_attr_dict, get_item_attribute_set, create_variants
class Cutting(Document):
	def on_submit(self):
		create_item_attribute()
		create_item_template(self)

	def create_variants(self, input_item_names,size):
		input_items = []
		for input_item_name in set(input_item_names):
			input_items.append(frappe.get_doc('Item', input_item_name))
		attribute_set = get_item_attribute_set(list(map(lambda x: x.attributes, input_items)))
		variants = []
		if self.attribute_validate("Apparelo Colour", attribute_set["Apparelo Colour"]) and self.attribute_validate("Dia", attribute_set["Dia"]):
			parts = set(self.get_attribute_values("Part"))
			for part in parts:
				variant_attribute_set = {}
				variant_attribute_set['Part'] = [part]
				variant_attribute_set['Apparelo Colour'] = self.get_attribute_values('Apparelo Colour', part)
				cutting_size=self.get_attribute_values('Apparelo Size', part)
				size.sort()
				cutting_size.sort()
				if cutting_size==size:
					variant_attribute_set['Apparelo Size'] = cutting_size
					variants.extend(create_variants(self.item+" Cut Cloth", variant_attribute_set))
				else:
					frappe.throw(_("Size is not available"))
		else:
			frappe.throw(_("Cutting has more colours or Dia that is not available in the input"))
		return variants,variant_attribute_set

	def attribute_validate(self, attribute_name, input_attribute_values):
		return set(self.get_attribute_values(attribute_name)).issubset(set(input_attribute_values))


	def get_matching_details(self, part, size):
		# ToDo: Part Size combination may not be unique
		for detail in self.details:
			if detail.part == part[0] and detail.size == size[0]:
				return {"Dia": detail.dia, "Weight": detail.weight}

	def create_boms(self, input_item_names, variants):
		input_items = []
		for input_item_name in input_item_names:
			input_items.append(frappe.get_doc('Item', input_item_name))
		boms = []
		for variant in variants:
			var=frappe.get_doc('Item', variant)
			attr = get_attr_dict(var.attributes)
			attr.update(self.get_matching_details(attr["Part"], attr["Apparelo Size"]))
			for input_item in input_items:
				input_item_attr = get_attr_dict(input_item.attributes)
				if input_item_attr["Apparelo Colour"] == attr["Apparelo Colour"] and input_item_attr["Dia"] == attr["Dia"]:
					break
			existing_bom = frappe.db.get_value('BOM', {'item': variant}, 'name')
			if not existing_bom:
				bom = frappe.get_doc({
					"doctype": "BOM",
					"currency": get_default_currency(),
					"item": variant,
					"company": get_default_company(),
					"items": [
						{
							"item_code": input_item.name,
							"qty": attr["Weight"],
							"uom": 'Gram',
						}
					]
				})
				bom.save()
				bom.submit()
				boms.append(bom.name)
			else:
				boms.append(existing_bom)
		return boms

	def get_attribute_values(self, attribute_name, part=None):
		attribute_value = set()
		if attribute_name == "Apparelo Colour":
			if part == None:
				for colour_mapping in self.colour_mapping:
					attribute_value.add(colour_mapping.colour)
			elif part:
				for colour_mapping in self.colour_mapping:
					if colour_mapping.part == part:
						attribute_value.add(colour_mapping.colour)
		elif attribute_name == "Dia":
			for detail in self.details:
				if int(str(float(detail.dia)).split('.')[1]) > 0:
					attribute_value.add(str(detail.dia))
				else:
					attribute_value.add(str(detail.dia).split('.')[0])
		elif attribute_name == "Apparelo Size":
			if part == None:
				for detail in self.details:
					attribute_value.add(detail.size)
			elif part:
				for detail in self.details:
					if detail.part == part:
						attribute_value.add(detail.size)
		elif attribute_name == "Part":
			for detail in self.details:
					attribute_value.add(detail.part)
		elif attribute_name == "weight":
			for detail in self.details:
					attribute_value.add(detail.weight)
		return list(attribute_value)

def create_item_attribute():
	if not frappe.db.exists("Item Attribute", "Part"):
		frappe.get_doc({
			"doctype": "Item Attribute",
			"attribute_name": "Part",
			"item_attribute_values": [
				{
					"attribute_value" : "Front",
					"abbr" : "Front"
				},
				{
					"attribute_value" : "Back",
					"abbr" : "Back"
				},
				{
					"attribute_value" : "Panel",
					"abbr" : "Panel"
				},
				{
					"attribute_value" : "Sleeve",
					"abbr" : "Sleeve"
				}
			]
		}).save()

	items = []
	for num in range(35,120,5):
		items.append({"attribute_value" : str(num) +" cm","abbr" : str(num)+" cm"})
	if not frappe.db.exists("Item Attribute", "Apparelo Size"):
		frappe.get_doc({
			"doctype": "Item Attribute",
			"attribute_name": "Apparelo Size",
			"item_attribute_values": items
		}).save()

def create_item_template(self):
	if not frappe.db.exists("Item", self.item+" Cut Cloth"):
		item = frappe.get_doc({
			"doctype": "Item",
			"item_code": self.item+" Cut Cloth",
			"item_name": self.item+" Cut Cloth",
			"description":self.item+" Cut Cloth",
			"item_group": "Sub Assemblies",
			"stock_uom" : "Kg",
			"has_variants" : "1",
			"variant_based_on" : "Item Attribute",
			"is_sub_contracted_item": "1",
			"attributes" : [
				{
					"attribute" : "Apparelo Colour"
				},
				{
					"attribute" : "Part"
				},
				{
					"attribute" : "Apparelo Size"
				}
			]
		})
		item.save()