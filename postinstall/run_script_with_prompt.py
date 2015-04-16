import os
from datahub import DataHub
from datahub.constants import *
from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import THttpClient
from thrift.transport import TTransport
import secret
import pdb

import os
import csv

''' 
		This is a convenience program allowing app owners to query accross multiple
		user repos that run their apps.

		This program assumes that the DHAPPID and DHAPPTOKEN specified in secret.py
		have been authorized to operate on the "getfit" repo in your DataHub account.

		Be forwarned, the getfit.results table will be dropped and overwritten.

		to run:

			$ python 
			>>> from run_script_with_prompt import *
'''

resultArray = [];
typeDict = {16: "bool",
17: "bytea",
18: "char",
19: "name",
20: "int8",
21: "int2",
22: "int2vector",
23: "int4",
24: "regproc",
25: "text",
26: "oid",
27: "tid",
28: "xid",
29: "cid",
30: "oidvector",
71: "pg_type",
75: "pg_attribute",
81: "pg_proc",
83: "pg_class",
114: "json",
142: "xml",
143: "_xml",
199: "_json",
194: "pg_node_tree",
210: "smgr",
600: "point",
601: "lseg",
602: "path",
603: "box",
604: "polygon",
628: "line",
629: "_line",
700: "float4",
701: "float8",
702: "abstime",
703: "reltime",
704: "tinterval",
705: "unknown",
718: "circle",
719: "_circle",
790: "money",
791: "_money",
829: "macaddr",
869: "inet",
650: "cidr",
1000: "_bool",
1001: "_bytea",
1002: "_char",
1003: "_name",
1005: "_int2",
1006: "_int2vector",
1007: "_int4",
1008: "_regproc",
1009: "_text",
1028: "_oid",
1010: "_tid",
1011: "_xid",
1012: "_cid",
1013: "_oidvector",
1014: "_bpchar",
1015: "_varchar",
1016: "_int8",
1017: "_point",
1018: "_lseg",
1019: "_path",
1020: "_box",
1021: "_float4",
1022: "_float8",
1023: "_abstime",
1024: "_reltime",
1025: "_tinterval",
1027: "_polygon",
1033: "aclitem",
1034: "_aclitem",
1040: "_macaddr",
1041: "_inet",
651: "_cidr",
1263: "_cstring",
1042: "bpchar",
1043: "varchar",
1082: "date",
1083: "time",
1114: "timestamp",
1115: "_timestamp",
1182: "_date",
1183: "_time",
1184: "timestamptz",
1185: "_timestamptz",
1186: "interval",
1187: "_interval",
1231: "_numeric",
1266: "timetz",
1270: "_timetz",
1560: "bit",
1561: "_bit",
1562: "varbit",
1563: "_varbit",
1700: "numeric",
1790: "refcursor",
2201: "_refcursor",
2202: "regprocedure",
2203: "regoper",
2204: "regoperator",
2205: "regclass",
2206: "regtype",
2207: "_regprocedure",
2208: "_regoper",
2209: "_regoperator",
2210: "_regclass",
2211: "_regtype",
2950: "uuid",
2951: "_uuid",
3614: "tsvector",
3642: "gtsvector",
3615: "tsquery",
3734: "regconfig",
3769: "regdictionary",
3643: "_tsvector",
3644: "_gtsvector",
3645: "_tsquery",
3735: "_regconfig",
3770: "_regdictionary",
2970: "txid_snapshot",
2949: "_txid_snapshot",
3904: "int4range",
3905: "_int4range",
3906: "numrange",
3907: "_numrange",
3908: "tsrange",
3909: "_tsrange",
3910: "tstzrange",
3911: "_tstzrange",
3912: "daterange",
3913: "_daterange",
3926: "int8range",
3927: "_int8range",
2249: "record",
2287: "_record",
2275: "cstring",
2276: "any",
2277: "anyarray",
2278: "void",
2279: "trigger",
3838: "event_trigger",
2280: "language_handler",
2281: "internal",
2282: "opaque",
2283: "anyelement",
2776: "anynonarray",
3500: "anyenum",
3115: "fdw_handler",
3831: "anyrange",
10000: "pg_attrdef",
10001: "pg_constraint",
10002: "pg_inherits",
10003: "pg_index",
10004: "pg_operator",
10005: "pg_opfamily",
10006: "pg_opclass",
10117: "pg_am",
10118: "pg_amop",
10522: "pg_amproc",
10814: "pg_language",
10815: "pg_largeobject_metadata",
10816: "pg_largeobject",
10817: "pg_aggregate",
10818: "pg_statistic",
10819: "pg_rewrite",
10820: "pg_trigger",
10821: "pg_event_trigger",
10822: "pg_description",
10823: "pg_cast",
11020: "pg_enum",
11021: "pg_namespace",
11022: "pg_conversion",
11023: "pg_depend",
1248: "pg_database",
11024: "pg_db_role_setting",
11025: "pg_tablespace",
11026: "pg_pltemplate",
2842: "pg_authid",
2843: "pg_auth_members",
11027: "pg_shdepend",
11028: "pg_shdescription",
11029: "pg_ts_config",
11030: "pg_ts_config_map",
11031: "pg_ts_dict",
11032: "pg_ts_parser",
11033: "pg_ts_template",
11034: "pg_extension",
11035: "pg_foreign_data_wrapper",
11036: "pg_foreign_server",
11037: "pg_user_mapping",
11038: "pg_foreign_table",
11039: "pg_default_acl",
11040: "pg_seclabel",
11041: "pg_shseclabel",
11042: "pg_collation",
11043: "pg_range",
11044: "pg_toast_2604",
11045: "pg_toast_2606",
11046: "pg_toast_2609",
11047: "pg_toast_1255",
11048: "pg_toast_2618",
11049: "pg_toast_3596",
11050: "pg_toast_2619",
11051: "pg_toast_2620",
11052: "pg_toast_2396",
11053: "pg_toast_2964",
11055: "pg_roles",
11058: "pg_shadow",
11061: "pg_group",
11064: "pg_user",
11067: "pg_rules",
11071: "pg_views",
11075: "pg_tables",
11079: "pg_matviews",
11083: "pg_indexes",
11087: "pg_stats",
11091: "pg_locks",
11094: "pg_cursors",
11097: "pg_available_extensions",
11100: "pg_available_extension_versions",
11103: "pg_prepared_xacts",
11107: "pg_prepared_statements",
11110: "pg_seclabels",
11114: "pg_settings",
11119: "pg_timezone_abbrevs",
11122: "pg_timezone_names",
11125: "pg_stat_all_tables",
11129: "pg_stat_xact_all_tables",
11133: "pg_stat_sys_tables",
11137: "pg_stat_xact_sys_tables",
11140: "pg_stat_user_tables",
11144: "pg_stat_xact_user_tables",
11147: "pg_statio_all_tables",
11151: "pg_statio_sys_tables",
11154: "pg_statio_user_tables",
11157: "pg_stat_all_indexes",
11161: "pg_stat_sys_indexes",
11164: "pg_stat_user_indexes",
11167: "pg_statio_all_indexes",
11171: "pg_statio_sys_indexes",
11174: "pg_statio_user_indexes",
11177: "pg_statio_all_sequences",
11181: "pg_statio_sys_sequences",
11184: "pg_statio_user_sequences",
11187: "pg_stat_activity",
11190: "pg_stat_replication",
11193: "pg_stat_database",
11196: "pg_stat_database_conflicts",
11199: "pg_stat_user_functions",
11203: "pg_stat_xact_user_functions",
11207: "pg_stat_bgwriter",
11210: "pg_user_mappings",
11499: "cardinal_number",
11501: "character_data",
11502: "sql_identifier",
11504: "information_schema_catalog_name",
11506: "time_stamp",
11507: "yes_or_no",
11510: "applicable_roles",
11514: "administrable_role_authorizations",
11517: "attributes",
11521: "character_sets",
11525: "check_constraint_routine_usage",
11529: "check_constraints",
11533: "collations",
11536: "collation_character_set_applicability",
11539: "column_domain_usage",
11543: "column_privileges",
11547: "column_udt_usage",
11551: "columns",
11555: "constraint_column_usage",
11559: "constraint_table_usage",
11563: "domain_constraints",
11567: "domain_udt_usage",
11570: "domains",
11574: "enabled_roles",
11577: "key_column_usage",
11581: "parameters",
11585: "referential_constraints",
11589: "role_column_grants",
11592: "routine_privileges",
11596: "role_routine_grants",
11599: "routines",
11603: "schemata",
11606: "sequences",
11610: "sql_features",
11612: "pg_toast_11609",
11615: "sql_implementation_info",
11617: "pg_toast_11614",
11620: "sql_languages",
11622: "pg_toast_11619",
11625: "sql_packages",
11627: "pg_toast_11624",
11630: "sql_parts",
11632: "pg_toast_11629",
11635: "sql_sizing",
11637: "pg_toast_11634",
11640: "sql_sizing_profiles",
11642: "pg_toast_11639",
11645: "table_constraints",
11649: "table_privileges",
11653: "role_table_grants",
11656: "tables",
11660: "triggered_update_columns",
11664: "triggers",
11668: "udt_privileges",
11672: "role_udt_grants",
11675: "usage_privileges",
11679: "role_usage_grants",
11682: "user_defined_types",
11686: "view_column_usage",
11690: "view_routine_usage",
11694: "view_table_usage",
11698: "views",
11702: "data_type_privileges",
11706: "element_types",
11710: "_pg_foreign_table_columns",
11714: "column_options",
11717: "_pg_foreign_data_wrappers",
11720: "foreign_data_wrapper_options",
11723: "foreign_data_wrappers",
11726: "_pg_foreign_servers",
11730: "foreign_server_options",
11733: "foreign_servers",
11736: "_pg_foreign_tables",
11740: "foreign_table_options",
11743: "foreign_tables",
11746: "_pg_user_mappings",
11750: "user_mapping_options",
11754: "user_mappings",
153056: "wifi",
153055: "_wifi",
167151: "locs",
167150: "_locs",
167153: "pg_toast_167149",
171483: "occupancy",
171482: "_occupancy",
171485: "pg_toast_171481",
176360: "uptodateoccupancy",
176359: "_uptodateoccupancy"}

