# -*- coding: utf-8 -*-
# Copyright (c) 2019, Aerele Technologies Private Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from apparelo.apparelo.doctype.ipd_item_mapping.ipd_item_mapping import ipd_item_mapping
from apparelo.apparelo.doctype.ipd_bom_mapping.ipd_bom_mapping import ipd_bom_mapping

class ItemProductionDetail(Document):
	def on_submit(self):
		ipd_list=self.create_process_details()
		# ipd_item_mapping(ipd_list,self.name,self.item)
		# ipd_bom_mapping(ipd_list,self.name,self.item)

	def create_process_details(self):
		ipd = []
		attribute_set={}
		piece_count=None
		item_size=[]
		colour=[]
		for final_size in self.size:
			item_size.append(final_size.size)
		for final_colour in self.colour:
			colour.append(final_colour.colour)

		for process in self.processes:
			process_variants = {}
			if process.process_name == 'Knitting':
				process_variants['process'] = 'Knitting'
				process_variants['index']=process.idx
				process_variants['input_index']=''
				process_variants['input_item']=process.input_item
				if process.input_item:
					knitting_doc = frappe.get_doc('Knitting', process.process_record)
					variants = knitting_doc.create_variants([process.input_item])
					process_variants['variants'] = list(set(variants))
					boms=knitting_doc.create_boms([process.input_item], variants, attribute_set,item_size,colour,piece_count)
					process_variants['BOM']=list(set(boms))
					ipd.append(process_variants)
				elif process.input_index:
					pass
				continue

			if process.process_name == 'Dyeing':
				process_variants['process'] = 'Dyeing'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items = []
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								dyeing_doc = frappe.get_doc('Dyeing', process.process_record)
								variants.extend(dyeing_doc.create_variants(input_items))
								boms.extend(dyeing_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Steaming':
				process_variants['process'] = 'Steaming'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					variants=[]
					boms=[]
					input_items_= []
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								steaming_doc = frappe.get_doc('Steaming', process.process_record)
								variants.extend(steaming_doc.create_variants(input_items))
								boms.extend(steaming_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Compacting':
				process_variants['process'] = 'Compacting'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					variants=[]
					boms=[]
					input_items_= []
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								compacting_doc = frappe.get_doc('Compacting', process.process_record)
								variants.extend(compacting_doc.create_variants(input_items))
								boms.extend(compacting_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Bleaching':
				process_variants['process'] = 'Bleaching'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								bleaching_doc = frappe.get_doc('Bleaching', process.process_record)
								variants.extend(bleaching_doc.create_variants(input_items))
								boms.extend(bleaching_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Cutting':
				process_variants['process'] = 'Cutting'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					variants_=[]
					boms=[]
					input_items_= []
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								cutting_doc = frappe.get_doc('Cutting', process.process_record)
								variants,attribute_set = cutting_doc.create_variants(input_items,item_size)
								variants_.extend(variants)
								boms.extend(cutting_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants_))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Piece Printing':
				process_variants['process'] = 'Piece Printing'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								piece_printing_doc = frappe.get_doc('Piece Printing', process.process_record)
								variants.extend(piece_printing_doc.create_variants(input_items))
								boms.extend(piece_printing_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Stitching':
				process_variants['process'] = 'Stitching'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							if str(pro['index'])==input_index:
								input_items.extend(pro['variants'])
					stitching_doc = frappe.get_doc('Stitching', process.process_record)
					variants.extend(stitching_doc.create_variants(input_items,colour))
					boms.extend(stitching_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Label Fusing':
				process_variants['process'] = 'Label Fusing'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								label_fusing_doc = frappe.get_doc('Label Fusing', process.process_record)
								variants.extend(label_fusing_doc.create_variants(input_items))
								boms.extend(label_fusing_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue
				pr
			if process.process_name == 'Checking':
				process_variants['process'] = 'Checking'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								checking_doc = frappe.get_doc('Checking', process.process_record)
								variants.extend(checking_doc.create_variants(input_items))
								boms.extend(checking_doc.create_boms(input_items, variants,attribute_set,item_size,colour,piece_count))
					process_variants['variants'] =list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Ironing':
				process_variants['process'] = 'Ironing'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								ironing_doc = frappe.get_doc('Ironing', process.process_record)
								variants.extend(ironing_doc.create_variants(input_items))
								boms.extend(ironing_doc.create_boms(input_items, variants,attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue

			if process.process_name == 'Packing':
				index=process.idx
				process_variants['process'] = 'Packing'
				process_variants['index']=process.idx
				if process.input_item:
					pass
				elif process.input_index:
					input_items_= []
					variants_=[]
					boms=[]
					input_indexs = process.input_index.split(',')
					process_variants['input_index']=process.input_index
					for pro in ipd:
						for input_index in input_indexs:
							input_items=[]
							if str(pro['index'])==input_index:
								input_items=pro['variants']
								input_items_.extend(input_items)
								packing_doc = frappe.get_doc('Packing', process.process_record)
								variants,piece_count= packing_doc.create_variants(input_items,self.item)
								variants_.extend(variants)
								boms.extend(packing_doc.create_boms(input_items, variants, attribute_set,item_size,colour,piece_count))
					process_variants['variants'] = list(set(variants_))
					process_variants['BOM']=list(set(boms))
					process_variants['input_item']=list(set(input_items_))
					ipd.append(process_variants)
				continue
		# additional_process(ipd)
		print(ipd)
		return ipd

def additional_process(ipd):
	a=['Cutting to Packing']
	items={}
	for process in a:
			input_index=''
			input_item=[]
			process_variants={}
			variants=[]
			# process_variants['index']='A'+str(process.idx)
			process_variants['process']='Cutting to Packing'
			process_=frappe.get_doc("Multi Process",'Cutting to Packing')
			for ipd_ in ipd:
				if ipd_['process']=='Cutting':
					input_index=ipd_['input_index']
			for ipd_ in ipd:
				if str(ipd_['index'])==input_index:
					input_item=ipd_['variants']

				if ipd_['process']=='Packing':
					process_variants['variants']=ipd_['variants']
					process_variants['BOM']=ipd_['BOM']
			# print(input_item,process_variants['variants'],process_variants['BOM'])
			for item in input_item:
				items[item]=0
			for bom in process_variants['BOM']:
				bom_=frappe.get_doc("BOM",bom)
				additional_item={}
				for item in bom_.items:
					if item.bom_no=='':
						additional_item[item.item_code]=0
				additional_item,items=bom_item(bom,additional_item,input_item,items)
				print(additional_item,items)

def bom_item(bom,additional_item,variants,items):
	bom_=frappe.get_doc("BOM",bom)
	for item in bom_.items:
		if item.bom_no=='':
			additional_item[item.item_code]+=item.qty
		else:
			if item.item_code in variants:
				items[item.item_code]+=item.qty
			else:
				bom_item(item.bom_no,additional_item,variants,items)
	return additional_item,items