# prompt the user to enter a sql query
# users can also view the resultArray for python results
def runPrompt():
	query = raw_input("---your query or 'quit()'---\n> ")
	if query == "quit()":
		print "--- to return to SQL, type 'runPrompt()' ---"
		print "---        now exising to python         ---"
	else:
		try:
			resultArray = []
			resultArray = runQueryOnAllUsers(query)
			createAndPopulateTable(resultArray)
			print "--complete. check getfit.results in your datahub--"
		
		except Exception, e:
			print 

		# pdb.set_trace()
		runPrompt()

# query all users in the secret.allusers list
def runQueryOnAllUsers(query):
	results = []
	for user in secret.subsetOfUsers:
		try:
			# pdb.set_trace()
			transport = THttpClient.THttpClient('http://datahub.csail.mit.edu/service')
			transport = TTransport.TBufferedTransport(transport)
			protocol = TBinaryProtocol.TBinaryProtocol(transport)
			client = DataHub.Client(protocol)
			con_params = ConnectionParams(repo_base=user, app_id=secret.DHAPPID, app_token=secret.DHAPPTOKEN)
			con = client.open_connection(con_params=con_params)

			res = client.execute_sql(
					con=con,
					query=query,
					query_params=None)

			# save a variable for python
			results.append(res)

			# create a table in the operator's repo, so that they can query against it.
			# createAndPopulateTable(resultArray)

		except Exception, e:
			print "\n---EXCEPTION in runQueryOnAllUsers---"
			print e

	return results

	# print resultArray

# run sql creating and populating the getfit.results table
def createAndPopulateTable(resultArray):
	''' create a table to store the results
	'''
	
	# create the ddl script
	ddl = createDDL(resultArray)
	dml = createDML(resultArray)

	#concatinate the dml and ddl
	query = ddl + dml
	# print query

	try:
		transport = THttpClient.THttpClient('http://datahub.csail.mit.edu/service')
		transport = TTransport.TBufferedTransport(transport)
		protocol = TBinaryProtocol.TBinaryProtocol(transport)
		client = DataHub.Client(protocol)
		con_params = ConnectionParams(repo_base='al_carter', app_id=secret.DHAPPID, app_token=secret.DHAPPTOKEN)
		con = client.open_connection(con_params=con_params)

		res = client.execute_sql(
			con=con,
			query=query,
			query_params=None)

		resultArray.append(res)
		# print resultArray

	except Exception, e:
		print "\n---EXCEPTION in createAndPopulateTable ---"
		print e

# generate sql for creating the getfit.results table
def createDDL(resultArray):
	fieldNames = resultArray[0].field_names
	fieldTypes = resultArray[0].field_types

	ddl = "DROP TABLE IF EXISTS getfit.results; CREATE TABLE getfit.results (username text,"
	for i in range(0, len(fieldNames)):
		columnName = fieldNames[i]
		columnType = typeDict.get(int(fieldTypes[i]))
		ddl += columnName + " " + columnType + ", "

	ddl = ddl[:-2]
	ddl+= ");"
	return ddl

# generate sql for populating the getfit.results table
def createDML(resultArray):
	fieldNames = resultArray[0].field_names
	fieldTypes = resultArray[0].field_types
		# create the column names for the dml script
	dml = "INSERT INTO getfit.results (username, "
	for field in fieldNames:
		columnName = field
		dml += columnName + ", "

	dml = dml[:-2]
	dml+= ") values"

	# populate the values of the dml
	parsedColumns = []
	for i in range(0, len(resultArray)):
		# pdb.set_trace()
		print i
		print secret.subsetOfUsers[i]
		user = secret.subsetOfUsers[i]
		userResults = resultArray[i].tuples
		for tup in userResults:
			result = tup.cells
			parsedColumns = []
			for column in result:
				parsedColumns.append(stringOrNumber(column))
			dml += "('"+user + "', "
			for column in parsedColumns:
				if isinstance(column, basestring):
					dml += "'" + column + "', "
				else:
					dml += str(column) + ", "		
			dml = dml[:-2] + "), "

	dml = dml[:-2]

	return dml
	
# return bool, null, or strings for sql
def stringOrNumber(object):
	if object == "True":
		return True
	if object == "False":
		return False
	if object == "":
		return "null"

	try:
		int(object)
		return int(object)
	except:
		pass
	try:
		float(object)
		return float(object)
	except:
		pass
	return object

runPrompt()